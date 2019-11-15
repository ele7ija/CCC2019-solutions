# Generic/Built-in Libs
import sys, getopt, os
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

# Other imports
from model import *

# Globals
ROWS, COLS, K = 0, 0, 0
INPUT_F = None

def _get_inputfilepath(argv):
    """Parses the command-line arguments. Returns the output file path."""
    global INPUT_F

    inputfilepath = None
    outputfilepath = None
    try:
        opts, args = getopt.getopt(argv,"i:o:h")
    except getopt.GetoptError:
        print('Usage: example.py -i <inputfilepath> -o <outputfilepath> -h')
        sys.exit(2)
    found = False
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: example.py -i <inputfilepath> -o <outputfilepath>')
            sys.exit()
        elif opt == '-i':
            inputfilepath = arg
            INPUT_F = inputfilepath
            found = True
        elif opt == '-o':
            outputfilepath = arg
    if not found:
        print('ERROR.')
        print('Usage: example.py -i <inputfilepath> -o <outputfilepath> -h')
        sys.exit()

    return inputfilepath, outputfilepath


def read_file(filename):
    f = open(filename, 'r')
    return f.read()


def write_to_file(filename, content):
    f = open(filename, 'w')
    f.write(content)

def _parse_solars(icparsed):
    global K

    solar_panels = []
    # first index: 1
    # last index: k*2
    for i in range(1, K*2+1, 2):
        s = Solar(country=icparsed[i], price=icparsed[i+1])
        solar_panels.append(s)
    return solar_panels

def _parse_matrix(icparsed):
    global ROWS, COLS, K
    matrix = Matrix()

    index = 1 + K*2 + 2
    for i in range(COLS):
        column = []
        for j in range(ROWS):
            column.append(Cell(
                x=j, 
                y=i, 
                altitude=icparsed[index], 
                country=icparsed[index+1]))
            index += 2
        matrix.append(column)
    return matrix 


def _visualize(capitals, neighbours):
    fig, ax = plt.subplots()
    ax.grid(which='major', axis='both')
    plt.xlim(0, ROWS-1)
    plt.ylim(0, COLS-1)

    plotted = set()
    for capital in capitals:
        plt.scatter(capital.x, capital.y, color='r')
        plt.text(capital.x, capital.y, "Country:" + str(capital.country))
        for neighbour in neighbours[capital.country]:
            n_capital = capitals[neighbour]
            # plot again
            plt.plot([capital.x, n_capital.x], [capital.y, n_capital.y], color='b')
            # plot distance
            x_avg, y_avg = (capital.x + n_capital.x) / 2, (capital.y + n_capital.y) / 2 
            plt.text(x_avg, y_avg, euclidean_distance(capital.x, capital.y, n_capital.x, n_capital.y))
            plotted.add(neighbour)
    plt.title('input: \'' + INPUT_F + '\'')

    if not os.path.exists('./viz'):
        os.mkdir('./viz')
    plt.savefig('./viz/' + INPUT_F + '.png')


def solution(i_content):
    global ROWS, COLS, K

    icparsed = [int(x) for x in i_content.split()]
    K = icparsed[0]
    solar_panels = _parse_solars(icparsed)

    ROWS, COLS = icparsed[K*2+1], icparsed[K*2+2]
    matrix = _parse_matrix(icparsed)
    
    # find the capital and the neighbours of every country
    # Note: capitals[i] returns the capital of i-th country
    capitals, country_cells = matrix.find_capitals()
    neighbours = matrix.find_neighbours(capitals, country_cells)

    viz_distances = []
    o_content_raw = []
    for country_id, capital in enumerate(capitals):
        country_solars = []

        # get the mapping: any_capital -> min_distance_to_this_capital
        md = min_distance(country_id, capitals, neighbours)

        # calculate the costs to collect all the solars in this
        # capital using the minimum distance mapping
        for solar in solar_panels:
            cost = calculate_cost(solar, md, capitals)
            country_solars.append(cost)

        o_content_raw.append(country_solars)
        viz_distances.append(md)

    _visualize(capitals, neighbours)
        
    return o_content_raw


def main(argv):
    inputfilepath, outputfilepath = _get_inputfilepath(argv)
    i_content_raw = read_file(inputfilepath)

    o_content_raw = solution(i_content_raw)

    o_content_frmtd = ""
    for i in range(len(o_content_raw)):
        for cost in o_content_raw[i]:
            o_content_frmtd += str(cost) + ' '
        o_content_frmtd += '\n'
    o_content_frmtd = o_content_frmtd[:-1]

    write_to_file(outputfilepath if outputfilepath != None else INPUT_F + ".out", o_content_frmtd)


if __name__ == "__main__":
    main(sys.argv[1:])