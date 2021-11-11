"""functions related to parsing a .svg file"""
import re

from app.abc import Curve
from app.arc.arc import Arc
from app.point import Point
from app.svg import Path
from robot.config import logger


@logger.time()
def parse_svg(svg_file_name):
    """Parses an svg file and returns a list of paths in the svg"""
    instructions, inputs = _commands_from_svg(svg_file_name)
    if len(instructions) == 0:
        return [Path()]

    return _commands_to_paths(instructions, inputs)


@logger.time()
def _commands_from_svg(svg_file_name):
    """
    Returns a list of instructions and a list of inputs form an svg file.

    Ex: ['M', '16-0.034', 'C', '7.1-0-0.03,7.1-0.03,16',
    'S', '7.1,32.03,16,32.03']
    """
    with open(svg_file_name, "r", encoding="utf-8") as file:
        text = file.read().replace("\n", "")

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


@logger.time()
def _commands_to_paths(  # pylint: disable=too-many-locals, too-many-branches
    instuctions, inputs
):
    # assert that the first instruction is a moveto
    if instuctions[0].lower() != "m":
        raise ValueError("The first instruction needs to be a moveto")

    movement = {
        "m",
        "z",
    }

    extract_dict = {
        "c": extract_points(3),
        "q": extract_points(2),
        "l": extract_points(1),
        "s": extract_smooth_points(2),
        "t": extract_smooth_points(1),
        "a": extract_arc_data,
    }

    not_implemented = {
        "h",
        "v",
    }

    path = Path()
    paths = []
    for command, raw_input in zip(instuctions, inputs):
        cmd_letter = command.lower()
        relative = cmd_letter == command
        inp = _parse_command_input(raw_input)

        if cmd_letter in movement:
            # Close path
            if cmd_letter == "z":
                # Line to start
                path.append_curve([path.start_position])
                start_point = path.start_position

            # Move to
            elif cmd_letter == "m":
                start_point = Point(inp[0], -inp[1])
                # implicit lineto
                if len(inp) > 2:
                    cmd_letter = "l"
                    inp = inp[2:]

            if len(path) != 0:
                paths.append(path)

            # Starts new subpath
            path = Path(start_point)

            # No implicit lineto
            if cmd_letter in movement:
                continue

        # Curve
        if cmd_letter in extract_dict:
            points_gen = extract_dict[cmd_letter]

            # Eliptic arc
            if cmd_letter == "a":
                for data in points_gen(inp, path, relative):
                    path.append(Arc(*data))
                continue

            # Bezier
            for points in points_gen(inp, path, relative):
                path.append_curve(points)

            continue

        # Not implemented
        if cmd_letter in not_implemented:
            raise NotImplementedError(
                "Instruction not implemented ['{}']".format(command)
            )

        # Not recognized
        raise ValueError("Instruction not recognized ['{}']".format(command))

    if len(path) != 0:
        paths.append(path)

    return paths


@logger.time()
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


@logger.time()
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


@logger.time()
def extract_arc_data(inp, path, relative):
    """Returns the arc data needed to construct an eliptic arc

    --Params--
    :param inp: A list of input numbers that gets turned into points.
    :param path: The current path that the curve edventually get appended to
    :param relative: Bool variable to signify that the points are meant to be
                     interpereted relatively.
    """
    start_pos = path.end_position
    for i in range(0, len(inp), 7):
        radii = Point(inp[i], inp[i + 1])
        rotation = inp[i + 2]
        large_arc = inp[i + 3]
        sweep = inp[i + 4]
        end_pos = Point(inp[i + 5], -inp[i + 6])
        if relative:
            end_pos += start_pos

        points = [start_pos, radii, end_pos]
        yield points, large_arc, sweep, rotation

        start_pos = end_pos


@logger.time()
def _parse_command_input(command_input):
    """Parses command inputs and returns a list of floats"""
    # Finds a number
    pattern = r"\-?\.?(?:(?:(?<=\.)\d+(?:e\d+)?)|(?:(?<!\.)\d+(?:\.?\d+(?:e\-?\d+)?)?))" # wtf?
    result = re.findall(pattern, command_input)

    if len(result) == 0:
        return []

    return [float(num) for num in result]
