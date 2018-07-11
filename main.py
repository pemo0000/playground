#!/usr/bin/python3
import argparse, string

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
                    tempboard += [' '] 
                else:
                    tempboard += ['X']
            self.board += [tempboard]
            self.x += self.alphabet[i]
        self.boardsize=boardsize

    def print(self):
        y = self.boardsize
        for i in range(0,self.boardsize):
            print(str(y) + "\t", end ='')
            print(*self.board[i], sep = '')
            y -= 1
        print("\t", end ='')
        print(*self.x, sep = '')

    def set_piece(self, coordinate):
        splitCoordinate = list(coordinate)        
        self.board[self.alphabet.index(splitCoordinate[0])][int(splitCoordinate[1])] = "P"

board1 = Board(args.boardsize)
board1.set_piece(args.coordinate)
board1.print()
