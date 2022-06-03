from svgpathtools import svg2paths
import numpy as np

def load(filename):
    paths, _ = svg2paths(filename)
    points = np.array([shape.points(np.linspace(0,1,100)) for path in paths for shape in path]).reshape(-1).conjugate()
    points -= points.mean()
    points /= max(abs(points))
    return points

def fft(points, n):
    coefficients = np.fft.fft(points,norm="forward")
    frequencies = np.fft.fftfreq(len(points),1/len(points))
    indices = np.argsort(-abs(coefficients))[:n]
    frequencies = frequencies[indices]
    coefficients = coefficients[indices]
    phases = np.angle(coefficients)
    amplitudes = abs(coefficients)
    return amplitudes, frequencies, phases