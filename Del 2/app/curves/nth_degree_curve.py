from app.abc import NonLinearCurve

class NthDegreeCurve(NonLinearCurve):
    def __init__(self, points, generate_LUT=True):
        """
        Creates a Bézier Curve in the nth degree based on n absolute points.
        Please use cubic or quadratic curves for an n less than five.
        """
        if len(points) < 4:
            raise ValueError(
                "Please use quadratic or cubic curves for curves of a degree less than 5"
            )

        # Re-assigns functions to not be reccursive if the curve is cubic
        if len(points) == 4:
            curve = CubicCurve(points, generate_LUT=False)
            self.get_pos = curve.get_pos
            self.get_vel = curve.get_vel
            self.get_acc = curve.get_acc
        else:
            self._subcurve0 = self.__class__(points[:-1], generate_LUT=False)
            self._subcurve1 = self.__class__(points[1:], generate_LUT=False)

        super().__init__(points, generate_LUT=generate_LUT)

    def get_pos(self, t):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (1 - t) * self._subcurve0.get_pos(t) + t * self._subcurve1.get_pos(t)

    def get_vel(self, t):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            (self._subcurve1.get_pos(t) - self._subcurve0.get_pos(t))
            + (1 - t) * self._subcurve0.get_vel(t)
            + t * self._subcurve1.get_vel(t)
        )

    def get_acc(self, t):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            2 * (self._subcurve1.get_vel(t) - self._subcurve0.get_vel(t))
            + (1 - t) * self._subcurve0.get_acc(t)
            + t * self._subcurve1.get_acc(t)
        )