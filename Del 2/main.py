#!/usr/bin/env pybricks-micropython
"""Entrypoint file"""
import sys

from app.svg.parsing import parse_svg
from app.point import Point
from robot import Robot
from robot.config import DRAWING_LEN


def main():
    """Program entrypoint - Here comes the main logic"""
    print("Parsing SVG-file")
    paths = parse_svg("app/svg/sample_svgs/triangle.svg")

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
    # with open("logfile.log", "a", encoding="utf-8") as file:
    #     file.write(
    #         "the max point is ({}, {}) and the min point is ({}, {})\n".format(
    #             max_x, max_y, min_x, min_y
    #         )
    #     )
    #     file.write(
    #         "The scale is therefore {}\n".format(
    #             DRAWING_LEN / max(max_x - min_x, max_y - min_y)
    #         )
    #     )

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


def plot(file_names=("Mediamodifier-Design", "arc_test1", "arc_test2", "smiley")):
    """
    Used to plot svg files using the matplotlib library.

    Filenames can be specified to indicate what files you want plotted.
    """
    from app.utils import plotting  # pylint: disable=import-outside-toplevel
    import matplotlib.pyplot as plt  # pylint: disable=import-outside-toplevel

    if len(file_names) > 4:
        print("Warning: This application only supports 4 plots at a time (max)")

    img_paths = [
        "app/svg/sample_svgs/{}.svg".format(file_name) for file_name in file_names
    ]
    names = [file_name + ".svg" for file_name in file_names]
    svgs = [parse_svg(path) for path in img_paths[:4]]

    _, axs = plt.subplots(2, 2)
    for i, coords in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
        plot_square = axs[coords[0], coords[1]]
        for path in svgs[i]:
            plot_square.set_title(names[i])
            plotting.plot_path(path, plot_square)

    plotting.show()


def turtle(file_name="smiley"):
    """
    Used to simulate the way the robot would drive through
    an svg file using the turtle library

    A filename can be given to specify which file in the svg/sample_svgs
    you want to simulate
    """
    from turtle_sim import Turtle  # pylint: disable=import-outside-toplevel

    print("Parsing SVG-file")
    paths = parse_svg("app/svg/sample_svgs/{}.svg".format(file_name))

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


def profile(file_name="Mediamodifier-Design"):
    """
    Used to profile the parse_svg function on an svg file using cProfile and snakeviz.

    The file can be manually specified.
    """
    import cProfile  # pylint: disable=import-outside-toplevel
    import os  # pylint: disable=import-outside-toplevel

    profiler = cProfile.Profile()
    profiler.runcall(parse_svg, "app/svg/sample_svgs/{}.svg".format(file_name))
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
                plot(file_names=sys.argv[2:])
            else:
                plot()
        except FileNotFoundError as e:
            print(e)
        finally:
            sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        try:
            if len(sys.argv) > 2:
                profile(file_name=sys.argv[2])
            else:
                profile()
        except FileNotFoundError as e:
            print(e)
        finally:
            sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "turtle":
        try:
            if len(sys.argv) > 2:
                turtle(file_name=sys.argv[2])
            else:
                turtle()
            input("Press enter to exit..")
        except FileNotFoundError as e:
            print(e)
        finally:
            sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "help":
        if len(sys.argv) > 2:
            help(func_name=sys.argv[2])
        else:
            help()
        sys.exit()

    main()
