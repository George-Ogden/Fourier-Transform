from calculation import *
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


class FourierScene(Scene):
    N = 10
    SCALE = 3
    def construct(self):
        points = load("github.svg")
        amplitudes, frequencies, phases = fft(points, self.N)
        tracker = ValueTracker(0)
        arrows = [Arrow(ORIGIN, RIGHT) for _ in range(self.N)]
        circles = [Circle(radius=self.SCALE * amplitudes[i]) for i in range(self.N)]
        values = ArrayMobject()
        cumulative = ArrayMobject()
        self.add(*arrows, *circles, values, cumulative)

        values.add_updater(lambda array, dt: array.set_data(np.array(
            [0] + [self.SCALE*a*np.exp(1j*(p+tracker.get_value()*f)) for a, f, p in zip(amplitudes, frequencies, phases)])), call_updater=True)
        cumulative.add_updater(lambda array, dt: array.become(
            values.sum()), call_updater=True)

        for i, (arrow, ring) in enumerate(zip(arrows, circles)):
            arrow.idx = i
            ring.idx = i
            ring.add_updater(lambda ring: ring.move_to(
                complex_to_R3(cumulative[ring.idx])))
            arrow.add_updater(lambda arrow: arrow.become(Arrow(complex_to_R3(
                cumulative[arrow.idx]), complex_to_R3(cumulative[arrow.idx+1]), buff=0)))

        self.play(tracker.animate.set_value(np.pi),
                  run_time=3, rate_func=linear)
