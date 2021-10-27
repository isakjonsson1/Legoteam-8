from matplotlib import pyplot as plt
import numpy as np


def plot_curve(curve):
    ts = np.linspace(0, 1)
    points = [curve.get_pos(t) for t in ts]
    x = [p.x for p in points]
    y = [p.y for p in points]

    plt.plot(x, y)
