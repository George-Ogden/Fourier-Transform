from svgpathtools import svg2paths
import cv2

from manim import config
from typing import Tuple
import numpy as np


def normalise(points: np.ndarray) -> np.ndarray:
    # scale the points to fill 90% of the screen
    # and place them in the centre
    points /= max((max(points.real) - min(points.real)) / config.frame_width,
                  (max(points.imag) - min(points.imag)) / config.frame_height) / .9
    points -= (max(points.real) + min(points.real)) / 2 - \
        (max(points.imag) + min(points.imag)) / 2j
    return points


def load_svg(filename: str) -> np.ndarray:
    # load path from file
    paths, _ = svg2paths(filename)
    # turn paths into array of points
    points = np.array([shape.points(np.linspace(0, 1, 1000))
                      for path in paths for shape in path]).reshape(-1).conjugate()
    return normalise(points)


def load_image(filename: str) -> np.ndarray:
    # load image from file
    image = cv2.imread(filename)
    # scale image to 1080 x 920 (max)
    scale = min(920 / image.shape[0], 1080 / image.shape[1])
    image = cv2.resize(
        image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))

    # find edges
    edges = cv2.Canny(image, 100, 100)
    # create contours
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = np.array(contours, dtype=object)
    # only keep contours with 50 or more pixels
    contours = contours[np.vectorize(len)(contours) > 50]
    # convert contours into complex numbers
    points = np.concatenate(contours).reshape(-1, 2)
    points = points[:, 0] - 1j * points[:, 1]

    # find shortest path for better drawing
    points = shortest_path(points)

    # normalise
    return normalise(points)


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


def shortest_path(points: np.ndarray) -> np.ndarray:
    # keep only unique points
    points = np.unique(points)
    # initialise empty path
    path = np.ndarray(len(points), dtype=complex)

    for i in range(len(points)):
        # find the nearest point
        nearest = np.abs(points - path[i-1]).argmin()
        # set the next element in the path to this value
        path[i] = points[nearest]
        # delete that point
        points = np.delete(points, nearest)

    return path
