from calculation import *
from manim import *
import numpy as np

n = 50


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


class FourierScene(Scene):
    def construct(self):
        points = load("github.svg")
        amplitudes, frequencies, phases = fft(points, n)
        tracker = ValueTracker(0)
        arrows = [Arrow(ORIGIN, RIGHT) for _ in range(n)]
        values = ArrayMobject()
        cumulative = ArrayMobject()
        self.add(*arrows, values, cumulative)

        values.add_updater(lambda array, dt: array.set_data(np.array(
            [0] + [3*a*np.exp(1j*(p+tracker.get_value()*f)) for a, f, p in zip(amplitudes, frequencies, phases)])), call_updater=True)
        cumulative.add_updater(lambda array, dt: array.become(
            values.sum()), call_updater=True)

        for i, arrow in enumerate(arrows):
            arrow.idx = i
            arrow.add_updater(lambda arrow: arrow.become(Arrow(complex_to_R3(
                cumulative[arrow.idx]), complex_to_R3(cumulative[arrow.idx+1]))))

        self.play(tracker.animate.set_value(np.pi),
                  run_time=3, rate_func=linear)
