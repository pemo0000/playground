#!/usr/bin/python3
import argparse, string, re

print("Running...\n")

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--boardsize", help="integer [1-26] to define the boardsize to be drawn. Default is 8 -> chessboard.", type=int, choices=range(1,27), default=8)
parser.add_argument("-c", "--coordinate", help="coordinate [e.g. a1, b2, c3,...], where a chesspiece is placed on the board.")
args = parser.parse_args()

class Board:

    alphabet = list(string.ascii_lowercase)

    def __init__(self, boardsize):
        self.board = []
        self.x = []
        for i in range(0,boardsize):
            tempboard = []
            for j in range(0,boardsize):
                if i & 1 and j & 1 or not i & 1 and not j & 1:
                    tempboard += ['X'] 
                else:
                    tempboard += [' ']
            self.board += [tempboard]
            self.x += self.alphabet[i]
        self.boardsize=boardsize

    def print(self):
        for i in range(self.boardsize,0,-1):
            print(str(i) + "\t", end ='')
            i -= 1 
            print(*self.board[i], sep = '')
        print("\t", end ='')
        print(*self.x, sep = '')

    def set_piece(self, coordinate):
        match = re.match(r"([a-z]+)([0-9]+)", args.coordinate, re.I)
        items = match.groups()
        self.board[(int(items[1])-1)][self.alphabet.index(items[0])] = "P"

board1 = Board(args.boardsize)
board1.set_piece(args.coordinate)
board1.print()
