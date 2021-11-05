"""Entrypoint file"""
import sys

from matplotlib import pyplot as plt

# from config import *
from app.point import Point
from app.curves import Line
from app.svg.parsing import parse_svg
from app.utils.plotting import plot_curve, plot_path
from app.svg import Path


def main():
    paths = parse_svg(r"app\svg\sample_svgs\arc_test.svg")
    print(len(paths))
    for path in paths:
        plot_path(path)
    plt.show()

    # path = Path(Point(0, 3))

    # print(Point.from_list([1, 2]))

    # path.append_curve([Point(0, 1), Point(2, 3), Point(1, 3)])
    # path.append_curve([Point(2, 3), Point(3, 5), Point(3, 3)])
    # path.append_curve([Point(1, 1)])
    # plot_path(path)
    # plt.show()

    # """Program entrypoint - Here comes the main logic"""
    # points = [P(0.25, 0), P(0, 1), P(1, 1), P(0.75, 0), P(0, -1), P(1, -1)]
    # curve = NthDegreeCurve(points)

    # print(curve.length())
    # print(curve.get_t(2))
    # print(curve.get_acc(0))

    # line = Line([P(0, 0), P(1, 1)])
    # print(line.get_acc(0))

    # plot_curve(curve)
    # plot_curve(line)
    # for point in curve.points:
    #     plt.plot(point.x, point.y, marker="o")
    # plt.show()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import pytest

        sys.exit(pytest.main(["-x", "tests"]))

    main()
