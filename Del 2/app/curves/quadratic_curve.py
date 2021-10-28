"""Contais the QuadraticCurve class"""
from app.abc import NonLinearCurve

class QuadraticCurve(NonLinearCurve):
    """Used to represent a quadratic Bézier Curve"""

    def __init__(self, points, generate_lut=True):
        """
        Creates a quadratic Bézier Curve based on three absolute points.
        """
        if len(points) != 3:
            raise ValueError("You can only generate a cubic curve from 3 points")

        self.compund_point_a = points[2] - points[1]
        self.compund_point_b = points[0] - points[1]

        super().__init__(points, generate_lut=generate_lut)

    def get_pos(self, t_param):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            self.points[1]
            + (t_param) ** 2 * (self.compund_point_a)
            + (1 - t_param) ** 2 * (self.compund_point_b)
        )

    def get_vel(self, t_param):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            2 * t_param * self.compund_point_a
            - 2 * (1 - t_param) * self.compund_point_b
        )

    def get_acc(self, t_param=None):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 2 * (self.compund_point_a + self.compund_point_b)
