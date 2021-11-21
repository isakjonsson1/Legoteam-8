"""Utility functions for plotting"""
from matplotlib import pyplot as plt
import numpy as np


def plot_path(path, plot_obj=plt):
    """Plot a given path"""
    for curve in path:
        plot_curve(curve, plot_obj)


def plot_curve(curve, plot_obj=plt):
    """Plots a given curve"""
    t_values = np.linspace(0, 1)
    points = [curve.get_pos(t) for t in t_values]

    x = [p.x for p in points]
    y = [p.y for p in points]
    plot_obj.plot(x, y)


def plot_point(point, plot_obj=plt):
    """Plots a point"""
    plot_obj.plot(point.x, point.y, marker="o")


def show():
    """Reveals all drawn plots by calling mathplotlib.pyplot.show()"""
    plt.show()
