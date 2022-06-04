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
