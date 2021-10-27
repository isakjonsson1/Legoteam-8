from app.abc import NonLinearCurve
from app.point import Point


if __name__ == "__main__":
    # Test
    from Utils import plt_curve
    from Point import Point as P
    from matplotlib import pyplot as plt

    points = [P(0.25, 0), P(0, 1), P(1, 1), P(0.75, 0), P(0, -1), P(1, -1)]
    c = NthDegreeCurve(points)

    print(c.length())
    print(c.get_t(2))
    print(c.get_acc(0))

    l = Line([P(0, 0), P(1, 1)])
    print(l.get_acc(0))

    plt_curve(c)
    plt_curve(l)
    for point in c.points:
        plt.plot(point.x, point.y, marker="o")
    plt.show()
