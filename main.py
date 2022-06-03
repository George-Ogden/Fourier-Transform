from svgpathtools import svg2paths
from manim import *
import numpy as np


class ArrayMobject(Mobject):
    def __init__(self, array=None):
        super().__init__()
        self.set_data(array)

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def sum(self):
        return ArrayMobject(np.add.accumulate(self.get_data()))

    def __getitem__(self, idx):
        return self.get_data()[idx]

    def become(self, new_obj):
        self.set_data(new_obj.get_data())


class NestedPath(VMobject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def updater(self, point, fade):
        previous_path = NestedPath()
        self.add(previous_path)
        previous_path.set_points_as_corners(self.points.copy())
        previous_path.add_updater(lambda path: path.fade(
            fade) if path.get_stroke_opacity() > 1e-3 else path.clear_updaters())
        self.add_points_as_corners([point])
        self.set_points_as_corners(self.points[-4:])


class FourierScene(Scene):
    scale = 3
    colour = TEAL

    def __init__(self, filename="github.svg",  n=50, rotations=.5, duration=3, fade=.005, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = self.load(filename)
        self.N = n
        self.rotations = rotations
        self.duration = duration
        self.fade = fade

    def construct(self):
        amplitudes, frequencies, phases = self.fft(self.points, self.N)

        tracker = ValueTracker(0)
        arrows = [Arrow(ORIGIN, RIGHT) for _ in range(self.N)]
        circles = [Circle(radius=self.scale * amplitudes[i], color=self.colour,
                          stroke_width=2, stroke_opacity=.5) for i in range(self.N)]
        path = NestedPath()

        values = ArrayMobject()
        cumulative = ArrayMobject()
        values.add_updater(lambda array, dt: array.set_data(np.array(
            [0] + [self.scale*a*np.exp(1j*(p+tracker.get_value()*f)) for a, f, p in zip(amplitudes, frequencies, phases)])), call_updater=True)
        cumulative.add_updater(lambda array, dt: array.become(
            values.sum()), call_updater=True)

        self.add(*arrows, *circles, values, cumulative, path)

        for i, (arrow, ring) in enumerate(zip(arrows, circles)):
            arrow.idx = i
            ring.idx = i
            ring.add_updater(lambda ring: ring.move_to(
                complex_to_R3(cumulative[ring.idx])))
            arrow.add_updater(lambda arrow: arrow.become(Arrow(complex_to_R3(
                cumulative[arrow.idx]), complex_to_R3(cumulative[arrow.idx+1]), buff=0, max_tip_length_to_length_ratio=.2, stroke_width=2, stroke_opacity=.8)))

        path.set_points_as_corners([complex_to_R3(cumulative[-1])] * 2)
        path.add_updater(lambda path: path.updater(
            complex_to_R3(cumulative[-1]), self.fade))

        self.play(tracker.animate.set_value(self.rotations * 2 * np.pi),
                  run_time=self.duration, rate_func=linear)

    @staticmethod
    def load(filename):
        paths, _ = svg2paths(filename)
        points = np.array([shape.points(np.linspace(0, 1, 100))
                          for path in paths for shape in path]).reshape(-1).conjugate()
        points -= points.mean()
        points /= max(abs(points))
        return points

    @staticmethod
    def fft(points, n):
        coefficients = np.fft.fft(points, norm="forward")
        frequencies = np.fft.fftfreq(len(points), 1/len(points))
        indices = np.argsort(-abs(coefficients))[:n]
        frequencies = frequencies[indices]
        coefficients = coefficients[indices]
        phases = np.angle(coefficients)
        amplitudes = abs(coefficients)
        return amplitudes, frequencies, phases
