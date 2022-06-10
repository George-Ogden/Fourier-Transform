import numpy as np

from tqdm import trange
import platform

# adapted from https://github.com/diego-vicente/som-tsp
def self_organising_maps(points: np.ndarray, iterations: int = 0, learning_rate: float = 0.8) -> np.ndarray:
    # keep points only once
    # and then the population size is 8 times the number of cities
    points = np.unique(points)
    n = len(points) * 8

    # generate an adequate network of neurons
    network = np.random.uniform(min(points.real), max(
        points.real), n) + 1j * np.random.uniform(min(points.imag), max(points.imag), n)

    if iterations == 0:
        iterations = min(100000, int(np.log(n) / -np.log(.9997)))

    for _ in trange(iterations, desc="Optimising shape", ascii=True if platform.system() == "Windows" else None, leave=False):
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
    points *= 1j
    path[-1] = min(points[points.imag == min(points.imag)]) / 1j
    points /= 1j

    for i in trange(len(points), desc="Optimising shape", ascii=True if platform.system() == "Windows" else None, leave=False):
        # find the nearest point
        nearest = np.abs(points - path[i-1]).argmin()
        # set the next element in the path to this value
        path[i] = points[nearest]
        # delete that point
        points = np.delete(points, nearest)

    return path


def optimised_shortest_path(points: np.ndarray, iterations : int = 2) -> np.ndarray:
    # precompute greedy path
    points = greedy_shortest_path(points)

    for _ in range(iterations):
        # start with points that are already in place
        order = np.argsort(abs(points - np.roll(points, 1)) + abs(points - np.roll(points, -1)))
        for i in order:
            point = points[i]
            # remove the point
            points = np.delete(points, i)
            # find the best place to insert
            distances = abs(points - point)
            heuristic = distances + np.roll(distances, 1) - abs(points - np.roll(points, 1))
            nearest = heuristic.argmin()
            # insert back in the shortest place
            points = np.insert(points, nearest, point)        

    return points