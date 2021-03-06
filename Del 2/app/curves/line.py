"""Contains the Line class"""
from app.abc import LinearCurve
from app.point import Point


class Line(LinearCurve):
    """Used to represent a line between two points."""

    def __init__(self, points):
        """
        Creates a straight linesegment between two points
        """
        if len(points) != 2:
            raise ValueError("A line is only defined between two points")
        super().__init__(points)

    def length(self):
        """Returns the total length of the curve"""
        return abs(self.points[1] - self.points[0])

    def get_pos(self, t_param):
        """
        Returns the position at a given t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (1 - t_param) * self.points[0] + t_param * self.points[1]

    # pylint: disable=unused-argument

    def get_vel(self, t_param=None):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        Since velocity is constant for a line, the t argument is optional.
        """
        return self.points[1] - self.points[0]

    # pylint: disable=no-self-use

    def get_acc(self, t_param=None):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        Since acceleration is constant for a line, the t argument is optional.
        """
        return Point(0, 0)

    def get_curvature(self, t_param=None):
        """
        Returns the curvature at a given t velue [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.

        Since this is a straight line, the curvature is always 0
        """
        return 0
