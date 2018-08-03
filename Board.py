import string
import re
import json
import wx
from graphics import *


class Board:
    """A board is always quadratic. ;-)
    Biggest board is 26x26.
    """
    preferences = {
                   'Default': {'darkSquareColor':'black', 'homeSquareColor':'red', 'targetSquareColor':'orange', 'captureSquareColor':'green'},
                   'FEN':     {'darkSquareColor':'grey'}
                  }

    alphabet = list(string.ascii_lowercase)
    graphWinWidth = 400
    graphWinHeight = graphWinWidth

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
        
        self.rectangleSize = self.graphWinWidth / self.boardsize
        self.offsetToCentralizeImageInFEN = self.rectangleSize / 2
        self.offsetToCentralizeImage = self.rectangleSize / 2
        self.win = GraphWin("The Ultimate Chessboard v0.1", width=self.graphWinWidth, height=self.graphWinHeight)
        self.win.setCoords(0, 0, self.boardsize * self.rectangleSize, self.boardsize * self.rectangleSize)

    def print(self, piece, x, y, reachableSquares, flip, displayReachableSquares, coordinateOfPieceToBeCaptured):
        """Prints the board normal or flipped (180° rotated), if the script is called with -f.
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :param reachableSquares: a list with lists of squares a piece can visit
        :param flip: flips = True flips the board (rotates it by 180°)
        :param displayReachableSquares: displayReachableSquares = True displays the squares a piece can visit
        :param coordinateOfPieceToBeCaptured: square of the piece, that might be catured or not by another piece
        """
        # set home square of piece
        self.board[y][x] = piece
        # set reachable squares
        if displayReachableSquares:
            for coordinate in reachableSquares:
                self.board[coordinate[1]][coordinate[0]] = piece.lower() 
        # set target square
        if coordinateOfPieceToBeCaptured:
            coordinate = Board.convert_square_to_coordinate(coordinateOfPieceToBeCaptured)
            self.board[coordinate[1]][coordinate[0]] = "T"
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

    def draw(self, piece, x, y, reachableSquares, flip, displayReachableSquares, coordinateOfPieceToBeCaptured):
        """Draws a graphical board.
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :param reachableSquares: a list with lists of squares a piece can visit
        :param flip: flips = True flips the board (rotates it by 180°)
        :param displayReachableSquares: displayReachableSquares = True displays the squares a piece can visit
        :param coordinateOfPieceToBeCaptured: square of the piece, that might be catured or not by another piece
        """
        y1 = 0
        y2 = y1 + self.rectangleSize 
        if flip:
            xflip = self.boardsize - 1 - x
            yflip = self.boardsize - 1 - y
            for i in range(0, self.boardsize):
                x1 = 0
                x2 = x1 + self.rectangleSize 
                for j in range(0, self.boardsize):
                    square = Rectangle(Point(x1, y1), Point(x2, y2))
                    x1 += self.rectangleSize 
                    x2 += self.rectangleSize 
                    if i & 1 == j & 1:
                        square.setFill(Board.preferences["Default"]["darkSquareColor"])
                    square.draw(self.win)
                y1 += self.rectangleSize
                y2 += self.rectangleSize
            # home square of piece
            homeSquare = Board.convert_coordinate_to_rectangle(self, xflip, yflip)
            homeSquare.setFill(Board.preferences["Default"]["homeSquareColor"])
            homeSquare.draw(self.win)
            # draw picture and reachable squares
            Board.draw_image(self, self.win, piece, xflip ,yflip)
            if displayReachableSquares:
                if piece == "B" or piece =="b":
                    flippedReachableSquares = Board.bishop_squares(self, xflip, yflip)
                elif piece == "R" or piece == "r":
                    flippedReachableSquares = Board.rook_squares(self, xflip, yflip)
                elif piece == "K" or piece == "k":
                    flippedReachableSquares = Board.king_squares(self, xflip, yflip)
                elif piece == "P":
                    flippedReachableSquares = Board.white_pawn_squares(self, xflip, yflip)
                elif piece == "p":
                    flippedReachableSquares = Board.black_pawn_squares(self, xflip, yflip)
                elif piece == "Q" or piece == "q":
                    flippedReachableSquares = Board.bishop_squares(self, xflip, yflip) + Board.rook_squares(self, xflip, yflip)
                elif piece == "N" or piece == "n":
                    flippedReachableSquares = Board.knight_squares(self, xflip, yflip)
                Board.set_target_rectangles(self, self.win, flippedReachableSquares)
            # target square of the piece in question to be captured
            if coordinateOfPieceToBeCaptured:
                coordinate = Board.convert_square_to_coordinate(coordinateOfPieceToBeCaptured)
                flippedXCoordinateOfPieceToBeCaptured = self.boardsize - 1 - coordinate[0]
                flippedYCoordinateOfPieceToBeCaptured = self.boardsize - 1 - coordinate[1]
                targetSquare = Board.convert_coordinate_to_rectangle(self, flippedXCoordinateOfPieceToBeCaptured, flippedYCoordinateOfPieceToBeCaptured)
                targetSquare.setFill(Board.preferences["Default"]["captureSquareColor"])
                targetSquare.draw(self.win)
        else:
            for i in range(0, self.boardsize):
                x1 = 0
                x2 = x1 + self.rectangleSize 
                for j in range(0, self.boardsize):
                    square = Rectangle(Point(x1, y1), Point(x2, y2))
                    x1 += self.rectangleSize 
                    x2 += self.rectangleSize 
                    if i & 1 == j & 1:
                        square.setFill(Board.preferences["Default"]["darkSquareColor"])
                    square.draw(self.win)
                y1 += self.rectangleSize
                y2 += self.rectangleSize
            # home square of piece
            homeSquare = Board.convert_coordinate_to_rectangle(self, x, y)
            homeSquare.setFill(Board.preferences["Default"]["homeSquareColor"])
            homeSquare.draw(self.win)
            # draw picture and reachable squares
            Board.draw_image(self, self.win, piece, x ,y)
            if displayReachableSquares:
                Board.set_target_rectangles(self, self.win, reachableSquares)
            # target square of the piece in question to be captured
            if coordinateOfPieceToBeCaptured:
                coordinate = Board.convert_square_to_coordinate(coordinateOfPieceToBeCaptured)
                targetSquare = Board.convert_coordinate_to_rectangle(self, coordinate[0], coordinate[1])
                targetSquare.setFill(Board.preferences["Default"]["captureSquareColor"])
                targetSquare.draw(self.win)

    @staticmethod 
    def convert_square_to_coordinate(square):
        """converts a square into a coordinate.
        :param square: square of type <character><digit>, e.g. e1, e8, or f7
        :return: a list with a coordinate (tupel) of type (x, y), e.g. (1,0) or (3,7)
        """
        match = re.match(r'([a-z]+)([0-9]+)', square, re.I)
        items = match.groups()
        letter = Board.alphabet.index(items[0])
        coordinate = [letter, int(items[1]) - 1]
        return coordinate

    def set_squares(self, piece, rookSquares, bishopSquares, kingSquares, knightSquares, whitePawnSquares, blackPawnSquares):
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
        elif piece == "P":
            for coordinate in whitePawnSquares:
                self.board[coordinate[1]][coordinate[0]] = "p"

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

    def white_pawn_squares(self, x, y):
        """returns a list of squares/coordinates a white pawn can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of coordinates a white pawn can visit except its own position
        """
        if y == 1:
            allWhitePawnSquares = [[x, y + 1], [x, y + 2]]
        else:
            allWhitePawnSquares = [[x, y + 1]]
        return self.__filter_legal_squares(allWhitePawnSquares)

    def black_pawn_squares(self, x, y):
        """returns a list of squares/coordinates a black pawn can visit except its own position.
        :param x: x coordinate where the piece is put, beginning at 0
        :param y: y coordinate where the piece is put, beginning at 0
        :return: a list with lists of coordinates a black pawn can visit except its own position
        """
        if y == 6:
            allBlackPawnSquares = [[x, y - 1], [x, y - 2]]
        else:
            allBlackPawnSquares = [[x, y - 1]]
        return self.__filter_legal_squares(allBlackPawnSquares)

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

    def __filter_legal_squares(self, reachableSquares):
        """returns a list of "valid" squares/coordinates a piece can visit except its own position.
        :param reachableSquares: a list with list of all coordinates a piece can visit. Could contain coordinates outside the board.
        :return: a list with lists of valid coordinates - that means coordinates, that are really part of the board.
        """
        legalSquares = []
        for coordinate in reachableSquares:
            if coordinate[0] >= 0 and coordinate[1] >= 0 and coordinate[0] < self.boardsize and coordinate[1] < self.boardsize:
                legalSquares.append(coordinate)
        return legalSquares

    @staticmethod
    def try_to_catch_piece(coordinateOfPieceToBeCaptured, squares):
        """checks if a piece can catch/capture another one.
        :param coordinateOfPieceToBeCaptured: square of the piece, that might be catured or not by another piece
        :param squares: a list with lists of coordinates the piece, that might capture another piece, can visit
        :return: True in case of a catch, False if no catch is possible
        """
        if coordinateOfPieceToBeCaptured:
            match = re.match(r'([a-z]+)([0-9]+)', coordinateOfPieceToBeCaptured, re.I)
            items = match.groups()
            letter = Board.alphabet.index(items[0])
            convertedCoordinate = []
            convertedCoordinate += [letter, int(items[1]) - 1]
            return convertedCoordinate in squares

    def draw_image(self, win, piece, x, y):
        """Creates image object and draws image
        :param win: window object representing graphicalBoard
        :param piece: the piece ([K]ing, [Q]ueen, [R]ook, [B]ishop or K[N]ight) chosen
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :return: a label
        """
        pieceImage = Image(Point((x * self.rectangleSize) + self.offsetToCentralizeImage, (y * self.rectangleSize) + self.offsetToCentralizeImage), piece + "40.png")
        pieceImage.draw(win)

    def set_target_rectangles(self, win, targetSquares):
        """creates the rectangles for the graphical board - the squares a piece can visit except its own location
        :param win: window object representing graphicalBoard
        :param targetSquares: a list with lists of coordinates for which the rectangles are set - the squares a piece can visit except its own location
        """
        for coordinate in targetSquares:  # type: object
            square = Board.convert_coordinate_to_rectangle(self, coordinate[0], coordinate[1])
            square.setFill(Board.preferences["Default"]["targetSquareColor"])
            square.draw(win)

    def convert_coordinate_to_rectangle(self, x, y):
        """Converts a coordinate to a rectangle
        :param x: x postion of the piece to put on the board
        :param y: y postion of the piece to put on the board
        :return: a rectangle
        """
        return Rectangle(Point(x * self.rectangleSize, y * self.rectangleSize), Point(x * self.rectangleSize + self.rectangleSize, y * self.rectangleSize + self.rectangleSize))

    @staticmethod
    def convert_fen_to_board_representation(fen):
        """Is converting FEN (Forsyth-Edwards-Notation) into a chess board representation
        :param fen: chess position in Forsyth-Edwards-Notation (FEN), e.g. r4rnk/1pp4p/3p4/3P1b2/1PPbpBPq/8/2QNB1KP/1R3R2 w KQkq - 0 25
        """
        if fen:
            fenParts = fen.split(" ")
            fenWoSlashes = fenParts[0].replace("/", "")
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
            FEN2BoardRepresentation = [extendedFenWoSlashes[x:x+8] for x in range(0, len(extendedFenWoSlashes), 8)]
            splitAfterNthItem = 8
            str_list = [
                '{}\n'.format(item)
                if(((FEN2BoardRepresentation.index(item)+1) % splitAfterNthItem) == 0)
                else
                '{}'.format(item)
                for item in FEN2BoardRepresentation
            ]
            print("FEN")
            print('\n'.join(str_list))
        return FEN2BoardRepresentation 

    def draw_fen(self, FEN2Board):
        """Is drawing the converted FEN to a board 
        :param FEN2Board: list of lists (8x8), that represents all squares on the board with its pieces
        """
        FENwin = GraphWin("The Ultimate Chessboard v0.1 - display FEN", width=self.graphWinWidth, height=self.graphWinHeight)
        FENwin.setCoords(0, 0, self.boardsize * self.rectangleSize, self.boardsize * self.rectangleSize)
        y1 = 0
        y2 = y1 + self.rectangleSize 
        for i in range(self.boardsize - 1, -1, -1):
            x1 = 1
            x2 = x1 + self.rectangleSize 
            for j in range(0, self.boardsize):
                square = Rectangle(Point(x1, y1), Point(x2, y2))
                x1 += self.rectangleSize 
                x2 += self.rectangleSize 
                if i & 1 != j & 1:
                    square.setFill(Board.preferences["FEN"]["darkSquareColor"])
                    square.draw(FENwin)
                    if FEN2Board[i][j] != ' ':
                        pieceImage = Image(Point(x1 - self.offsetToCentralizeImageInFEN, y1 + self.offsetToCentralizeImageInFEN), FEN2Board[i][j] + "40.png")
                        pieceImage.draw(FENwin)
                else:
                    square.draw(FENwin)
                    if FEN2Board[i][j] != ' ':
                        pieceImage = Image(Point(x1 - self.offsetToCentralizeImageInFEN, y1 + self.offsetToCentralizeImageInFEN), FEN2Board[i][j] + "40.png")
                        pieceImage.draw(FENwin)
            y1 += self.rectangleSize
            y2 += self.rectangleSize

    def convert_console_input_to_board_representation(self, piecesWithCoordinates):
        """Is converting a list of pieces with its coordinates (taken from -p and -c from console) to a board representation
        :param piecesWithCoordinates: list of pieces and its coordinates
        """
        listRepresentation = []
        for i in range(0, self.boardsize**2):
            listRepresentation += ' '
        console2BoardRepresentation = [listRepresentation[x:x+self.boardsize] for x in range(0, len(listRepresentation), self.boardsize)]
        for index, element in enumerate(piecesWithCoordinates):
            coordinate = Board.convert_square_to_coordinate(str(piecesWithCoordinates[index][1]))
            console2BoardRepresentation[coordinate[1]][coordinate[0]] = element[0]

        # print reversed board representation to console, maybe for visual debugging. Not really necessary.
        revBoardRepresentation = list(reversed(console2BoardRepresentation))
        splitAfterNthItem = self.boardsize 
        str_list = [
            '{}\n'.format(item)
            if(((revBoardRepresentation.index(item)+1) % splitAfterNthItem) == 0)
            else
            '{}'.format(item)
            for item in revBoardRepresentation
        ]
        print("real board")
        print('\n'.join(str_list))

        return console2BoardRepresentation

    def new_draw(self, boardRepresentation):
        """Is drawing a graphical board
        :param boardRepresentation: list of lists that represents a NxN board with its squares and pieces (if placed on the board)
        """
        boardwin = GraphWin("The Ultimate Chessboard v0.1 - display board", width=self.graphWinWidth, height=self.graphWinHeight)
        boardwin.setCoords(0, 0, self.boardsize * self.rectangleSize, self.boardsize * self.rectangleSize)
        y1 = 0
        y2 = y1 + self.rectangleSize 
        for i in range(0, self.boardsize):
            x1 = 1
            x2 = x1 + self.rectangleSize 
            for j in range(0, self.boardsize):
                square = Rectangle(Point(x1, y1), Point(x2, y2))
                x1 += self.rectangleSize 
                x2 += self.rectangleSize 
                if i & 1 != j & 1:
                    square.setFill(Board.preferences["FEN"]["darkSquareColor"])
                square.draw(boardwin)
                if boardRepresentation[i][j] != ' ':
                    pieceImage = Image(Point(x1 - self.offsetToCentralizeImageInFEN, y1 + self.offsetToCentralizeImageInFEN), boardRepresentation[i][j] + "40.png")
                    pieceImage.draw(boardwin)
            y1 += self.rectangleSize
            y2 += self.rectangleSize
        try:
            self.win.getMouse()
        except GraphicsError:
            pass

    @staticmethod
    def dump_preferences_to_json():
        """Is dumping the preferences (stored in a dictionary) to 'preferences.json' """
        with open('preferences.json', 'w') as fp:
            json.dump(Board.preferences, fp)

    class graphicalBoard(wx.Frame): 
                
       def __init__(self, parent, title): 

          boardsize = 8 
          boardWidth = 400
          boardHeigth = boardWidth
          sizeStatusbar = 70
          rectangleSize = boardWidth / boardsize

          super(Board.graphicalBoard, self).__init__(parent, title = "Ich dreh durch! ;-)", size = (boardWidth,boardHeigth + sizeStatusbar))  
          self.InitUI() 
             
       def InitUI(self): 
          self.CreateStatusBar()
          # Setting up the menu.
          filemenu= wx.Menu()
          menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
          menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

          # Creating the menubar.
          menuBar = wx.MenuBar()
          menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
          self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
          self.Bind(wx.EVT_PAINT, self.OnPaint) 
          self.Centre() 
          self.Show(True)

          # Events.
          self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
          self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
          
          # Drawing image.
          bmp = wx.Bitmap("p40.png")
          wx.StaticBitmap(self, bitmap=bmp, pos=(58,55))
          bmp1 = wx.Bitmap("P40.png")
          wx.StaticBitmap(self, bitmap=bmp1, pos=(205,201))
    		
       def OnPaint(self, e): 
          boardsize = 8
          x = 0
          y = 0
          dc = wx.PaintDC(self) 
          for i in range(0, boardsize):
              for j in range(0, boardsize):
                  if i & 1 == j & 1:
                      dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
                      dc.DrawRectangle(x, y, 50, 50) 
                  else:
                      dc.SetBrush(wx.Brush(wx.Colour(155,155,155)))
                      dc.DrawRectangle(x, y, 50, 50) 
                  x = x + 49
              x = 0
              y = y + 49

       def OnAbout(self,e):
          # Create a message dialog box
          dlg = wx.MessageDialog(self, " Maybe the Ultimate Chess Playground. \n Developped by E8 under strong code and design control of E1.", "About Ultimate Chess Playground", wx.OK)
          dlg.ShowModal()
          dlg.Destroy()

       def OnExit(self,e):
           self.Close(True)
