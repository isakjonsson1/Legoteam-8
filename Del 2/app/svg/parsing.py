"""functions related to parsing a .svg file"""
import re

from app.abc import Curve
from app.point import Point
from app.svg import Path


def parse_svg(svg_file_name):
    """Parses an svg file and returns a list of paths in the svg"""
    instructions, inputs = _commands_from_svg(svg_file_name)
    return _commands_to_paths(instructions, inputs)


def _commands_from_svg(svg_file_name):
    """
    Returns a list of commands and command inputs form an svg file.

    Ex: ['M', '16-0.034', 'C', '7.1-0-0.03,7.1-0.03,16',
    'S', '7.1,32.03,16,32.03']
    """
    with open(svg_file_name, "r", encoding="utf-8") as file:
        text = file.read().replace("\n", "")
    file.close()

    # match paths
    regex = r"(?<=\bd=\").*?(?=\")"
    matches = re.findall(regex, text)

    # Slits at every command-letter (command-letter is retained)
    paths = []

    # Separates the data based on instructions.
    # Lower case means relative instructions, while uppercase means absolute
    # [M, m, Z, z]: Move to and close path
    # [C, c, S, s]: Cubic bezier curves
    # [Q, q, T, t]: Quadratic bezier curves
    # [L, l, H, h, V, v]: Lines
    # [A, a]: Eliptical arcs
    # https://www.w3.org/TR/SVG/paths.html#PathData
    for match in matches:
        paths.append(re.split("([cCsSqQtTlLaAvVhHmMzZ])", match))

    # Removes first element of every list of command chain (path) (it's empty)
    # Removes whitespace from command
    # Flattens the list
    flat = [cmd.strip() for path in paths for cmd in path[1:]]

    # Splits into instructions and inputs
    instructions = list(flat[::2])
    inputs = list(flat[1::2])
    return instructions, inputs


def _commands_to_paths(instuctions, inputs):
    # assert that the first instruction is a moveto
    if instuctions[0].lower() != "m":
        raise ValueError("The first instruction needs to be a moveto")

    # Inizialize path
    inp = _parse_command_input(inputs[0])
    path = Path(Point(inp[0], -inp[1]))

    movement = {
        "m",
        "z",
    }

    curves_dict = {
        "c": extract_points(3),
        "q": extract_points(2),
        "l": extract_points(1),
        "s": extract_smooth_points(2),
        "t": extract_smooth_points(1),
    }

    not_implemented = {
        "a",
        "h",
        "v",
    }

    paths = []
    for command, raw_input in zip(instuctions, inputs):
        cmd_letter = command.lower()
        relative = cmd_letter == command

        # Close path
        if cmd_letter == "z":
            paths.append(path)
            path = Path(path.start_position)
            continue

        # Command input
        inp = _parse_command_input(raw_input)

        # Move to
        if cmd_letter in movement:
            if len(path) != 0:
                paths.append(path)
            start_point = Point(inp[0], -inp[1])
            if relative:
                start_point += path.end_position
            path = Path(start_point)

        # Bezier curve
        elif cmd_letter in curves_dict:
            points_gen = curves_dict[cmd_letter]
            for points in points_gen(inp, path, relative):
                path.append_curve(points)

        # Not implemented
        elif cmd_letter in not_implemented:
            raise NotImplementedError(f"Instruction not implemented ['{command}']")

        # Not recognized
        else:
            raise ValueError(f"Instruction not recognized ['{command}']")

    return paths


def extract_points(number_of_points):
    """
    Returns a generator for the points needed to construct a bezier curve.
    The start position is always implicitly defined as the endposition as
    the previous curve, so for any nth degree bezier curve, number_of_points
    should be n.
    """
    if number_of_points < 1:
        ValueError("Number of points per curve must be equal or greater than 1")

    def generator(inp, path, relative):
        """
        Returns points needed to construct a curve.

        --Params--
        :param inp: A list of input numbers that gets turned into points.
        :param path: The current path that the curve edventually get appended to
        :param relative: Bool variable to signify that the points are meant to be
                         interpereted relatively.
        """
        # Start is the end_position of the previous curve
        start = path.end_position

        # A point consists of two numbers
        num_count = number_of_points * 2

        # If there are 12 numbers and the curve is defiend by 3 points,
        # The first i is 0 and the second i is 6. This makes is easy to
        # fetch any number of points at the same time. Each loop is a new
        # curve
        for i in range(0, len(inp), num_count):
            # The points for this curve
            points = [Point(inp[j], -inp[j + 1]) for j in range(i, i + num_count, 2)]

            # adds start point and updates it if relative
            if relative:
                points = [point + start for point in points]
                start = points[-1]

            yield points

    return generator


def extract_smooth_points(number_of_points):
    """
    Returns a generator for the points needed to construct a bezier curve.

    For a smooth curve, the first control point in this generator is implicitly
    defined as the reflection of the last control point, so the first control point
    should not be explicitly given.

    The start position is always implicitly defined as the endposition as
    the previous curve, so for any nth degree bezier curve, number_of_points
    should be n - 1.
    """
    # To be used to extract the explicit points
    _extract_points = extract_points(number_of_points)

    def generator(inp, path, relative):
        """
        Returns points needed to construct a curve.

        --Params--
        :param inp: A list of input numbers that gets turned into points.
        :param path: The current path that the curve edventually get appended to
        :param relative: Bool variable to signify that the points are meant to be
                         interpereted relatively.
        """
        # Gets the explicitly given points
        explicit_points_generator = _extract_points(inp, path, relative)

        start = path.end_position

        # Last curve was not a bezier curve of the same order as this one
        if number_of_points != len(path[-1].points) - 2 or not isinstance(
            path[-1], Curve
        ):
            ctr_point = start
        else:
            ctr_point = 2 * start - path[-1].points[2]

        for exp_points in explicit_points_generator:
            yield [ctr_point] + exp_points

            # Updates the control point
            ctr_point = 2 * exp_points[-1] - exp_points[-2]

    return generator


def _parse_command_input(command_input):
    # Finds a number
    pattern = r"\-?\.?(?:(?:(?<=\.)\d+)|(?:(?<!\.)\d+(?:\.?\d+)?))"
    result = re.findall(pattern, command_input)
    return [float(num) for num in result]
