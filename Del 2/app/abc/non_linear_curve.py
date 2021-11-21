"""Contains the abstract class NonLinearCurve"""
import math
from app.abc import Curve


class NonLinearCurve(Curve):
    """
    An abstract class for nonlinear curves. Uses a look-up table to convert
    from traversed distance to the t value of a given point on the curve.
    """

    def __init__(self, points, number_of_entries=100, generate_lut=True):
        """
        Creates a Curve and generates a look-up table (LUT) for the curve based
        on an arbitrary list of points.
        """
        super().__init__(points)
        if generate_lut:
            self.look_up_table = self.generate_lut(number_of_entries)

    def generate_lut(self, number_of_entries):
        """Generates a look-up table to convert from distance to t values [0, 1]"""

        # Initiates a new dict as an empty look-up table
        look_up_table = {}

        # Samples of t in the interval <0, 1]
        delta = 1 / number_of_entries
        t_params = (i * delta for i in range(1, number_of_entries + 1))

        traversed_length = 0
        look_up_table[traversed_length] = 0

        last = self.get_pos(0)
        for t_param in t_params:
            current = self.get_pos(t_param)

            step_length = math.sqrt(
                (current.x - last.x) ** 2 + (current.y - last.y) ** 2
            )

            last = current
            traversed_length += step_length
            look_up_table[traversed_length] = t_param

        return look_up_table

    def get_t(self, traversed_length):
        """Finds a t given a an arc-length L"""
        if traversed_length < 0 or self.length() <= traversed_length:
            raise ValueError("L needs to greater than 0 and under the total arc-length")

        # Max and min traversed length
        min_length, max_length = self.bin_search_lut(traversed_length)

        # Max and min t_param
        min_t, max_t = self.look_up_table[min_length], self.look_up_table[max_length]

        ratio = (traversed_length - min_length) / (min_length - max_length)
        return (max_t - min_t) * ratio + min_t

    def bin_search_lut(self, traversed_length):
        """
        Returns an two values. The first one is the lower bound of the value from
        the look-up table (inclusive), and the other one is the upper bound (exclusive)
        """
        keys = list(self.look_up_table.keys())

        # Min and max index
        min_i, max_i = 0, len(keys) - 1

        # Min and max value
        min_v, max_v = 0, keys[max_i]

        while True:
            mid_i = (min_i + max_i) // 2
            mid_v = keys[mid_i]

            if traversed_length < mid_v:
                max_i = mid_i
                max_v = mid_v
            else:
                min_i = mid_i
                min_v = mid_v

            if min_i + 1 == max_i:
                return min_v, max_v

    def length(self):
        """Returns the toatal arc-lengt of the curve"""
        return list(self.look_up_table.keys())[-1]
