from math import atan2
from numpy import linspace


class BaseCurve:
    def __init__(self, points):
        """
        Creates a Curve based on an arbitrary list of points.
        This is a baseclass and should not be instanced by itself.
        """

        self.points = points

    def get_curvature(self, t):
        """
        Returns the curvature of the curve at a given t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.

        The curvature is the inverse of the radius.
        """
        vel = self.get_vel(t)
        acc = self.get_acc(t)

        return (vel.x * acc.y - vel.y * acc.x) / ((vel.x ** 2 + vel.y ** 2) ** (3 / 2))

    def get_endpoint(self):
        """Returns the absolute position where the curve ended"""
        return self.points[-1]

    def get_exit_angle(self):
        """Returns the exit angle where the curve ends"""
        dSdt = self.get_vel(1)
        atan2(dSdt.y, dSdt.x)

    @staticmethod
    def convert_rel_points_to_abs_points(base, rel_points):
        """
        Converts a list of point using relative coordinates to a list using absolue coordinates.
        Start is given in absolute coordinates, while points are given relative to the start position.
        """
        points_abs = [base]

        for point in rel_points:
            points_abs.append(base + point)

        return points_abs


class BaseLUTCurve(BaseCurve):
    def __init__(self, points, n=100, generate_LUT=True):
        """
        Creates a Curve and generates a look-up table (LUT) for the curve based
        on an arbitrary list of points. This is a baseclass and should not
        be instanced by itself. n is the number of entries in the LUT
        """

        super().__init__(points)
        if generate_LUT:
            self.LUT = self.generate_LUT(n)

    def generate_LUT(self, n):
        """Generates a look-up table to convert from distance to t values [0, 1]"""

        # Initiates a new dict as an empty look-up table
        LUT = dict()

        # Samples of t in the interval [0, 1]
        ts = linspace(0, 1, n + 1)

        L = 0
        LUT[L] = 0

        last = self.get_pos(ts[0])
        for t in ts[1:]:
            current = self.get_pos(t)
            l = abs(current - last)
            last = current
            L += l
            LUT[L] = t

        return LUT

    def get_t(self, L):
        """Finds a t given a an arc-length L"""
        if L < 0 or self.length() <= L:
            raise ValueError("L needs to greater than 0 and under the total arc-length")

        min_L, max_L = self.bin_search_LUT(L)
        min_t, max_t = self.LUT[min_L], self.LUT[max_L]

        ratio = (L - min_L) / (max_L - min_L)
        return (max_t - min_t) * ratio + min_t

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

    def length(self):
        """Returns the toatal arc-lengt of the curve"""
        return list(self.LUT.keys())[-1]
