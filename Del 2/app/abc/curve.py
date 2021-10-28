"""Contains the abstract class Curve"""
from math import atan2
from abc import ABC, abstractmethod


class Curve(ABC):
    """An abstract class for all curves"""

    def __init__(self, points):
        """
        Creates a Curve based on an arbitrary list of points.
        This is an abstract class and cannot be instanced by itself.
        """
        self.points = points

    @abstractmethod
    def get_pos(self, t_param):
        """
        Returns the position at a given t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """

    @abstractmethod
    def get_vel(self, t_param):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """

    @abstractmethod
    def get_acc(self, t_param):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """

    @abstractmethod
    def get_t(self, traversed_length):
        """Finds a t given a an arc-length L"""

    @abstractmethod
    def length(self):
        """Returns the toatal arc-lengt of the curve"""

    def get_curvature(self, t_param):
        """
        Returns the curvature of the curve at a given t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.

        The curvature is the inverse of the radius.
        """
        vel = self.get_vel(t_param)
        acc = self.get_acc(t_param)

        return (vel.x * acc.y - vel.y * acc.x) / ((vel.x ** 2 + vel.y ** 2) ** (3 / 2))

    def get_start_pos(self):
        return self.points[0]

    def get_start_angle(self):
        return self.get_angle(0)

    def get_end_pos(self):
        """Returns the absolute position where the curve ended"""
        return self.points[-1]

    def get_end_angle(self):
        """Returns the exit angle where the curve ends"""
        return self.get_angle(1)

    def get_angle(self, t_param):
        vel = self.get_vel(t_param)
        return atan2(vel.y, vel.x)

    @staticmethod
    def convert_rel_points_to_abs_points(base, rel_points):
        """
        Converts a list of point using relative coordinates to a list using absolue coordinates.
        Start is given in absolute coordinates, while points are given relative to the start
        position.
        """
        points_abs = [base]

        for point in rel_points:
            points_abs.append(base + point)

        return points_abs
