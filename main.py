#!/usr/bin/python3
import argparse, string

print("Running...\n")

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--boardsize", help="integer [1-26] to define the boardsize to be drawn. Default is 8 -> chessboard.", type=int, choices=range(1,27), default=8)
args = parser.parse_args()

class Board:

    alphabet = list(string.ascii_lowercase)

    def __init__(self, n):
        self.board = []
        self.x = []
        for i in range(0,n):
            tempboard = []
            for j in range(0,n):
                if i & 1 and j & 1 or not i & 1 and not j & 1:
                    tempboard += [' '] 
                else:
                    tempboard += ['X']
            self.board += [tempboard]
            self.x += self.alphabet[i]
        self.n=n

    def print(self):
        y = self.n
        for i in range(0,self.n):
            print(str(y) + "\t", end ='')
            print(*self.board[i], sep = '')
            y -= 1
        print("\t", end ='')
        print(*self.x, sep = '')

board1 = Board(args.boardsize)
board1.print()
