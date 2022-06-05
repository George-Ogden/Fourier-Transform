from svgpathtools import svg2paths
from typing import Tuple
import numpy as np


def normalise(points: np.ndarray) -> np.ndarray:
    # centre points
    # and fit them in a unit circle
    points -= points.mean()
    points /= max(abs(points))
    return points


def load(filename: str) -> np.ndarray:
    # load path from file
    paths, _ = svg2paths(filename)
    # turn paths into array of points
    points = np.array([shape.points(np.linspace(0, 1, 1000))
                      for path in paths for shape in path]).reshape(-1).conjugate()
    return normalise(points)


def polygon(n: int) -> np.ndarray:
    points = np.array([np.linspace(np.exp(2j * k * np.pi / n), np.exp(2j *
                      (k + 1) * np.pi / n), 1000) for k in range(n)]).reshape(-1)
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
