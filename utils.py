from svgpathtools import svg2paths
import numpy as np


def load(filename):
    # load path from file
    paths, _ = svg2paths(filename)
    # turn paths into array of points
    points = np.array([shape.points(np.linspace(0, 1, 100))
                      for path in paths for shape in path]).reshape(-1).conjugate()

    # normalise points to centre
    # and size of 1
    points -= points.mean()
    points /= max(abs(points))
    return points


def fft(points, n):
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
