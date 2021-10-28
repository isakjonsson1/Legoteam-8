"""Contains the CubicCurve class"""
from app.abc import NonLinearCurve


class CubicCurve(NonLinearCurve):
    """A curve used to represent a cubic Bézier Curve"""

    def __init__(self, points, generate_lut=True):
        """
        Creates a cubic Bézier Curve based on four absolute points.
        """
        if len(points) != 4:
            raise ValueError("You can only generate a cubic curve from 4 points")

        self.compound_point_a = points[3] - 3 * points[2] + 3 * points[1] - points[0]
        self.compound_point_b = points[2] - 2 * points[1] + points[0]
        self.compound_point_c = points[1] - points[0]
        self.compound_point_d = points[0]

        super().__init__(points, generate_lut=generate_lut)

    def get_pos(self, t_param):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            t_param ** 3 * self.compound_point_a
            + 3 * t_param ** 2 * self.compound_point_b
            + 3 * t_param * self.compound_point_c
            + self.compound_point_d
        )

    def get_vel(self, t_param):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            3 * t_param ** 2 * self.compound_point_a
            + 6 * t_param * self.compound_point_b
            + 3 * self.compound_point_c
        )

    def get_acc(self, t_param):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 6 * t_param * self.compound_point_a + 6 * self.compound_point_b
