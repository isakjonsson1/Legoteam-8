"""Contains the Path class"""
from app.abc import Curve
from app.point.point import Point
from app.utils.curves import make_curve


class Path(list):
    """Represents a path (list of curves)"""

    def __init__(self, start_position=Point(0, 0)):
        """
        Creates a new path.
        Can take an iterable containing curves as an argument.
        """
        if not isinstance(start_position, Point):
            raise TypeError("Start position must be a Point")

        self._start_pos = start_position
        super().__init__()

    def append(self, curve):
        """Appends curve at the end of path"""
        if not isinstance(curve, Curve):
            raise TypeError("Appended item must be a curve")

        super().append(curve)

    def append_curve(self, points, relative=False):
        """
        Appends a new curve based on the current endpoint
        and a list of control points.

        If relative is set to True, the curve is calculated using relative
        positions of the points points[1:] using the first point (points[0]) as a base
        """
        curve = make_curve([self.end_position] + points, relative=relative)
        self.append(curve)

    def length(self):
        """Returns the total length of the path"""
        return sum(map(lambda s: s.length(), self))

    @property
    def start_position(self):
        """Returns the start postition of the path"""
        if len(self) == 0:
            return self._start_pos

        return self[0].get_start_pos()

    @property
    def start_angle(self):
        """Returns the start angle of the path"""
        return self[0].get_start_angle()

    @property
    def end_position(self):
        """Returns the end position of the path"""
        if len(self) == 0:
            return self.start_position

        return self[-1].get_end_pos()

    @property
    def end_angle(self):
        """Returns the end angle of the path"""
        return self[-1].get_end_angle()

    @property
    def min_position(self):
        """Retuns a point with the min x and y value"""
        min_x = min(point.x for curve in self for point in curve)
        min_y = min(point.y for curve in self for point in curve)
        return Point(min_x, min_y)

    @property
    def max_position(self):
        """Returns a point with the max x and y value"""
        max_x = max(point.x for curve in self for point in curve)
        max_y = max(point.y for curve in self for point in curve)
        return Point(max_x, max_y)

    @classmethod
    def from_curves_list(cls, curves):
        """Returns a path based on a list of curves"""
        result = cls()
        for curve in curves:
            result.append(curve)

        return result
