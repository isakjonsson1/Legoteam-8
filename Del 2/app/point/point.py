"""Contains the class Point"""
import math


class Point:
    """Used to represent a 2d point"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotated(self, angle):
        """Returns a rotated (around origo) version of the point"""
        rotation = complex(math.cos(angle), math.sin(angle))
        imag_point = complex(self.x, self.y)
        imag_point *= rotation
        return Point(imag_point.real, imag_point.imag)

    def length(self):
        """Returns the distance from origo to the point"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x + other.x, self.y + other.y)

        raise TypeError(
            "unsupported operand type(s) for +: '{}' and '{type(other)}'".format(self.__class__)
        )

    def __sub__(self, other):
        return self + (-1) * other

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.x * other, self.y * other)

        raise TypeError(
            "unsupported operand type(s) for *: '{}' and '{}'".format(self.__class__, type(other))
        )

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __neg__(self):
        return self * -1

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "{}(x={}, y={})".format(type(self).__name__, self.x, self.y)

    @staticmethod
    def angle_between(point1, point2):
        """Returns the angle between two vectors from origo to the given points"""
        dot_prod = point1.x * point2.x + point1.y * point2.y
        angle = math.acos(dot_prod / (point1.length() * point2.length()))

        # Account for the positions of the point
        if point1.y * point2.x > point1.x * point2.y:
            angle *= -1

        return angle
