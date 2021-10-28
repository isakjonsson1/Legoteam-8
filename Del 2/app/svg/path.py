"""Contains the Path class"""
from app.abc.curve import Curve
from app.utils.plotting import plot_curve


class Path(list):
    """Represents a path (list of curves)"""

    def __init__(self, iterable=None):
        """
        Creates a new path.
        Can take an iterable containing curves as an argument.
        """
        if iterable is not None:
            super().__init__(iterable)
            if not all(isinstance(curve, Curve) for curve in self):
                raise TypeError(
                    "The iterable supplied must only contain "
                    "instances of the class, or subclasses of the class Curve"
                )
        else:
            super().__init__()

    def append(self, curve):
        """Appends curve at the end of path"""
        if not isinstance(curve, Curve):
            raise TypeError("Appended item must be a curve")

        super().append(curve)

    def length(self):
        """Returns the total length of the path"""
        return sum(map(lambda s: s.length(), self))

    def plot_path(self):
        """Plots the entire path"""
        for curve in self:
            plot_curve(curve)

    @property
    def start_position(self):
        return self[0].get_start_pos()

    @property
    def start_angle(self):
        return self[0].get_start_angle()

    @property
    def end_position(self):
        return self[-1].get_end_pos()

    @property
    def end_angle(self):
        return self[-1].get_end_angle()
