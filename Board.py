import string
import re
from graphics import *


class Board:
    """A board is always quadratic. ;-)
    Biggest board is 26x26.
    """
    alphabet = list(string.ascii_lowercase)
    boardMargin = 2
    rectangleHomeSquareColor = "red"
    rectangleTargetSquareColor = "orange"
    rectangleFillColorDarkSquares = "black"

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
        
        self.windowSize = self.boardsize * 6.25
        self.rectangleSize = self.boardsize * 1.25
        self.win = GraphWin("The Ultimate Chessboard v0.1", width=self.boardsize * self.windowSize, height=self.boardsize * self.windowSize)
        self.win.setCoords(0, 0, self.boardsize * self.rectangleSize + self.boardMargin, self.boardsize * self.rectangleSize + self.boardMargin)

    def print(self, piece, x, y, flip):
        """Prints the board normal or flipped (180° rotated), if the script is called with -f.
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :param flip: flips = True flips the board (rotates it by 180°)
        """
        self.board[y][x] = piece
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

    def draw(self, piece, x, y, allSquares):
        """Draws a graphical board.
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :param allSquares: a list with lists of squares a piece can visit
        """
        y1 = 1
        y2 = y1 + self.rectangleSize 
        for i in range(0, self.boardsize):
            x1 = 1
            x2 = x1 + self.rectangleSize 
            for j in range(0, self.boardsize):
                square = Rectangle(Point(x1, y1), Point(x2, y2))
                x1 += self.rectangleSize 
                x2 += self.rectangleSize 
                if i & 1 == j & 1:
                    square.setFill(self.rectangleFillColorDarkSquares)
                square.draw(self.win)
            y1 += self.rectangleSize
            y2 += self.rectangleSize
        square = Board.convert_coordinate_to_rectangle(self, x, y)
        square.setFill(self.rectangleHomeSquareColor)
        square.draw(self.win)
        Board.create_image(self, self.win, piece,x ,y)
        Board.set_target_rectangles(self, self.win, allSquares)
        try:
            self.win.getMouse()
        except GraphicsError:
            pass

    def create_image(self, win, piece, x, y):
        """Creates image object and draws image
        :param win: window object representing graphicalBoard
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :return: a label
        """
        pieceImage = Image(Point((x * self.rectangleSize) + 6, (y * self.rectangleSize) + 6), piece + "40.png")
        pieceImage.draw(win)

    def set_target_rectangles(self, win, targetSquares):
        """creates the rectangles for the graphical board - the squares a piece can visit except its own location
        :param win: window object representing graphicalBoard
        :param targetSquares: a list with lists of coordinates for which the rectangles are set - the squares a piece can visit except its own location
        """
        for coordinate in targetSquares:  # type: object
            square = Board.convert_coordinate_to_rectangle(self, coordinate[0], coordinate[1])
            square.setFill(Board.rectangleTargetSquareColor)
            square.draw(win)

    def convert_coordinate_to_rectangle(self, x, y):
        """Converts a coordinate to a rectangle
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :return: a rectangle
        """
        return Rectangle(Point((x * self.rectangleSize) + 1, (y * self.rectangleSize) + 1), Point((x * self.rectangleSize) + self.rectangleSize + 1, (y * self.rectangleSize) + self.rectangleSize + 1))

    @staticmethod
    def create_and_customize_label(win, piece, x, y):
        """Creates and customizes the lable for the piece to be placed on the board
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :return: a label
        """
        label = Text(Point((x * Board.rectangleSize) + 6, (y * Board.rectangleSize) + 6), piece)
        label.setSize(16)
        label.setStyle("bold")
        label.setFill("blue")
        label.draw(win)
        return label

    def do_something_with_fen(self, fen):
        """Is converting a FEN (Forsyth-Edwards-Notation) string into a list of lists that seems to look like a chess position - digits indicate blank squares
        :param fen: chess position in Forsyth-Edwards-Notation (FEN), e.g. r4rnk/1pp4p/3p4/3P1b2/1PPbpBPq/8/2QNB1KP/1R3R2
        """
        if fen:
            fenWoSlashes = fen.replace("/", "")
            extendedFenWoSlashes = []
            for element in fenWoSlashes:
                if element.isdigit():
                    for i in range(0, int(element)):
                        extendedFenWoSlashes += element
                else:
                    extendedFenWoSlashes += element
            for n, i in enumerate(extendedFenWoSlashes):
                if i.isdigit():
                    extendedFenWoSlashes[n] = ' ' 
            chunks = [extendedFenWoSlashes[x:x+8] for x in range(0, len(extendedFenWoSlashes), 8)]
            splitAfterNthItem = 8
            str_list = [
                '{}\n'.format(item)
                if(((chunks.index(item)+1) % splitAfterNthItem) == 0)
                else
                '{}'.format(item)
                for item in chunks
            ]
            print('\n'.join(str_list))
