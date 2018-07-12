#!/usr/bin/python3
import string

class Board:
    """A board is always quadratic. ;-)
    Biggest board is 26x26.
    """
    alphabet = list(string.ascii_lowercase)

    def __init__(self, boardsize):
        """Constructor"""
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
        """Print the board."""
        for i in range(self.boardsize - 1, -1, -1):
            print(str(i + 1) + "\t", end='')
            print(*self.board[i], sep='')
        print("\t", end='')
        print(*self.x, sep='')

    def put_piece(self, x, y):
        """Put a chesspiece on a board."""
        self.board[y - 1][x] = "P"
