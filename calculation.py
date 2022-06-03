from svgpathtools import *
import numpy as np
import matplotlib.pyplot as plt
paths, attributes = svg2paths('github.svg')

points = np.array([shape.points(np.linspace(0,1,100)) for path in paths for shape in path])
points = np.array((points.real, points.imag))

plt.scatter(*points)
plt.show()