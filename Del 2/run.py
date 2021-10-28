"""Entrypoint file"""
import sys

from matplotlib import pyplot as plt

# from config import *
from app.point import Point as P
from app.curves import Line
from app.curves import NthDegreeCurve
from app.utils.plotting import plot_curve


def main():
    """Program entrypoint - Here comes the main logic"""
    points = [P(0.25, 0), P(0, 1), P(1, 1), P(0.75, 0), P(0, -1), P(1, -1)]
    curve = NthDegreeCurve(points)

    print(curve.length())
    print(curve.get_t(2))
    print(curve.get_acc(0))

    line = Line([P(0, 0), P(1, 1)])
    print(line.get_acc(0))

    plot_curve(curve)
    plot_curve(line)
    for point in curve.points:
        plt.plot(point.x, point.y, marker="o")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import pytest

        sys.exit(pytest.main(["-x", "tests"]))

    main()
