import re
"""returns coordinates from an svg file"""
def coordinates_from_svg(SVG_file_name):
    with open(SVG_file_name, 'r') as file:
        text = file.read().replace('\n', '')
    file.close()

    #match paths
    pattern = re.compile(r'((\bd=\")(.*)(?=\"))')
    pattern_match = pattern.search(text)

    betterSelection = (pattern_match.group()).split('\"') 
    group = [] 

    for i in range(len(betterSelection) - 1):
        if betterSelection[i + 1][0] == 'm' or betterSelection[i + 1][0] =='M':
            group.append(betterSelection[i + 1])

    coordinates = []
    for i in group:
        coordinates.append(re.split('([cClLmMsS])', i))

    #removes first element if empty
    for k in range(len(coordinates)):
        del coordinates[k][0]
        for l in range(len(coordinates[k])):
                coordinates[k][l]=(coordinates[k][l]).strip()
                
    return coordinates

