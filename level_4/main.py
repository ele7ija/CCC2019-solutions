# Generic/Built-in Libs
import sys, getopt, os
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

# Other imports
from model import *

# Globals
ROWS, COLS, N = 0, 0, 0
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


def _parse_rays(icparsed):
    global N

    rays = []
    for i in range(3, N*4, 4):
        r = Ray(icparsed[i], icparsed[i+1], icparsed[i+2], icparsed[i+3])
        rays.append(r)

    return rays
    

def _visualize(i, r, visited_cells):
    fig, ax = plt.subplots()
    ax.grid(which='major', axis='both')
    plt.xlim(0, ROWS)
    plt.ylim(0, COLS)
    ax.set_xticks(np.arange(-0.5, ROWS + 0.5, 1))
    ax.set_yticks(np.arange(-0.5, COLS + 0.5, 1))

    x = [p.x for p in visited_cells]
    y = [p.y for p in visited_cells]
    plt.plot(x, y, color='g', label='Visited cells')

    plt.scatter(r.o.x, r.o.y, color='b', label='Origin')

    x_dom = np.arange(-0.5, ROWS + 0.5, 1)
    fun, _ = r.create_funs()
    y = [fun(x) for x in x_dom]
    plt.plot(x_dom, y, color='r', label='Ray direction')

    ax.legend()
    plt.title('input: \'' + INPUT_F + '\'\n' + \
        ' RAY: {}, O: {}, D: {}'.format(i, r.o, r.d))
    if not os.path.exists('./viz'):
        os.mkdir('./viz')
    plt.savefig('./viz/' + INPUT_F + '_RAY{}.png'.format(i))


def solution(i_content):
    global ROWS, COLS, N

    icparsed = [int(x) for x in i_content.split()]
    ROWS, COLS, N = icparsed[0], icparsed[1], icparsed[2]
    ROWS += 1   # I used range(ROWS) in several occasions so
    COLS += 1   # this seemed like an OK quick fix
    rays = _parse_rays(icparsed)
    
    o_content_raw = []
    for i, r in enumerate(rays):
        visited_cells = r.get_cells(ROWS, COLS)

        _visualize(i, r, visited_cells)

        o_content_raw.append(visited_cells)
    return o_content_raw


def main(argv):
    inputfilepath, outputfilepath = _get_inputfilepath(argv)
    i_content = read_file(inputfilepath)

    o_content_raw = solution(i_content)

    o_content_frmtd = ""
    for i in range(N):
        for cell in o_content_raw[i]:
            o_content_frmtd += str(cell.x) + ' ' + str(cell.y) + ' '
        o_content_frmtd += '\n'
    o_content_frmtd = o_content_frmtd[:-1]

    write_to_file(outputfilepath if outputfilepath != None else "your_input.out", o_content_frmtd)


if __name__ == "__main__":
    main(sys.argv[1:])