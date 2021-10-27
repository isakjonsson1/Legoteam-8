from app.curves import Line
from app.curves import NthDegreeCurve
from app.point import Point as P

def test_line():
    points = [
        P(0, 0),
        P(1, 1)
    ]
    l = Line(points)
    assert l.length() == 2**0.5
    assert l.get_t(1) == 1 / l.length()
    assert l.get_t(2) == 2 / l.length()

def test_nth_degree_curve():
    points = [
        P(0.25, 0),
        P(0, 1),
        P(1, 1),
        P(0.75, 0),
        P(0, -1),
        P(1, -1)
    ]
    c = NthDegreeCurve(points)
    # More testing