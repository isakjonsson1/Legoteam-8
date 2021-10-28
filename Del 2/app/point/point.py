"""Contains the class Point"""
from math import sqrt

class Point:
    """Used to represent a 2d point"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x + other.x, self.y + other.y)

        raise TypeError(
            f"unsupported operand type(s) for +: '{self.__class__}' and '{type(other)}'"
        )

    def __sub__(self, other):
        return self + (-1) * other

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(self.x * other, self.y * other)

        raise TypeError(
            f"unsupported operand type(s) for *: '{self.__class__}' and '{type(other)}'"
        )

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"{type(self).__name__}(x={self.x}, y={self.y})"
