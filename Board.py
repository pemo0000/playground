#!/usr/bin/python3
import string, re

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

    def print(self, flip):
        """Prints the board normal or flipped (180° rotated)."""
        if flip:
            for i in range(0, self.boardsize):
                print(str(i + 1) + "\t", end='')
                print(*self.board[i][::-1], sep='')
            print("\t", end='')                
            print(string.ascii_lowercase[:self.boardsize][::-1])
        else:
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
        self.board[y][x] = piece

    def set_squares(self, piece, horizontalSquares, verticalSquares, diagonalSquares, legalKingSquares, legalKnightSquares):
        """Sets the coordinates a piece can visit
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param horizontalSquares: a list with lists of horizontal squares a piece can visit
        :param verticalSquares: a list with lists of vertical squares a piece can visit
        :param diagonalSquares: a list with lists of diagonal squares a piece can visit
        :param legalKingSquares: a list with lists of squares the king can visit
        :param legalKnightSquares: a list with lists of squares the knight can visit
        """
        if piece == "R":
            for coordinate in horizontalSquares + verticalSquares:
                self.board[coordinate[1]][coordinate[0]] = "r"
        elif piece == "B":
            for coordinate in diagonalSquares:
                self.board[coordinate[1]][coordinate[0]] = "b"
        elif piece == "Q":
            for coordinate in horizontalSquares + verticalSquares + diagonalSquares:
                self.board[coordinate[1]][coordinate[0]] = "q"
        elif piece == "K":
            for coordinate in legalKingSquares:
                self.board[coordinate[1]][coordinate[0]] = "k"
        elif piece == "N":
            for coordinate in legalKnightSquares:
                self.board[coordinate[1]][coordinate[0]] = "n"

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
        kingSquares = [(x - 1, y - 1), (x - 1, y), (x -1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y -1), (x + 1, y), (x + 1, y + 1)]
        return self.__filter_legal_squares(kingSquares)

    def knight_squares(self, x, y):
        """returns a list of squares/coordinates the knight can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of coordinates the knight can visit except its own position
        """
        knightSquares = [(x + 1, y - 2), (x - 1, y -2), (x - 2, y - 1), (x - 2, y + 1), (x - 1, y + 2), (x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1)]
        return self.__filter_legal_squares(knightSquares)

    def try_to_catch_piece(self, coordinateOfPieceToBeCaptured, squares):
        """checks if a piece can catch/capture another one. 1st draft for rook...
        :param coordinateOfPieceToBeCaptured: square of the piece, that might be catured or not by another piece
        :param squares: a list with lists of coordinates the piece, that might capture another piece, can visit
        """
        match = re.match(r'([a-z]+)([0-9]+)', coordinateOfPieceToBeCaptured, re.I)
        items = match.groups()
        letter = Board.alphabet.index(items[0])
        convertedCoordinate = []
        convertedCoordinate += [(letter), int(items[1]) - 1]
        print(convertedCoordinate)
        print(squares)
        if convertedCoordinate in squares:
            print("Catch!")
        else:
            print("No catch!")

    def __filter_legal_squares(self, allSquares):
        """returns a list of "valid" squares/coordinates a piece can visit except its own position.
        :param squares: a list with list of all coordinates a piece can visit. Could contain coordinates outside the board.
        :return: a list with lists of valid coordinates - that means coordinates, that are really part of the board.
        """
        legalSquares = []
        for coordinate in allSquares:
            if coordinate[0] >= 0 and coordinate[1] >= 0 and coordinate[0] < self.boardsize and coordinate[1] < self.boardsize:
                legalSquares.append(coordinate)
        return legalSquares

