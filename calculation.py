from svgpathtools import *
import numpy as np

import matplotlib.pyplot as plt
paths, attributes = svg2paths('github.svg')

points = np.array([shape.points(np.linspace(0,1,100)) for path in paths for shape in path]).reshape(-1)
# points = np.array((points.real, points.imag))
fft = np.fft.fft(points)
fft[np.argsort(abs(fft))[:-50]] = 0

points = np.fft.ifft(fft)


plt.scatter(points.real, points.imag)
plt.show()