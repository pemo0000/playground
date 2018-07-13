#!/usr/bin/python3
import argparse, string, re
from Board import *

print("Running...\n")

#Define and parse command line options with argparse
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--boardsize",
                    help="integer [1-26] to define the boardsize to be drawn. Default is 8 -> chessboard.", type=int,
                    choices=range(1, 27), default=8)
parser.add_argument("-c", "--coordinate",
                    help="coordinate [e.g. a1, b2, c3,...], where a chesspiece is placed on the board.", default="c3")
args = parser.parse_args()
match = re.match(r'([a-z]+)([0-9]+)', args.coordinate, re.I)
items = match.groups()
x = Board.alphabet.index(items[0])
y = int(items[1]) - 1

#Main stuff...
board1 = Board(args.boardsize)
board1.put_piece(x, y)
board1.print()
board1.horizontal_squares(x, y)
board1.vertical_squares(x, y)
board1.diagonal_squares(x, y)

#test push if automatic github authetification works...
