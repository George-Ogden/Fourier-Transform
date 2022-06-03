from svgpathtools import *
import numpy as np
import scipy.fft

import matplotlib.pyplot as plt
paths, attributes = svg2paths('github.svg')

points = np.array([shape.points(np.linspace(0,1,100)) for path in paths for shape in path]).reshape(-1)
# points = np.array((points.real, points.imag))
fft = scipy.fft.fft2((points.real, points.imag))
print(fft.shape)
points = scipy.fft.ifft2(fft[:,:1000])

# print(fft)
print(points.shape)

plt.scatter(*points)
plt.show()