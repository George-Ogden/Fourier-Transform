from manim import config
from typing import Tuple
import numpy as np

from svgpathtools import svg2paths
from PIL import ImageFont, Image
import cv2

from tqdm import trange
import platform


def normalise(points: np.ndarray) -> np.ndarray:
    # scale the points to fill 90% of the screen
    # and place them in the centre
    points /= max((max(points.real) - min(points.real)) / config.frame_width,
                  (max(points.imag) - min(points.imag)) / config.frame_height) / .9
    points -= (max(points.real) + min(points.real)) / 2 - \
        (max(points.imag) + min(points.imag)) / 2j
    return points


def fft(points: np.ndarray, n: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    # calculate fft using numpy
    coefficients = np.fft.fft(points, norm="forward")
    # get the frequencies
    frequencies = np.fft.fftfreq(len(points), 1/len(points))

    # keep only n largest frequencies
    indices = np.argsort(-abs(coefficients))[:n]
    frequencies = frequencies[indices]
    coefficients = coefficients[indices]

    # split complex numbers into modulus and argument
    phases = np.angle(coefficients)
    amplitudes = abs(coefficients)
    return amplitudes, frequencies, phases


# adapted from https://github.com/diego-vicente/som-tsp
def shortest_path(points: np.ndarray, learning_rate: float = 0.8) -> np.ndarray:
    # keep points only once 
    # and then the population size is 8 times the number of cities
    points = np.unique(points)
    n = len(points) * 8

    # generate an adequate network of neurons
    network = np.random.uniform(min(points.real), max(
        points.real), n) + 1j * np.random.uniform(min(points.imag), max(points.imag), n)

    for _ in trange(min(100000, int(np.log(n) / -np.log(.9997))), desc="Optimising shape", ascii=True if platform.system() == "Windows" else None, leave=False):
        # choose a random city
        point = np.random.choice(points)
        idx = abs(network - point).argmin()

        # generate a filter that applies changes to the winner's gaussian
        # compute the circular network distance to the center
        deltas = np.absolute(idx - np.arange(len(network)))
        distances = np.minimum(deltas, len(network) - deltas)
        # impose an upper bound on the radix to prevent NaN and blocks
        radix = max(n / 10, 1)
        # compute Gaussian distribution around the given center
        gaussian = np.exp(-(distances**2) / (2*radix**2))

        # update the network's weights (closer to the city)
        network += gaussian * learning_rate * (point - network)

        # decay the variables
        learning_rate *= 0.99997
        n *= 0.9997

    # find route from network
    route = points[np.argsort(
        [np.argmin(abs(network - point)) for point in points])]
    return route


def greedy_shortest_path(points: np.ndarray) -> np.ndarray:
    # keep points only once 
    points = np.unique(points)
    
    # initialise empty path
    path = np.ndarray(len(points), dtype=complex)

    for i in trange(len(points), desc="Optimising shape", ascii=True if platform.system() == "Windows" else None, leave=False):
        # find the nearest point
        nearest = np.abs(points - path[i-1]).argmin()
        # set the next element in the path to this value
        path[i] = points[nearest]
        # delete that point
        points = np.delete(points, nearest)

    return path


def extract_edges(image: np.ndarray, algorithm = shortest_path) -> np.ndarray:
    # find edges
    edges = cv2.Canny(image, 100, 100)
    # create contours
    contours_, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = np.ndarray(len(contours_), dtype=object)
    for i, contour in enumerate(contours_):
        contours[i] = contours_[i]
    # only keep contours with 50 or more pixels
    contours = contours[np.vectorize(len)(contours) > 50]
    # convert contours into complex numbers
    points = np.concatenate(contours).reshape(-1, 2)
    points = points[:, 0] - 1j * points[:, 1]
    # normalise
    # and find shortest path for better drawing
    points = normalise(points)
    return algorithm(points)


def load_svg(filename: str) -> np.ndarray:
    # load path from file
    paths, _ = svg2paths(filename)
    # turn paths into array of points
    points = np.array([shape.points(np.linspace(0, 1, 1000))
                      for path in paths for shape in path]).reshape(-1).conjugate()
    return normalise(points)


def load_image(filename: str, threshold: bool = True) -> np.ndarray:
    # load image from file
    image = cv2.imread(filename)
    # scale image to 1080 x 920 (max)
    scale = min(920 / image.shape[0], 1080 / image.shape[1])
    image = cv2.resize(
        image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))

    if threshold:
        # convert to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # find different areas
        image = 255 - \
            cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # find outlines of the areas
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # find largest area (background)
        largest = max(contours, key=cv2.contourArea)
        # shade everything that isn't the largest area
        image = np.zeros(image.shape, dtype=image.dtype)
        cv2.drawContours(image, [largest], -1, (255, 255, 255), -1)

    # find the edges to draw
    return extract_edges(image)


def polygon(n: int) -> np.ndarray:
    # roots of unity
    points = np.array([np.linspace(np.exp(2j * k * np.pi / n), np.exp(2j *
                      (k + 1) * np.pi / n), 1000) for k in range(n)]).reshape(-1)
    # scale the points to fill 90% of the screen
    # and rotate so start is top
    # and left if sides are even
    points *= config.frame_height * .9 / 2
    points *= 1j
    if not n % 2:
        points *= np.exp(1j * np.pi / n)
    return points


def load_text(text: str) -> np.ndarray:
    # load font
    font = ImageFont.truetype("arial-bold.ttf", size=1000)
    # find the mask
    mask = font.getmask(text, mode="1")
    # convert to opencv-style image
    image = Image.frombytes(mask.mode, mask.size, bytes(mask))
    image = np.array(image)
    # extract edges
    return extract_edges(image, greedy_shortest_path)