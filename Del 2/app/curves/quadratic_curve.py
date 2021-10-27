from app.abc import NonLinearCurve

class QuadraticCurve(NonLinearCurve):
    def __init__(self, points, generate_LUT=True):
        """
        Creates a quadratic Bézier Curve based on three absolute points.
        """
        if len(points) != 3:
            raise ValueError("You can only generate a cubic curve from 3 points")

        self.a = points[2] - points[1]
        self.b = points[0] - points[1]

        super().__init__(points, generate_LUT=generate_LUT)

    def get_pos(self, t):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return self.points[1] + (t) ** 2 * (self.a) + (1 - t) ** 2 * (self.b)

    def get_vel(self, t):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 2 * t * self.a - 2 * (1 - t) * self.b

    def get_acc(self, t=None):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 2 * (self.a + self.b)