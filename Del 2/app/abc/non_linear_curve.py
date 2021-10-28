from numpy import linspace

from app.abc import Curve


class NonLinearCurve(Curve):
    """
    An abstract class for nonlinear curves. Uses a look-up table to convert
    from traversed distance to the t value of a given point on the curve.
    """

    def __init__(self, points, n=100, generate_LUT=True):
        """
        Creates a Curve and generates a look-up table (LUT) for the curve based
        on an arbitrary list of points.
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
