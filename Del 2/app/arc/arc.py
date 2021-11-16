"""Holds the Arc class"""
import math
from app.abc import NonLinearCurve
from app.point.point import Point


class Arc(NonLinearCurve):
    """Represents a eliptical arc"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        points,
        large_arc,
        sweep,
        rotation=0,
        generate_lut=True,
    ):
        """Defines an arc based on the parameters passed

        --Params--
        :param points: The points that define the arc. This first point and the last point
                       are the start and end points, while the middle point (2nd point) is
                       the unrotated radius in the x and y directions.
        :param large_arc: Specifies if the desired arc is the large one
        :param sweep: Specified the desired sweep direcion (read the svg docs for more info)
        :param rotation: rotation of the elipse i relation to a unrotated coordinate system
        :param generae_lup: Speciies if generating a look-up table is desired. This is
                            necesery to derive a t value from distance traveled.
        """
        self.large_arc = large_arc
        self.sweep = sweep
        self.rotation = -math.radians(rotation)

        if len(points) != 3:
            raise ValueError(
                "The number of points given must equal 3 [start_pos, radii, end_pos]"
            )

        helper = self.calc_helper(
            start_pos=points[0],
            end_pos=points[2],
            rotation=self.rotation,
        )

        self.radii = self.correct_radii(points[1], helper)

        center_helper = self.calc_center_helper(helper, self.radii, large_arc, sweep)

        self.center = self.calc_center(
            center_helper, self.rotation, staring_pos=points[0], end_pos=points[-1]
        )

        self._start_angle = self.calc_start_angle(helper, center_helper, self.radii)
        self._angle_delta = self.calc_angle_delta(
            helper, center_helper, self.radii, sweep
        )

        super().__init__(points, generate_lut=generate_lut)

    def get_pos(self, t_param):
        """
        Returns the position at a given t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        angle = self._start_angle + t_param * self._angle_delta
        point = Point(self.radii.x * math.cos(angle), self.radii.y * math.sin(angle))

        if self.rotation:
            point = point.rotated(self.rotation)

        return point + self.center

    def get_vel(self, t_param):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        angle = self._start_angle + t_param * self._angle_delta
        point = Point(
            -self._angle_delta * self.radii.x * math.sin(angle),
            self._angle_delta * self.radii.y * math.cos(angle),
        )

        if self.rotation:
            point = point.rotated(self.rotation)

        return point

    def get_acc(self, t_param):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        angle = self._start_angle + t_param * self._angle_delta
        point = Point(
            -self._angle_delta ** 2 * self.radii.x * math.cos(angle),
            -self._angle_delta ** 2 * self.radii.y * math.sin(angle),
        )

        if self.rotation:
            point = point.rotated(self.rotation)

        return point

    @staticmethod
    def calc_helper(start_pos, end_pos, rotation):
        """
        Calculates the helper point based on the given params.
        See https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        for explanation
        """
        helper = ((start_pos - end_pos) * 0.5).rotated(-rotation)
        return helper

    @staticmethod
    def correct_radii(radii, helper):
        """
        Returns a corrected radii based on the original radii and helper.
        See https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        for explanation
        """
        big_lambda = (helper.x / radii.x) ** 2 + (helper.y / radii.y) ** 2

        result = Point(radii.x, radii.y)
        if big_lambda > 1:
            result *= math.sqrt(big_lambda)

        return result

    @staticmethod
    def calc_center_helper(helper, radii, large_arc, sweep):
        """
        Calculates the center_helper based on the given params.
        See https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        for explanation
        """
        try:
            center_helper = math.sqrt(
                (
                    (radii.x * radii.y) ** 2
                    - (radii.x * helper.y) ** 2
                    - (radii.y * helper.x) ** 2
                )
                / ((radii.x * helper.y) ** 2 + (radii.y * helper.x) ** 2)
            ) * Point(
                radii.x * helper.y / radii.y,
                -radii.y * helper.x / radii.x,
            )
        except ValueError:  # sqr of something negative
            center_helper = Point(0, 0)

        if large_arc == sweep:
            center_helper *= -1

        return center_helper

    @staticmethod
    def calc_center(center_helper, rotation, staring_pos, end_pos):
        """
        Calculates the center based on the given params.
        See https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        for explanation
        """
        return center_helper.rotated(rotation) + (staring_pos + end_pos) * 0.5

    @staticmethod
    def calc_start_angle(helper, center_helper, radii):
        """
        Calculates the start angle based on the given params.
        See https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        for explanation
        """
        point2 = helper - center_helper
        point2.x /= radii.x
        point2.y /= radii.y
        return Point.angle_between(Point(1, 0), point2)

    @staticmethod
    def calc_angle_delta(helper, center_helper, radii, sweep):
        """
        Calculates the angle delta based on the given params.
        See https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        for explanation
        """
        point1 = helper - center_helper
        point1.x /= radii.x
        point1.y /= radii.y

        point2 = -helper - center_helper
        point2.x /= radii.x
        point2.y /= radii.y

        angle_delta = Point.angle_between(point1, point2) % (math.pi * 2)

        if sweep:
            angle_delta -= math.pi * 2

        return angle_delta
