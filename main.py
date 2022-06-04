from manim import *
import numpy as np

import shutil
import os

from mobjects import ArrayMobject, NestedPath
from options import parse_args, config
from utils import load, fft

class FourierScene(Scene):
    scale = 4
    colour = TEAL

    def __init__(self, filename,  number, rotations, duration, fade, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = load(filename)
        self.N = number
        self.rotations = rotations
        self.duration = duration
        self.fade = fade

    def construct(self):
        amplitudes, frequencies, phases = fft(self.points, self.N)

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
                  run_time=self.duration * self.rotations, rate_func=linear)

if __name__ == "__main__":
    args = parse_args()

    infile = args["options"]["filename"]
    outfile = args["options"]["output"]
    head, tail = os.path.split(outfile)
    ext = os.path.splitext(tail)[1]
    config.output_file = tail
    if ext == ".gif":
        config.format = "gif"
    else:
        config.movie_file_extension = os.path.splitext(tail)[1]

    if head:
        os.makedirs(head,exist_ok=True)

    scene = FourierScene(filename=infile,**args["Display Options"])
    scene.render()

    shutil.copy(os.path.join(config.get_dir("video_dir", module_name=os.path.dirname(infile)),tail), outfile)
    shutil.rmtree(config.media_dir)

    if args["options"]["preview"]:
        os.startfile(outfile)