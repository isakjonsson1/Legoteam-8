#!/usr/bin/env pybricks-micropython
"""Entrypoint file"""
import sys

from app.svg.parsing import parse_svg
from app.point import Point
from robot import Robot
from robot.config import DRAWING_LEN
from config import logger


def main():
    """Program entrypoint - Here comes the main logic"""
    logger.debug("Parsing SVG-file")
    paths = parse_svg("app/svg/sample_svgs/triangle.svg")

    # Debugging
    logger.debug("File fully parsed.")
    logger.debug("Finding min and max positions of the path...")

    # Finds min position of the paths
    min_x = min(path.min_position.x for path in paths)
    min_y = min(path.min_position.y for path in paths)

    # Finds max position of the paths
    max_x = max(path.max_position.x for path in paths)
    max_y = max(path.max_position.y for path in paths)

    logger.debug("Found min and max positions of the paths")
    logger.debug("The max point is ({}, {}) ".format(max_x, max_y) +
                 "and the min point is ({}, {})".format(min_x, min_y))

    logger.debug("The scale is therefore {}".format(DRAWING_LEN / max(max_x - min_x, max_y - min_y)))
    logger.debug("Initializing robot...")
    logger.debug("Check pen motor if initializing does not work")

    robot = Robot(
        scale=DRAWING_LEN / max(max_x - min_x, max_y - min_y),
        start_pos=Point(min_x, min_y),
    )

    logger.debug("Done.")
    logger.debug("Driving through paths...")

    for i, path in enumerate(paths):
        logger.debug("Driving through path {}".format(i))
        logger.run_and_time(robot.drive_through_path(path, drawing=True))

    logger.debug("All paths completed.")

def plot():
    """Used to plot example files"""
    from app.utils import plotting  # pylint: disable=import-outside-toplevel
    import matplotlib.pyplot as plt  # pylint: disable=import-outside-toplevel

    img_paths = [
        r"app\svg\sample_svgs\Mediamodifier-Design.svg",
        r"app\svg\sample_svgs\arc_test1.svg",
        r"app\svg\sample_svgs\arc_test2.svg",
        r"app\svg\sample_svgs\smiley.svg",
    ]

    names = [
        "Mediamodifier-Design.svg",
        "arc_test1.svg",
        "arc_test2.svg",
        "smiley.svg",
    ]

    svgs = [parse_svg(path) for path in img_paths]
    _, axs = plt.subplots(2, 2)
    for i, coords in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
        plot_square = axs[coords[0], coords[1]]
        for path in svgs[i]:
            plot_square.set_title(names[i])
            plotting.plot_path(path, plot_square)

    plotting.show()


def turtle():
    """Used to simulate the way the robot would drive through an svg file"""
    from turtle_sim import Turtle  # pylint: disable=import-outside-toplevel

    print("Parsing SVG-file")
    paths = parse_svg("app/svg/sample_svgs/smiley.svg")

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


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import pytest  # pylint: disable=import-outside-toplevel

        sys.exit(pytest.main(["-x", "tests"]))

    if len(sys.argv) > 1 and sys.argv[1] == "plot":
        plot()
        sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        import cProfile  # pylint: disable=import-outside-toplevel
        import os  # pylint: disable=import-outside-toplevel

        profile = cProfile.Profile()
        profile.runcall(parse_svg, "app/svg/sample_svgs/Mediamodifier-Design.svg")
        profile.dump_stats("latest.log")

        os.system("{} -m snakeviz latest.log".format(sys.executable))
        sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "turtle":
        turtle()
        input("Press enter to exit..")
        sys.exit()

    main()
