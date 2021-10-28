"""Used to test different classes and methods"""
import math
import pytest

from app.abc.non_linear_curve import NonLinearCurve
from app.curves import Line
from app.curves import QuadraticCurve
from app.curves import NthDegreeCurve
from app.curves.cubic_curve import CubicCurve
from app.point import Point

points = [
    Point(0, 0),
    Point(0, 1),
    Point(1, 1),
    Point(0.75, 0),
    Point(0, -1),
    Point(1, -1),
]


def test_line():
    """Tests the Line class"""
    l = Line(points[:2])
    assert l.length() == 1
    assert l.get_t(0.5) == 0.5 / l.length()

    with pytest.raises(ValueError):
        l.get_t(2)
        l.get_t(-1)

    _test_curve(l)


def test_quadratic_curve():
    """Tests the QuadraticCurve class"""
    c = QuadraticCurve(points[:3])

    with pytest.raises(ValueError):
        QuadraticCurve(points[:2])
        QuadraticCurve(points[:4])

    _test_curve(c)


def test_quadratic_curve():
    """Tests the CubicCurve class"""
    c = CubicCurve(points[:4])

    with pytest.raises(ValueError):
        CubicCurve(points[:3])
        QuadraticCurve(points[:5])

    _test_curve(c)


def test_nth_degree_curve():
    """Tests the NthDegreeCurve class"""
    c = NthDegreeCurve(points)

    with pytest.raises(ValueError):
        NthDegreeCurve(points[:3])

    _test_curve(c)


def _test_curve(curve):
    """Tests any curve"""
    assert curve.length() > 0
    assert curve.get_t(0) == 0
    assert curve.get_pos(1) == curve.get_end_pos()
    assert curve.get_start_angle() == math.pi / 2

    assert isinstance(curve.get_pos(0.5), Point)
    assert isinstance(curve.get_vel(0.5), Point)
    assert isinstance(curve.get_acc(0.5), Point)

    with pytest.raises(ValueError):
        curve.get_t(-1)
        curve.get_t(curve.length())

    if isinstance(curve, NonLinearCurve):
        # Checks that the keys in the the look-up table are sorted
        keys = list(curve.look_up_table.keys())
        assert all(keys[i] <= keys[i + 1] for i in range(len(keys) - 1))
