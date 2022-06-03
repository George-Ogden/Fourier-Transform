from svgpathtools import svg2paths
import numpy as np

def load(filename):
    paths, _ = svg2paths(filename)
    return np.array([shape.points(np.linspace(0,1,100)) for path in paths for shape in path]).reshape(-1)

def fft(points):
    return np.fft.fft(points)