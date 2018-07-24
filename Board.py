import string
import re
from graphics import *


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
        """Prints the board normal or flipped (180° rotated), if the script is called with -f.
        :param flip: flips = True flips the board (rotates it by 180°)
        """
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
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        """
        self.board[y][x] = piece

    def set_squares(self, piece, rookSquares, bishopSquares, kingSquares, knightSquares):
        """Sets the coordinates a piece can visit
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param rookSquares: a list with lists of squares the rook can visit
        :param bishopSquares: a list with lists of squares the bishop can visit
        :param kingSquares: a list with lists of squares the king can visit
        :param knightSquares: a list with lists of squares the knight can visit
        """
        if piece == "R":
            for coordinate in rookSquares:
                self.board[coordinate[1]][coordinate[0]] = "r"
        elif piece == "B":
            for coordinate in bishopSquares:
                self.board[coordinate[1]][coordinate[0]] = "b"
        elif piece == "Q":
            for coordinate in rookSquares + bishopSquares:
                self.board[coordinate[1]][coordinate[0]] = "q"
        elif piece == "K":
            for coordinate in kingSquares:
                self.board[coordinate[1]][coordinate[0]] = "k"
        elif piece == "N":
            for coordinate in knightSquares:
                self.board[coordinate[1]][coordinate[0]] = "n"

    def __horizontal_squares(self, x, y):
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

    def __vertical_squares(self, x, y):
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
    
    def rook_squares(self, x, y):
        """returns a list of squares/coordinates  the rook can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists coordinates the rook can visit except its own position
        """
        return self.__horizontal_squares(x, y) + self.__vertical_squares(x, y)

    def bishop_squares(self, x, y):
        """returns a list of squares/coordinates the bishop can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of coordinates the the bishop can visit except its own position
        """
        xtemp = x
        ytemp = y
        diagonalSquaresRightUp = []
        while xtemp < self.boardsize - 1 and ytemp < self.boardsize - 1:
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
        while (0 <= xtemp < self.boardsize - 1) and ytemp > 0:
            xtemp += 1
            ytemp -= 1
            diagonalSquaresRightDown.append([xtemp, ytemp])

        return diagonalSquaresRightUp + diagonalSquaresLeftDown + diagonalSquaresLeftUp + diagonalSquaresRightDown

    def king_squares(self, x, y):
        """returns a list of squares/coordinates the king  can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of coordinates the king can visit except its own position
        """
        allKingSquares = [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1], [x, y - 1], [x, y + 1], [x + 1, y - 1],
                          [x + 1, y], [x + 1, y + 1]]
        return self.__filter_legal_squares(allKingSquares)

    def knight_squares(self, x, y):
        """returns a list of squares/coordinates the knight can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of coordinates the knight can visit except its own position
        """
        allKnightSquares = [[x + 1, y - 2], [x - 1, y - 2], [x - 2, y - 1], [x - 2, y + 1], [x - 1, y + 2],
                            [x + 1, y + 2], [x + 2, y + 1], [x + 2, y - 1]]
        return self.__filter_legal_squares(allKnightSquares)

    def __filter_legal_squares(self, allSquares):
        """returns a list of "valid" squares/coordinates a piece can visit except its own position.
        :param allSquares: a list with list of all coordinates a piece can visit. Could contain coordinates outside the board.
        :return: a list with lists of valid coordinates - that means coordinates, that are really part of the board.
        """
        legalSquares = []
        for coordinate in allSquares:
            if coordinate[0] >= 0 and self.boardsize > 0 <= coordinate[1] < self.boardsize:
                legalSquares.append(coordinate)
        return legalSquares

    @staticmethod
    def try_to_catch_piece(coordinateOfPieceToBeCaptured, squares):
        """checks if a piece can catch/capture another one.
        :param coordinateOfPieceToBeCaptured: square of the piece, that might be catured or not by another piece
        :param squares: a list with lists of coordinates the piece, that might capture another piece, can visit
        :return: True in case of a catch, False if no catch is possible
        """
        match = re.match(r'([a-z]+)([0-9]+)', coordinateOfPieceToBeCaptured, re.I)
        items = match.groups()
        letter = Board.alphabet.index(items[0])
        convertedCoordinate = []
        convertedCoordinate += [letter, int(items[1]) - 1]
        return convertedCoordinate in squares

    def draw(self, piece, x, y):
        """Draws a graphical board.
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        """
        win = GraphWin(width=self.boardsize * 50, height=self.boardsize * 50)
        win.setCoords(0, 0, self.boardsize * 10 + 2, self.boardsize * 10 + 2)
        y1 = 1
        y2 = 11
        for i in range(0, self.boardsize):
            x1 = 1
            x2 = 11
            for j in range(0, self.boardsize):
                if i & 1 == j & 1:
                    square = Rectangle(Point(x1, y1), Point(x2, y2))
                    square.setFill("black")
                    x1 += 10 
                    x2 += 10 
                    square.draw(win)
                else:
                    square = Rectangle(Point(x1, y1), Point(x2, y2))
                    x1 += 10
                    x2 += 10
                    square.draw(win)
            y1 += 10
            y2 += 10
        square = self.convert_coordinate_to_rectangle(x, y)
        square.setFill("red")
        square.draw(win)
        label = self.create_and_customize_label(piece, x, y)
        label.draw(win)
        win.getMouse()

    @staticmethod
    def convert_coordinate_to_rectangle(x, y):
        """Converts a coordinate to a rectangle
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :return: a rectangle
        """
        return Rectangle(Point((x * 10) + 1, (y * 10) + 1), Point((x * 10) + 11, (y * 10) + 11))

    @staticmethod
    def create_and_customize_label(piece, x, y):
        """creates and customizes the lable for the piece to be placed on the board
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :return: a label
        """
        label = Text(Point((x * 10) + 6, (y * 10) + 6), piece)
        label.setSize(16)
        label.setStyle("bold")
        label.setFill("blue")
        return label
