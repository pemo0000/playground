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
            self.x += Board.alphabet[i]
        self.boardsize = boardsize

    def print(self):
        """Prints the board."""
        for i in range(self.boardsize - 1, -1, -1):
            print(str(i + 1) + "\t", end='')
            print(*self.board[i], sep='')
        print("\t", end='')
        print(*self.x, sep='')

    def put_piece(self, x, y):
        """Puts a chesspiece on a board.
        :param x:
        :param y:
        """
        self.board[y - 1][x] = "P"

    def horizontal_squares(self, x, y):
        """returns a list of horizontal squares/coordinates P can visit except its own position.
        :param x:
        :param y:
        :return:
        """
        horizontalSquares = []
        for i in range(0, self.boardsize):
            horizontalSquares.append([i + 1, y])
        del horizontalSquares[x]
        print("\nhorizontal squares/coordinates P can visit:\n" + str(horizontalSquares))
        return horizontalSquares

    def vertical_squares(self, x, y):
        """returns a list of vertical squares/coordinates P can visit except its own position.
        :param x:
        :param y:
        :return:
        """
        verticalSquares = []
        for i in range(0, self.boardsize):
            verticalSquares.append([x, i + 1])
        del verticalSquares[y - 1]
        print("\nvertical squares/coordinates P can visit:\n" + str(verticalSquares))
        return verticalSquares

    def diagonal_squares(self, x, y):
        """returns a list of diagonal squares/coordinates P can visit except its own position.
        """
        xtemp1 = x
        ytemp1 = y
        diagonalSquaresUp = []
        for i in range(ytemp1, self.boardsize + 1):
            diagonalSquaresUp.append([xtemp1 + 1, ytemp1])
            xtemp1 += 1
            ytemp1 += 1
        diagonalSquaresUp.pop(0)
        print("\ndiagonal squares/coordinates UP P can visit:\n" + str(diagonalSquaresUp))

        xtemp2 = x
        ytemp2 = y
        diagonalSquaresDown = []
        for i in range(ytemp2 - 1, 1, -1):
            xtemp2 -= 1
            ytemp2 -= 1
            diagonalSquaresDown.append([xtemp2 + 1, ytemp2])
        # diagonalSquaresDown.pop(0)
        print("\ndiagonal squares/coordinates DOWN P can visit:\n" + str(diagonalSquaresDown))

        diagonalSquares = diagonalSquaresUp + diagonalSquaresDown
        print("\ndiagonal squares/coordinates P can visit:\n" + str(diagonalSquares))
