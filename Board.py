#!/usr/bin/python3
import string

class Board:
    """A board is always quadratic. ;-)
    Biggest board is 26x26.
    """
    alphabet = list(string.ascii_lowercase)

    def __init__(self, boardsize):
        """Constructor"""
        self.boardsize = boardsize
        self.board = []
        for i in range(0, boardsize):
            templine = []
            for j in range(0, boardsize):
                if i & 1 == j & 1:
                    templine += ['X']
                else:
                    templine += [' ']
            self.board += [templine]

    def print(self):
        """Prints the board."""
        for i in range(self.boardsize - 1, -1, -1):
            print(str(i + 1) + "\t", end='')
            print(*self.board[i], sep='')
        print("\t", end='')
        print(string.ascii_lowercase[:self.boardsize])

    def put_piece(self, piece, x, y):
        """Puts a chesspiece on a board.
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        """
        if piece == "Q":
            self.board[y][x] = "Q"
        elif piece == "R":
            self.board[y][x] = "R"
        elif piece == "B":
            self.board[y][x] = "B"
        elif piece == "K":
            self.board[y][x] = "K"
        elif piece == "N":
            self.board[y][x] = "N"

    def set_squares(self, piece, horizontalSquares, verticalSquares, diagonalSquares, legalKingSquares, legalKnightSquares):
        """Sets the coordinates a piece can visit
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight chosen
        :param horizontalSquares: a list with lists of horizontal squares a piece can visit
        :param verticalSquares: a list with lists of vertical squares a piece can visit
        :param diagonalSquares: a list with list of diagonal squares a piece can visit
        """
        if piece == "R":
            rookSquares = horizontalSquares + verticalSquares
            for coordinate in rookSquares:
                x = coordinate[0]
                y = coordinate[1]
                self.board[y][x] = "r"
        elif piece == "B":
            bishopSquares = diagonalSquares
            for coordinate in bishopSquares:
                x = coordinate[0]
                y = coordinate[1]
                self.board[y][x] = "b"
        elif piece == "Q":
            queenSquares = horizontalSquares + verticalSquares + diagonalSquares
            for coordinate in queenSquares:
                x = coordinate[0]
                y = coordinate[1]
                self.board[y][x] = "q"
        elif piece == "K":
            for coordinate in legalKingSquares:
                x = coordinate[0]
                y = coordinate[1]
                self.board[y][x] = "k"
        elif piece == "N":
            for coordinate in legalKnightSquares:
                x = coordinate[0]
                y = coordinate[1]
                self.board[y][x] = "n"

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
        return verticalSquares

    def diagonal_squares(self, x, y):
        """returns a list of diagonal squares/coordinates P can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of diagonal coordinates the piece can visit except its own position
        """
        xtemp = x
        ytemp = y
        diagonalSquaresRightUp = []
        while xtemp < self.boardsize - 1 and ytemp < self.boardsize -1:
            xtemp += 1
            ytemp += 1
            diagonalSquaresRightUp.append([xtemp, ytemp])

        xtemp = x
        ytemp = y
        diagonalSquaresLeftDown = []
        while xtemp > 0 and ytemp > 0:
            xtemp -= 1
            ytemp -= 1
            diagonalSquaresLeftDown.append([xtemp, ytemp])

        xtemp = x
        ytemp = y
        diagonalSquaresLeftUp = []
        while xtemp > 0 and ytemp < self.boardsize - 1:
            xtemp -= 1
            ytemp += 1
            diagonalSquaresLeftUp.append([xtemp, ytemp])

        xtemp = x
        ytemp = y
        diagonalSquaresRightDown = []
        while (xtemp >= 0 and xtemp < self.boardsize - 1)  and ytemp > 0:
            xtemp += 1
            ytemp -= 1
            diagonalSquaresRightDown.append([xtemp, ytemp])

        diagonalSquares = diagonalSquaresRightUp + diagonalSquaresLeftDown + diagonalSquaresLeftUp + diagonalSquaresRightDown
        return diagonalSquares

    def king_squares(self, x, y):
        """returns a list of squares/coordinates the king  can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of coordinates the king can visit except its own position
        """
        xtemp = x
        ytemp = y
        kingSquares = [(xtemp - 1, ytemp - 1), (xtemp - 1, ytemp), (xtemp -1, ytemp + 1), (xtemp, ytemp - 1), (xtemp, ytemp + 1), (xtemp + 1, ytemp -1), (xtemp + 1, ytemp), (xtemp + 1, ytemp + 1)]
        return self.filter_legal_squares(kingSquares)

    def knight_squares(self, x, y):
        """returns a list of squares/coordinates the knight can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of coordinates the knight can visit except its own position
        """
        xtemp = x
        ytemp = y
        knightSquares = [(xtemp + 1, ytemp - 2), (xtemp - 1, ytemp -2), (xtemp - 2, ytemp - 1), (xtemp - 2, ytemp + 1), (xtemp - 1, ytemp + 2), (xtemp + 1, ytemp + 2), (xtemp + 2, ytemp + 1), (xtemp + 2, ytemp - 1)]
        return self.filter_legal_squares(knightSquares)

    def filter_legal_squares(self, allSquares):
        """returns a list of "valid" squares/coordinates a piece can visit except its own position.
        :param squares: a list with list of all coordinates a piece can visit. Could contain coordinates outside the board.
        :return: a list with lists of valid coordinates - that means coordinates, that are really part of the board.
        """
        legalSquares = []
        for coordinate in allSquares:
            if coordinate[0] >= 0 and coordinate[1] >= 0 and coordinate[0] < self.boardsize and coordinate[1] < self.boardsize:
                legalSquares.append(coordinate)
        return legalSquares

