"""Util functions related to creation of curves"""
from app.curves import Line, QuadraticCurve, CubicCurve, NthDegreeCurve
from app.abc.curve import Curve


def make_curve(points, relative=False):
    """
    Creates a bezier curve based on any number of points.

    If relative is set to true, the points are converted form relative
    points to absolute using the first point in the list as the base.
    """
    if relative:
        points = Curve.convert_rel_points_to_abs_points(points[0], points[1:])

    if len(points) == 2:
        return Line(points)
    if len(points) == 3:
        return QuadraticCurve(points)
    if len(points) == 4:
        return CubicCurve(points)
    if len(points) > 4:
        return NthDegreeCurve(points)

    raise ValueError("The number of points needs to be higher than one")
