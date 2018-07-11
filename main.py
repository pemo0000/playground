#!/usr/bin/python3
import argparse, string, re

print("Running...\n")

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--boardsize",
                    help="integer [1-26] to define the boardsize to be drawn. Default is 8 -> chessboard.", type=int,
                    choices=range(1, 27), default=8)
parser.add_argument("-c", "--coordinate",
                    help="coordinate [e.g. a1, b2, c3,...], where a chesspiece is placed on the board.", default="c3")
args = parser.parse_args()
match = re.match(r"([a-z]+)([0-9]+)", args.coordinate, re.I)
items = match.groups()
x, y = items[0], items[1]


class Board:
    alphabet = list(string.ascii_lowercase)

    def __init__(self, boardsize):
        self.board = []
        self.x = []
        for i in range(0, boardsize):
            tempboard = []
            for j in range(0, boardsize):
                if i & 1 and j & 1 or not i & 1 and not j & 1:
                    tempboard += ['X']
                else:
                    tempboard += [' ']
            self.board += [tempboard]
            self.x += self.alphabet[i]
        self.boardsize = boardsize

    def print(self):
        for i in range(self.boardsize - 1, -1, -1):
            print(str(i + 1) + "\t", end='')
            print(*self.board[i], sep='')
        print("\t", end='')
        print(*self.x, sep='')

    def set_piece(self, x, y):
        x = self.alphabet.index(x)
        self.board[int(y) - 1][int(x)] = "P"


board1 = Board(args.boardsize)
board1.set_piece(x, y)
board1.print()
