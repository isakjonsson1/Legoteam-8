from math import atan2


class Curve:
    def __init__(self, points):
        """
        Creates a Bézier Curve based on four absolute points
        """
        if len(points) != 4:
            raise ValueError("You can only generate a curve from 4 points")
        self.points = points
        self.a = (
            self.points[3] - 3 * self.points[2] + 3 * self.points[1] - self.points[0]
        )
        self.b = self.points[2] - 2 * self.points[1] + self.points[0]
        self.c = self.points[1] - self.points[0]
        self.d = self.points[0]

    def get_pos(self, t):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve
        """
        return t ** 3 * self.a + 3 * t ** 2 * self.b + 3 * t * self.c + self.d

    def get_vel(self, t):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve
        """
        return 3 * t ** 2 * self.a + 6 * t * self.b + 3 * self.c

    def get_acc(self, t):
        """
        Returns the acceleration at a give t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve
        """
        return 6 * t * self.a + 6 * self.b

    def get_jerk(self):
        """Returns the jerk throughout the curve (the third order derivative)"""
        return 6 * self.a

    def get_endpoint(self):
        """Returns the absolute position where the curve ended"""
        return self.points[-1]

    def get_exit_angle(self):
        """Returns the exit angle where the curve ends"""
        dSdt = self.get_vel(1)
        atan2(dSdt.y, dSdt.x)

    @classmethod
    def from_rel_points(cls, start, points):
        """
        Returns a curve based on one absulute point [start] and three aditional points¨
        with coordinates relative to the starting point
        """
        if len(points) != 3:
            raise ValueError(
                "You can only generate a curve from 4 points (1 start and 3 relative points)"
            )

        points_abs = [start]

        for point in points:
            points_abs.append(start + point)

        return cls(points_abs)


if __name__ == "__main__":
    # Test
    from Point import Point as P
    import numpy as np
    from matplotlib import pyplot as plt

    points = [P(0.25, 0), P(0, 1), P(1, 1), P(0.75, 0)]
    c = Curve(points)
    ts = np.linspace(0, 1)
    points = [c.get_pos(t) for t in ts]
    x = [point.x for point in points]
    y = [point.y for point in points]

    plt.plot(x, y)
    for point in c.points:
        plt.plot(point.x, point.y, marker="o")
    plt.show()
