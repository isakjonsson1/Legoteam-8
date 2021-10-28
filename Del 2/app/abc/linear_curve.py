"""Contains the abstract class LinearCurve"""

from app.abc import Curve


class LinearCurve(Curve):
    """
    An abstract class for linear curves. This type of curve assumes that
    atraversed distance is proportional at any point on the curve
    """

    def __init__(self, points):
        """Creates a curve given a list of points"""
        super().__init__(points)

    def get_t(self, traversed_length):
        """Finds a t given a traversed arc-length"""
        if traversed_length < 0 or self.length() <= traversed_length:
            raise ValueError(
                "traversed length needs to be greater than 0 and under the total arc-length"
            )

        return traversed_length / self.length()
