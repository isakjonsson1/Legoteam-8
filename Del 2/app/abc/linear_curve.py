from app.abc import Curve


class LinearCurve(Curve):
    """
    An abstract class for linear curves. This type of curve assumes that
    atraversed distance is proportional at any point on the curve
    """

    def __init__(self, points):
        """Creates a curve given a list of points"""
        super().__init__(points)

    def get_t(self, L):
        """Finds a t given a an arc-length L"""
        if L < 0 or self.length() <= L:
            raise ValueError("L needs to greater than 0 and under the total arc-length")

        return L / self.length()
