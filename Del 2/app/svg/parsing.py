"""functions related to parsing a .svg file"""
import re
from itertools import chain


def commands_from_svg(SVG_file_name):
    """
    Returns a list of commands and command inputs form an svg file.

    Ex: ['M', '16-0.034', 'C', '7.1-0-0.03,7.1-0.03,16',
    'S', '7.1,32.03,16,32.03']
    """
    with open(SVG_file_name, "r") as file:
        text = file.read().replace("\n", "")
    file.close()

    # match paths
    regex = r"(?<=\bd=\").*?(?=\")"
    matches = re.findall(regex, text)

    # Slits at every command-letter (command-letter is retained)
    commands = []
    for match in matches:
        commands.append(re.split("([cClLmMsS])", match))

    # Removes first element of every list of command chain (it's empty)
    for k in range(len(commands)):
        del commands[k][0]
        for l in range(len(commands[k])):
            commands[k][l] = (commands[k][l]).strip()

    # Flatten commands and returns
    return chain.from_iterable(commands)
