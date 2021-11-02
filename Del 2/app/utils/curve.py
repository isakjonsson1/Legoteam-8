from app.curves import Line, QuadraticCurve, CubicCurve, NthDegreeCurve
from app.abc.curve import Curve


def make_curve(points):
    """Creates a bezier curve based on any number of points"""
    if len(points) == 2:
        return Line(points)
    if len(points) == 3:
        return QuadraticCurve(points)
    if len(points) == 4:
        return CubicCurve
    if len(points) > 4:
        return NthDegreeCurve(points)
    else:
        raise ValueError("The number of points needs to be higher than one")


def make_curve_relative(points):
    """
    Creates a bezier curve based on any number of points.
    The points gievn in a relative manner where the first point is given in absolute coordinates,
    while the other points are calculated based on it.
    """
    points = Curve.convert_rel_points_to_abs_points(points[0], points[1:])
    return make_curve(points)
