from app.abc import NonLinearCurve

class CubicCurve(NonLinearCurve):
    def __init__(self, points, generate_LUT=True):
        """
        Creates a cubic Bézier Curve based on four absolute points.
        """
        if len(points) != 4:
            raise ValueError("You can only generate a cubic curve from 4 points")

        self.a = points[3] - 3 * points[2] + 3 * points[1] - points[0]
        self.b = points[2] - 2 * points[1] + points[0]
        self.c = points[1] - points[0]
        self.d = points[0]

        super().__init__(points, generate_LUT=generate_LUT)

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
