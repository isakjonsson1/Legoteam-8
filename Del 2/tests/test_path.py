"""Tests for app.svg.path"""
import math
import pytest

from app.svg import Path
from app.curves import *
from app.point import Point


points = [
    Point(0, 0),
    Point(0, 1),
    Point(1, 1),
    Point(0.75, 0),
    Point(0, -1),
    Point(1, -1),
]

curves = [
    Line(points[:2]),
    QuadraticCurve(points[:3]),
    CubicCurve(points[:4]),
    NthDegreeCurve(points),
]


def test_path_init():
    path = Path.from_curves_list(curves)
    assert len(path) == len(curves)

    assert len(Path()) == 0

    with pytest.raises(TypeError):
        Path([1, 2, 3])


def test_path_start_end():
    path = Path.from_curves_list(curves)

    assert path.start_position == points[0]
    assert path.end_position == points[-1]

    assert path.start_angle == math.pi / 2
    assert path.end_angle == 0
