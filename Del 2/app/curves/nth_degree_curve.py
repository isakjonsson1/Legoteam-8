"""Contains the NthDegreeCurve class"""
from app.abc import NonLinearCurve
from app.curves import CubicCurve


class NthDegreeCurve(NonLinearCurve):
    """Used to represent a Bézier Curve of nth degree where n > 4"""

    def __init__(self, points, generate_lut=True):
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
            curve = CubicCurve(points, generate_lut=False)
            self.get_pos = curve.get_pos
            self.get_vel = curve.get_vel
            self.get_acc = curve.get_acc
        else:
            self._subcurve0 = self.__class__(points[:-1], generate_lut=False)
            self._subcurve1 = self.__class__(points[1:], generate_lut=False)

        super().__init__(points, generate_lut=generate_lut)

    def get_pos(self, t_param):  # pylint disable=method-hidden
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (1 - t_param) * self._subcurve0.get_pos(
            t_param
        ) + t_param * self._subcurve1.get_pos(t_param)

    def get_vel(self, t_param):  # pylint disable=method-hidden
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            (self._subcurve1.get_pos(t_param) - self._subcurve0.get_pos(t_param))
            + (1 - t_param) * self._subcurve0.get_vel(t_param)
            + t_param * self._subcurve1.get_vel(t_param)
        )

    def get_acc(self, t_param):  # pylint disable=method-hidden
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            2 * (self._subcurve1.get_vel(t_param) - self._subcurve0.get_vel(t_param))
            + (1 - t_param) * self._subcurve0.get_acc(t_param)
            + t_param * self._subcurve1.get_acc(t_param)
        )
