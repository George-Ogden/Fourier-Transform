from manim import *
import numpy as np

import shutil
import os

from mobjects import ArrayMobject, NestedPath
from options import parse_args, config
from utils import load, fft


class FourierScene(Scene):
    # set scaling for circles and arrows
    scale = 4

    def __init__(self, filename : str,  number : int, rotations : int, duration : int, fade : float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # load points from svg
        self.points = load(filename)

        # setup settings
        self.N = number
        self.rotations = rotations
        self.duration = duration
        self.fade = fade

    def construct(self):
        # perform fft on points to produce N cycles
        amplitudes, frequencies, phases = fft(self.points, self.N)

        # initialise time at t = 0
        tracker = ValueTracker(0)
        # create arrows and circles for animation
        arrows = [Arrow(ORIGIN, RIGHT) for _ in range(self.N)]
        circles = [Circle(radius=self.scale * amplitudes[i], color=TEAL,
                          stroke_width=2, stroke_opacity=.5) for i in range(self.N)]
        # start a blank path
        path = NestedPath()

        # create values and points array for cycles
        values = ArrayMobject()
        cumulative = ArrayMobject()
        # set the value to e^i(a + wt)
        # and accumulate their sums
        values.add_updater(lambda array, dt: array.set_data(np.array([0] + [self.scale * a * np.exp(1j * (
            p + tracker.get_value() * f)) for a, f, p in zip(amplitudes, frequencies, phases)])), call_updater=True)
        cumulative.add_updater(lambda array, dt: array.become(
            values.sum()), call_updater=True)

        # draw mobjects in scene
        self.add(*arrows, *circles, values, cumulative, path)

        for i, (arrow, ring) in enumerate(zip(arrows, circles)):
            # give each object an id
            # then put the circle at the centre
            # and the arrow from the last to next point
            arrow.idx = i
            ring.idx = i
            ring.add_updater(lambda ring: ring.move_to(
                complex_to_R3(cumulative[ring.idx])))
            arrow.add_updater(lambda arrow: arrow.become(Arrow(complex_to_R3(cumulative[arrow.idx]), complex_to_R3(
                cumulative[arrow.idx+1]), buff=0, max_tip_length_to_length_ratio=.2, stroke_width=2, stroke_opacity=.8)))

        # add the last point to the path
        # and get the path to fade out
        path.set_points_as_corners([complex_to_R3(cumulative[-1])] * 2)
        path.add_updater(lambda path: path.updater(
            complex_to_R3(cumulative[-1]), self.fade))

        # play the animation
        self.play(tracker.animate.set_value(self.rotations * 2 * np.pi),
                  run_time=self.duration * self.rotations, rate_func=linear)


if __name__ == "__main__":
    # parse cli args (--help for more info)
    args = parse_args()

    # save the input file
    # and output file
    infile = args["options"]["filename"]
    outfile = args["options"]["output"]

    # split the file into directory, filename, extension
    head, tail = os.path.split(outfile)
    ext = os.path.splitext(tail)[1]
    # set the relevant manim config
    # then create directories
    config.output_file = tail
    if ext == ".gif":
        config.format = "gif"
    else:
        config.movie_file_extension = ext
    if head:
        os.makedirs(head, exist_ok=True)

    # render the scene
    scene = FourierScene(filename=infile, **args["Animation Options"])
    scene.render()

    # move file to the correct place and delete working directory
    shutil.copy(os.path.join(config.get_dir(
        "video_dir", module_name=os.path.dirname(infile)), tail), outfile)
    shutil.rmtree(config.media_dir)

    # preview file
    if args["options"]["preview"]:
        os.startfile(outfile)
