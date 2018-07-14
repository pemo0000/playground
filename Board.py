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
        self.board[y][x] = "P"

    def horizontal_squares(self, x, y):
        """returns a list of horizontal squares/coordinates P can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of horizontal coordinates the piece can visit except its own position
        """
        horizontalSquares = []
        for i in range(0, self.boardsize):
            horizontalSquares.append([i, y])
        del horizontalSquares[x]
        print("\nhorizontal squares/coordinates P can visit:\n" + str(horizontalSquares))
        return horizontalSquares

    def vertical_squares(self, x, y):
        """returns a list of vertical squares/coordinates P can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of vertical coordinates the piece can visit except its own position
        """
        verticalSquares = []
        for i in range(0, self.boardsize):
            verticalSquares.append([x, i])
        del verticalSquares[y]
        print("\nvertical squares/coordinates P can visit:\n" + str(verticalSquares))
        return verticalSquares

    def diagonal_squares(self, x, y):
        """returns a list of diagonal squares/coordinates P can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of diagonal coordinates the piece can visit except its own position
        """
        xtemp1 = x
        ytemp1 = y
        diagonalSquaresRightUp = []
        while xtemp1 < self.boardsize - 1 and ytemp1 < self.boardsize -1:
            xtemp1 += 1
            ytemp1 += 1
            diagonalSquaresRightUp.append([xtemp1, ytemp1])
        print("\ndiagonal squares/coordinates RIGHT UP P can visit:\n" + str(diagonalSquaresRightUp))

        xtemp2 = x
        ytemp2 = y
        diagonalSquaresLeftDown = []
        while xtemp2 > 0 and ytemp2 > 0:
            xtemp2 -= 1
            ytemp2 -= 1
            diagonalSquaresLeftDown.append([xtemp2, ytemp2])
        print("\ndiagonal squares/coordinates LEFT DOWN P can visit:\n" + str(diagonalSquaresLeftDown))

        xtemp3 = x
        ytemp3 = y
        diagonalSquaresLeftUp = []
        while xtemp3 > 0 and ytemp3 < self.boardsize - 1:
            xtemp3 -= 1
            ytemp3 += 1
            diagonalSquaresLeftUp.append([xtemp3, ytemp3])
        print("\ndiagonal squares/coordinates LEFT UP P can visit:\n" + str(diagonalSquaresLeftUp))

        xtemp4 = x
        ytemp4 = y
        diagonalSquaresRightDown = []
        while xtemp4 > 0 and ytemp4 > 0:
            xtemp4 += 1
            ytemp4 -= 1
            diagonalSquaresRightDown.append([xtemp4, ytemp4])
        print("\ndiagonal squares/coordinates RIGHT DOWN P can visit:\n" + str(diagonalSquaresRightDown))

        diagonalSquares = diagonalSquaresRightUp + diagonalSquaresLeftDown + diagonalSquaresLeftUp + diagonalSquaresRightDown
        print("\ndiagonal squares/coordinates P can visit:\n" + str(diagonalSquares))
