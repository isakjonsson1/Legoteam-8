"""functions related to parsing a .svg file"""
import re
from itertools import chain

from app.abc import Curve
from app.point import Point
from app.svg import Path


def parse_svg(svg_file_name):
    commands = _commands_from_svg(svg_file_name)
    return _commands_to_paths(commands)


def _commands_from_svg(svg_file_name):
    """
    Returns a list of commands and command inputs form an svg file.

    Ex: ['M', '16-0.034', 'C', '7.1-0-0.03,7.1-0.03,16',
    'S', '7.1,32.03,16,32.03']
    """
    with open(svg_file_name, "r") as file:
        text = file.read().replace("\n", "")
    file.close()

    # match paths
    regex = r"(?<=\bd=\").*?(?=\")"
    matches = re.findall(regex, text)

    # Slits at every command-letter (command-letter is retained)
    commands = []

    # Separates the data based on instructions.
    # Lower case means relative instructions, while uppercase means absolute
    # [M, m, Z, z]: Move to and close path
    # [C, c, S, s]: Cubic bezier curves
    # [Q, q, T, t]: Quadratic bezier curves
    # [L, l, H, h, V, v]: Lines
    # [A, a]: Eliptical arcs
    # https://www.w3.org/TR/SVG/paths.html#PathData
    for match in matches:
        commands.append(re.split("([cCsSqQtTlLaAvVhHmMzZ])", match))

    # Removes first element of every list of command chain (it's empty)
    for k in range(len(commands)):
        del commands[k][0]
        for l in range(len(commands[k])):
            commands[k][l] = (commands[k][l]).strip()

    # Flatten commands and returns
    return list(chain.from_iterable(commands))


def _commands_to_paths(commands):
    # Inizialize path
    inp = _parse_command_input(commands[1])
    path = Path(Point(inp[0], -inp[1]))

    paths = []
    for i in range(2, len(commands), 2):
        cmd_letter = commands[i].lower()
        relative = cmd_letter == commands[i]

        # Close path
        if cmd_letter == "z":
            paths.append(path)
            path = Path(path.start_position)
            continue

        # Command input
        inp = _parse_command_input(commands[i + 1])

        # Move to
        if cmd_letter == "m":
            if len(path) != 0:
                paths.append(path)
            start_point = Point(inp[0], -inp[1])
            if relative:
                start_point += path.end_position
            path = Path(start_point)

        # Cubic bezier
        elif cmd_letter == "c":
            for j in range(0, len(inp), 6):
                points = [Point(inp[k], -inp[k + 1]) for k in range(j, j + 6, 2)]
                path.append_curve(points, relative=relative)

        # "Smooth" cubic bezier
        elif cmd_letter == "s":

            # If last curve was a cubic bezier curve
            if commands[i - 2].lower() in ("c", "s"):
                # Sets first control point
                abs_ctr_point = 2 * path.end_position - path[-1].points[2]
            else:
                # Control point is starting point
                abs_ctr_point = path.end_position

            # Loops through command input one curve at a time
            for j in range(0, len(inp), 4):
                # Convert command input to points
                inp_points = [Point(inp[k], -inp[k + 1]) for k in range(j, j + 4, 2)]

                # Converts to absulute points if input is relative
                if relative:
                    inp_points = Curve.convert_rel_points_to_abs_points(
                        path.end_position, inp_points
                    )[1:]

                # Append points to curve
                path.append_curve([abs_ctr_point] + inp_points)

                # Updates control point
                abs_ctr_point = 2 * path.end_position - path[-1].points[2]

        # Quadratic bezier
        elif cmd_letter == "q":
            for j in range(0, len(inp), 4):
                points = [Point(inp[k], -inp[k + 1]) for k in range(j, j + 4, 2)]
                path.append_curve(points, relative=relative)

        # "Smooth" quadratic bezier
        elif cmd_letter == "t":
            # If last curve was a quadratic bezier curve
            if commands[i - 2].lower() in ("q", "t"):
                # Sets first control point
                abs_ctr_point = 2 * path.end_position - path[-1].points[2]
            else:
                # Control point is starting point
                abs_ctr_point = path.end_position

            # Loops through command input one curve at a time
            for j in range(0, len(inp), 2):
                # Convert command input to points
                inp_point = Point(inp[j], -inp[j + 1])

                # Converts to absulute points if input is relative
                if relative:
                    inp_point += path.end_position

                # Append points to curve
                path.append_curve([abs_ctr_point, inp_point])

                # Updates control point
                abs_ctr_point = 2 * path.end_position - path[-1].points[2]

        # Line
        elif cmd_letter == "l":
            for j in range(0, len(inp), 2):
                point = Point(inp[j], -inp[j + 1])
                path.append_curve([point], relative=relative)

        # Not implemented
        elif cmd_letter in ("h", "v", "a"):
            raise NotImplementedError(f"Instruction not implemented ['{commands[i]}']")

        # Not regognized
        else:
            raise ValueError(f"Instruction not recognized ['{commands[i]}']")

    return paths


# def extract_curve_points(number_of_points):
#     if number_of_points >= 1:
#         ValueError("Number of points per curve must be equal or greater than 1")

#     def generator(inp):
#         for i in range(0, len(inp), number_of_points * 2):
#             yield [Point(inp[i], inp[i + 1]) for k in range(i, i + 6, 2)]


def _parse_command_input(command_input):
    # Finds a number
    pattern = r"\-?\.?(?:(?:(?<=\.)\d+)|(?:(?<!\.)\d+(?:\.?\d+)?))"
    result = re.findall(pattern, command_input)
    return [float(num) for num in result]
