from math import atan2
from numpy import linspace


class Curve:
    def __init__(self, points):
        """
        Creates a Bézier Curve based on four absolute points.
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

        n = 100
        self.LUT = self.generate_LUT(n)
        self.dt = 1 / n

    def get_pos(self, t):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return t ** 3 * self.a + 3 * t ** 2 * self.b + 3 * t * self.c + self.d

    def get_vel(self, t):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 3 * t ** 2 * self.a + 6 * t * self.b + 3 * self.c

    def get_acc(self, t):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 6 * t * self.a + 6 * self.b

    def get_jerk(self):
        """Returns the jerk throughout the curve (the third order derivative)"""
        return 6 * self.a

    def get_curvature(self, t):
        """
        Returns the curvature of the curve at a given t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.

        The curvature is the inverse of the radius.
        """

        vel = self.get_vel(t)
        acc = self.get_acc(t)

        return (vel.x * acc.y - vel.y * acc.x) / ((vel.x ** 2 + vel.y ** 2) ** (3 / 2))

    def generate_LUT(self, n=100):
        """Generates a look-up table to convert from distance to t values [0, 1]"""

        # Initiates a new dict as an empty look-up table
        LUT = dict()

        # Samples of t in the interval [0, 1]
        ts = linspace(0, 1, n + 1)

        L = 0
        LUT[L] = 0

        lst = self.get_pos(ts[0])
        for t in ts[1:]:
            cur = self.get_pos(t)
            l = len(cur - lst)
            L += l
            LUT[L] = t

    def bin_search_LUT(self, L):
        """
        Returns an two values. The first one is the lower bound of the value from
        the look-up table (inclusive), and the other one is the upper bound (exclusive)
        """
        keys = list(self.LUT.keys())

        # Min and max index
        min_i, max_i = 0, len(keys) - 1
        # Min and max value
        min_v, max_v = 0, keys[max_i]

        while True:
            mid_i = (min_i + max_i) // 2
            mid_v = keys[mid_i]

            if L < mid_v:
                max_i = mid_i
                max_v = mid_v
            else:
                min_i = mid_i
                min_v = mid_v

            if min_i + 1 == max_i:
                return min_v, max_v

    def find_t(self, L):
        """Finds a t given a an arc-length L"""
        if L < 0 or len(self) <= L:
            raise ValueError("L needs to greater than 0 and under the total arc-length")

        min_L, max_L = self.bin_search_LUT(L)
        min_t, max_t = self.LUT[min_L], self.LUT[max_L]

        ratio = (L - min_L) / (max_L - min_L)
        return (max_t - min_t) * ratio + min_t

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

    def __len__(self):
        return self.LUT.keys()[-1]


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
