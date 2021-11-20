#!/usr/bin/env pybricks-micropython
"""Entrypoint file"""
import sys
import re

from app.svg.parsing import parse_svg
from app.point import Point
from robot import Robot
from robot.config import DRAWING_LEN

SAMPLE_SVGS = "app/svg/sample_svgs/"


def main():
    """Program entrypoint - Here comes the main logic"""

    print("Parsing SVG-file")
    paths = parse_svg(SAMPLE_SVGS + "triangle.svg")

    # Debugging
    print("File fully parsed.")
    print("Finding min and max positions of the path...")

    # Finds min position of the paths
    min_x = min(path.min_position.x for path in paths)
    min_y = min(path.min_position.y for path in paths)

    # Finds max position of the paths
    max_x = max(path.max_position.x for path in paths)
    max_y = max(path.max_position.y for path in paths)

    print("Found min and max positions of the paths")
    print(
        "The max point is ({}, {}) ".format(max_x, max_y)
        + "and the min point is ({}, {})".format(min_x, min_y)
    )

    print(
        "The scale is: {:.3f}".format(DRAWING_LEN / max(max_x - min_x, max_y - min_y))
    )

    print("Initializing robot...")
    print("Check pen motor if initializing does not work")
    robot = Robot(
        scale=DRAWING_LEN / max(max_x - min_x, max_y - min_y),
        start_pos=Point(min_x, min_y),
    )
    print("Done.")

    print("Driving through paths...")
    for i, path in enumerate(paths):
        print("Driving through path {}".format(i))
        robot.drive_through_path(path, drawing=True)

    print("All paths completed.")


def plot(
    file_paths=(
        SAMPLE_SVGS + "Mediamodifier-Design.svg",
        SAMPLE_SVGS + "arc_test1.svg",
        SAMPLE_SVGS + "arc_test2.svg",
        SAMPLE_SVGS + "smiley.svg",
    )
):
    """
    Used to plot svg files using the matplotlib library.

    The files can be manually specified by passing the path (relative or absolute)
    """
    from app.utils import plotting  # pylint: disable=import-outside-toplevel
    import matplotlib.pyplot as plt  # pylint: disable=import-outside-toplevel

    if len(file_paths) > 4:
        print("Warning: This application only supports 4 plots at a time (max)")

    plot_names = [
        re.search(r"(?:\\|\/)([^\\\/]*)\.svg$", file_path).group(1)
        for file_path in file_paths
    ]

    svgs = [parse_svg(path) for path in file_paths[:4]]

    _, axs = plt.subplots(2, 2)
    for i, coords in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
        plot_square = axs[coords[0], coords[1]]
        try:
            for path in svgs[i]:
                plot_square.set_title(plot_names[i])
                plotting.plot_path(path, plot_square)
        except IndexError:
            # Less than 4 plots
            break

    plotting.show()


def turtle(file_path=SAMPLE_SVGS + "smiley.svg"):
    """
    Used to simulate the way the robot would drive through
    an svg file using the turtle library

    The file can be manually specified by passing the path (relative or absolute)
    """
    from turtle_sim import Turtle  # pylint: disable=import-outside-toplevel

    print("Parsing SVG-file")
    paths = parse_svg(file_path)

    # Debugging
    print("File fully parsed.")
    print("Finding min and max positions of the path...")

    # Finds min position of the paths
    min_x = min(path.min_position.x for path in paths)
    min_y = min(path.min_position.y for path in paths)

    # Finds max position of the paths
    max_x = max(path.max_position.x for path in paths)
    max_y = max(path.max_position.y for path in paths)

    print("Found min and max positions of the paths")
    print("Initializing robot...")
    turtle_drivebase = Turtle()
    robot = Robot(
        scale=DRAWING_LEN / max(max_x - min_x, max_y - min_y),
        start_pos=Point(min_x, min_y),
        _drive_base=turtle_drivebase,
        _pen_motor=None,
    )
    print("Done.")
    print("Driving through paths...")

    for i, path in enumerate(paths):
        print("Driving through path {}".format(i))
        robot.drive_through_path(path, drawing=True)

    print("All paths completed.")


def profile(file_path=SAMPLE_SVGS + "Mediamodifier-Design.svg"):
    """
    Used to profile the parse_svg function on an svg file using cProfile and snakeviz.

    The file can be manually by passing the path (relative or absolute)
    """
    import cProfile  # pylint: disable=import-outside-toplevel
    import os  # pylint: disable=import-outside-toplevel

    profiler = cProfile.Profile()
    profiler.runcall(parse_svg, file_path)
    profiler.dump_stats("latest.log")

    os.system('"{}" -m snakeviz latest.log'.format(sys.executable))


def test():
    """
    Used to run the tests

    Returns an exit code
    """
    import pytest  # pylint: disable=import-outside-toplevel

    return pytest.main(["-x", "tests"])


def help(func_name=None):  # pylint: disable=redefined-builtin
    """
    Used to relay information about the different CLI commands
    to the user.
    """
    funcs = [plot, turtle, profile, test, help]
    if func_name is None:
        for func in funcs:
            print("\n{}: {}".format(func.__name__, func.__doc__))
        return

    for func in funcs:
        if func_name == func.__name__:
            print("\n{}: {}".format(func.__name__, func.__doc__))
            return

    print("The command {} does not exist".format(func_name))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.exit(test())

    if len(sys.argv) > 1 and sys.argv[1] == "plot":
        try:
            if len(sys.argv) > 2:
                plot(file_paths=sys.argv[2:])
            else:
                plot()
        except FileNotFoundError as e:
            print(e)
        sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        try:
            if len(sys.argv) > 2:
                profile(file_path=sys.argv[2])
            else:
                profile()
        except FileNotFoundError as e:
            print(e)
        sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "turtle":
        try:
            if len(sys.argv) > 2:
                turtle(file_path=sys.argv[2])
            else:
                turtle()
            input("Press enter to exit..")
        except FileNotFoundError as e:
            print(e)
        sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "help":
        if len(sys.argv) > 2:
            help(func_name=sys.argv[2])
        else:
            help()
        sys.exit()

    main()
