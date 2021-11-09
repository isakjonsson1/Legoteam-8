#!/usr/bin/env pybricks-micropython
"""Entrypoint file"""
import cProfile
import sys

from app.svg.parsing import parse_svg
from app.utils.logging import time_function_log
from robot import Robot
from app.point import Point
from robot.config import DRAWING_LEN

# Resets the log files
with open("latest.log", "w") as f:
    pass
with open("logfile.log", "w") as f:
    pass


def main():
    """Program entrypoint - Here comes the main logic"""

    # Profiler:
    # profile = cProfile.Profile()
    # profile.runcall(parse_svg, "app/svg/sample_svgs/Mediamodifier-Design.svg")
    # profile.dump_stats("latest.log")

    # Simple timer:
    paths = time_function_log(parse_svg, "app/svg/sample_svgs/Mediamodifier-Design.svg")

    # Finds min position of the paths
    min_x = min(path.min_position.x for path in paths)
    min_y = min(path.min_position.y for path in paths)

    # Finds max position of the paths
    max_x = max(path.max_position.x for path in paths)
    max_y = max(path.max_position.y for path in paths)

    with open("logfile.log", "a") as file:
        file.write(
            "the max poitn is ({}, {}) and the min point is ({}, {})\n".format(
                max_x, max_y, min_x, min_y
            )
        )
        file.write(
            "The scale is therefore {}\n".format(
                DRAWING_LEN / max(max_x - min_x, max_y - min_y)
            )
        )

    robot = Robot(
        scale=DRAWING_LEN / max(max_x - min_x, max_y - min_y),
        start_pos=Point(min_x, min_y),
    )

    print("Driving through paths...")
    for i, path in enumerate(paths):
        print("Driving through path {}".format(i))
        robot.drive_through_path(path, drawing=True)


def plot():
    from app.utils import plotting
    import matplotlib.pyplot as plt

    img1_path = r"app\svg\sample_svgs\Mediamodifier-Design.svg"
    img2_path = r"app\svg\sample_svgs\arc_test1.svg"
    img3_path = r"app\svg\sample_svgs\arc_test2.svg"
    img4_path = r"app\svg\sample_svgs\smiley.svg"

    names = ["Mediamodifier-Design.svg", "arc_test1.svg", "arc_test2.svg", "smiley.svg"]

    path1 = parse_svg(img1_path)
    path2 = parse_svg(img2_path)
    path3 = parse_svg(img3_path)
    path4 = parse_svg(img4_path)

    svgs = [path1, path2, path3, path4]
    fig, axs = plt.subplots(2, 2)
    for i, coords in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
        plot_square = axs[coords[0], coords[1]]
        for path in svgs[i]:
            plot_square.set_title(names[i])
            plotting.plot_path(path, plot_square)

    plotting.show()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import pytest

        sys.exit(pytest.main(["-x", "tests"]))

    if len(sys.argv) > 1 and sys.argv[1] == "plot":
        plot()
        exit()

    main()
