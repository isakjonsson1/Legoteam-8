"""Utility functions for plotting"""
from matplotlib import pyplot as plt
import numpy as np


def plot_path(path):
    """Plot a given path"""
    for curve in path:
        plot_curve(curve)


def plot_curve(curve):
    """Plots a given curve"""
    t_values = np.linspace(0, 1)
    points = [curve.get_pos(t) for t in t_values]

    x = [p.x for p in points]
    y = [p.y for p in points]
    plt.plot(x, y)


def plot_point(point):
    """Plots a point"""
    plt.plot(point.x, point.y, marker="o")


def show():
    """Reveals all drawn plots by calling mathplotlib.pyplot.show()"""
    plt.show()
