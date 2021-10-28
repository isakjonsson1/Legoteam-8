import pytest
from app.abc.non_linear_curve import NonLinearCurve

from app.curves import Line
from app.curves import QuadraticCurve
from app.curves import NthDegreeCurve
from app.curves.cubic_curve import CubicCurve
from app.point import Point as P

points = [P(0.25, 0), P(0, 1), P(1, 1), P(0.75, 0), P(0, -1), P(1, -1)]


def test_line():
    l = Line(points[1:3])
    assert l.length() == 1
    assert l.get_t(0.5) == 0.5 / l.length()

    with pytest.raises(ValueError):
        l.get_t(2)
        l.get_t(-1)

    _test_curve(l)


def test_quadratic_curve():
    c = QuadraticCurve(points[:3])

    with pytest.raises(ValueError):
        QuadraticCurve(points[:2])
        QuadraticCurve(points[0:4])

    _test_curve(c)


def test_quadratic_curve():
    c = CubicCurve(points[:4])

    with pytest.raises(ValueError):
        CubicCurve(points[:3])
        QuadraticCurve(points[0:5])

    _test_curve(c)


def test_nth_degree_curve():
    c = NthDegreeCurve(points)

    with pytest.raises(ValueError):
        NthDegreeCurve(points[0:3])

    _test_curve(c)


def _test_curve(curve):
    assert curve.length() > 0
    assert curve.get_t(0) == 0
    assert curve.get_pos(1) == curve.get_endpoint()
    assert isinstance(curve.get_pos(0.5), P)
    assert isinstance(curve.get_vel(0.5), P)
    assert isinstance(curve.get_acc(0.5), P)

    with pytest.raises(ValueError):
        curve.get_t(-1)
        curve.get_t(curve.length())

    if isinstance(curve, NonLinearCurve):
        # Checks that the keys in the the look-up table are sorted
        keys = list(curve.LUT.keys())
        assert all(keys[i] <= keys[i + 1] for i in range(len(keys) - 1))
