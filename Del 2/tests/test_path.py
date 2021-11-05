"""Tests for app.svg.path"""
import math
from matplotlib.pyplot import plot
import pytest

from app.svg import Path
from app.curves import *
from app.arc import Arc
from app.point import Point
from app.utils import plotting


points = [
    Point(0, 0),
    Point(0, 1),
    Point(1, 1),
    Point(0.75, 0),
]

curves = [
    Line(points[:2]),
    QuadraticCurve(points[:3]),
    Arc([points[0], Point(1, 2), points[-1]], large_arc=False, sweep=False),
    CubicCurve(points[:4]),
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
    assert path.end_angle == math.atan2(-1, -0.25)

    plotting.plot_path(path)
    plotting.show()
