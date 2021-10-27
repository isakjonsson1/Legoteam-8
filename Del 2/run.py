from matplotlib import pyplot as plt

from config import *
from app.point import Point as P
from app.curves import Line
from app.curves import NthDegreeCurve
from app.utils.plotting import plot_curve

import sys

def main():
    points = [P(0.25, 0), P(0, 1), P(1, 1), P(0.75, 0), P(0, -1), P(1, -1)]
    c = NthDegreeCurve(points)

    print(c.length())
    print(c.get_t(2))
    print(c.get_acc(0))

    l = Line([P(0, 0), P(1, 1)])
    print(l.get_acc(0))

    plot_curve(c)
    plot_curve(l)
    for point in c.points:
        plt.plot(point.x, point.y, marker="o")
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        import pytest
        sys.exit(pytest.main(['-x', 'tests']))

    main()