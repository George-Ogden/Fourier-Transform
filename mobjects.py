from __future__ import annotations
from manim import *
import numpy as np


# updating object to contain arrays
class ArrayMobject(Mobject):
    def __init__(self, array : np.ndarray = None):
        super().__init__()
        # save the data
        self.set_data(array)

    # data getter
    def get_data(self) -> np.ndarray:
        return self.__data

    # data setter
    def set_data(self, data : np.ndarray):
        self.__data = data

    def sum(self) -> ArrayMobject:
        # accumulate data and return new mobject
        return ArrayMobject(np.add.accumulate(self.get_data()))

    # easy indexing
    def __getitem__(self, idx: int) -> float:
        return self.get_data()[idx]

    def become(self, new_obj : ArrayMobject):
        # don't create new mobject
        self.set_data(new_obj.get_data())

        # standard
        return self


class NestedPath(VMobject):
    def updater(self, point : np.ndarray, fade: float):
        # save previous path
        # as submobject
        previous_path = NestedPath()
        self.add(previous_path)

        # add new point to corner
        # and fade while visible
        previous_path.set_points_as_corners(self.points.copy())
        previous_path.add_updater(lambda path: path.fade(
            fade) if path.get_stroke_opacity() > 2e-2 else path.clear_updaters())

        # add to path
        # and truncate points
        self.add_points_as_corners([point])
        self.set_points_as_corners(self.points[-4:])

        # standard
        return self
