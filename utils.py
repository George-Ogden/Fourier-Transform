from typing import Tuple, Callable, Union
from manim import config
import numpy as np

from svgpathtools import svg2paths
from PIL import ImageFont, Image
from paths import *
import cv2


def normalise(points: np.ndarray, return_factor: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, float]]:
    # scale the points to fill 90% of the screen
    # and place them in the centre
    scale = max((max(points.real) - min(points.real)) / config.frame_width,
                (max(points.imag) - min(points.imag)) / config.frame_height) / .9
    points /= scale
    points -= (max(points.real) + min(points.real)) / 2 - \
        (max(points.imag) + min(points.imag)) / 2j
    # return relevant data
    if return_factor:
        return points, scale
    else:
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


def extract_edges(image: np.ndarray, shortest_path: Callable[[np.ndarray], np.ndarray] = self_organising_maps) -> np.ndarray:
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
    points, scale = normalise(points, True)
    return shortest_path(points[::int(scale/10)])


def load_svg(filename: str) -> np.ndarray:
    # load path from file
    paths, _ = svg2paths(filename)
    # turn paths into array of points
    points = np.concatenate([shape.points(np.linspace(0, 1, 100 * int(shape.length())))
                      for path in paths for shape in path]).conjugate()
    # normalise 
    # and then subsample points
    points, scale = normalise(points, True)
    return points[::int(scale)]


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


def load_text(text: str, font: str) -> np.ndarray:
    # load font
    font = ImageFont.truetype(font, size=1000)
    # find the mask
    mask = font.getmask(text, mode="1")
    # convert to opencv-style image
    image = Image.frombytes(mask.mode, mask.size, bytes(mask))
    image = np.array(image)
    # extract edges
    return extract_edges(image, greedy_shortest_path)
