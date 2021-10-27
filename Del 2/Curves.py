from BaseClasses import BaseCurve, BaseLUTCurve


class QuadraticCurve(BaseLUTCurve):
    def __init__(self, points, generate_LUT=True):
        """
        Creates a quadratic Bézier Curve based on three absolute points.
        """
        if len(points) != 3:
            raise ValueError("You can only generate a cubic curve from 3 points")

        self.a = points[2] - points[1]
        self.b = points[0] - points[1]

        super().__init__(points, generate_LUT=generate_LUT)

    def get_pos(self, t):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return self.points[1] + (t) ** 2 * (self.a) + (1 - t) ** 2 * (self.b)

    def get_vel(self, t):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 2 * t * self.a - 2 * (1 - t) * self.b

    def get_acc(self, t):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 2 * (self.a + self.b)

    def get_jerk(self, t):
        """Returns the jerk throughout the curve (the third order derivative)"""
        return 0


class CubicCurve(BaseLUTCurve):
    def __init__(self, points, generate_LUT=True):
        """
        Creates a cubic Bézier Curve based on four absolute points.
        """
        if len(points) != 4:
            raise ValueError("You can only generate a cubic curve from 4 points")

        self.a = points[3] - 3 * points[2] + 3 * points[1] - points[0]
        self.b = points[2] - 2 * points[1] + points[0]
        self.c = points[1] - points[0]
        self.d = points[0]

        super().__init__(points, generate_LUT=generate_LUT)

    def get_pos(self, t):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return t ** 3 * self.a + 3 * t ** 2 * self.b + 3 * t * self.c + self.d

    def get_vel(self, t):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 3 * t ** 2 * self.a + 6 * t * self.b + 3 * self.c

    def get_acc(self, t):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return 6 * t * self.a + 6 * self.b

    def get_jerk(self, t):
        """Returns the jerk throughout the curve (the third order derivative)"""
        return 6 * self.a


class NthDegreeCurve(BaseLUTCurve):
    def __init__(self, points, generate_LUT=True):
        """
        Creates a Bézier Curve in the nth degree based on n absolute points.
        Please use cubic or quadratic curves for an n less than five.
        """
        if len(points) < 4:
            raise ValueError(
                "Please use quadratic or cubic curves for curves of a degree less than 5"
            )

        # Re-assigns functions to not be reccursive if the curve is cubic
        if len(points) == 4:
            curve = CubicCurve(points, generate_LUT=False)
            self.get_pos = curve.get_pos
            self.get_vel = curve.get_vel
            self.get_acc = curve.get_acc
            self.get_jerk = curve.get_jerk
        else:
            self._subcurve0 = self.__class__(points[:-1], generate_LUT=False)
            self._subcurve1 = self.__class__(points[1:], generate_LUT=False)

        super().__init__(points, generate_LUT=generate_LUT)

    def get_pos(self, t):
        """
        Returns a position on the curve based a t value [0, 1]
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (1 - t) * self._subcurve0.get_pos(t) + t * self._subcurve1.get_pos(t)

    def get_vel(self, t):
        """
        Returns the velocity at a given t value [0, 1] (the first order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            (self._subcurve1.get_pos(t) - self._subcurve0.get_pos(t))
            + (1 - t) * self._subcurve0.get_vel(t)
            + t * self._subcurve1.get_vel(t)
        )

    def get_acc(self, t):
        """
        Returns the acceleration at a given t value [0, 1] (the second order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            2 * (self._subcurve1.get_vel(t) - self._subcurve0.get_vel(t))
            + (1 - t) * self._subcurve0.get_acc(t)
            + t * self._subcurve1.get_acc(t)
        )

    def get_jerk(self, t):
        """
        Returns the jerk at a given t value [0, 1] (the third order derivative)
        where 0 is the start of the curve and 1 is the end of the curve.
        """
        return (
            3 * (self._subcurve1.get_acc(t) - self._subcurve0.get_acc(t))
            + (1 - t) * self._subcurve0.get_jerk(t)
            + t * self._subcurve1.get_jerk(t)
        )


if __name__ == "__main__":
    # Test
    from Point import Point as P
    import numpy as np
    from matplotlib import pyplot as plt

    points = [P(0.25, 0), P(0, 1), P(1, 1), P(0.75, 0), P(0, -1), P(1, -1)]
    c = NthDegreeCurve(points)
    ts = np.linspace(0, 1)
    points = [c.get_pos(t) for t in ts]
    x = [point.x for point in points]
    y = [point.y for point in points]

    print(c.length())
    print(c.get_t(2))
    print(c.get_jerk(0))

    plt.plot(x, y)
    for point in c.points:
        plt.plot(point.x, point.y, marker="o")
    plt.show()
