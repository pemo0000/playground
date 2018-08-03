#!/usr/bin/python3
import argparse
import sys, os, platform, wx

from Board import *
from DB import *
from UI import *

print("Running...\n")

# Define and parse command line options with argparse
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--boardsize",
                    help="integer [1-26] to define the boardsize to be drawn. Default is 8 -> chessboard.", type=int,
                    choices=range(1, 27), default=8)
parser.add_argument("-p", "--pieces",
                    help="comma separated list of chess piece [e.g. K,K,Q,...] you want to put on a square. Options are [K]ing, [Q]ueen, [R]ook, [B]ishop and K[N]ight for white pieces, use lowercase [kqrbn] for a black piece..",
                    default="Q")
parser.add_argument("-c", "--coordinates",
                    help="comma separated list of coordinates [e.g. a1,b2,c3,...], where the chesspieces defined with -p are placed on the board.",
                    default="c3")
parser.add_argument("-f", "--flip",
                    help="flips the board.", action="store_true")
parser.add_argument("-d", "--displayReachableSquares",
                    help="displays the squares a piece can visit except its own position.", action="store_true")
parser.add_argument("-t", "--target",
                    help="coordinate of the piece in question to be captured or not..")
parser.add_argument("-z", "--fen",
                    help="FEN notation of a position of an 8x8 board. E.g. r4rnk/1pp4p/3p4/3P1b2/1PPbpBPq/8/2QNB1KP/1R3R2",
                    default="r4rnk/1pp4p/3p4/3P1b2/1PPbpBPq/8/2QNB1KP/1R3R2")
parser.add_argument("-s", "--saveFEN",
                    help="inserts FEN in sqlite.", action="store_true")
args = parser.parse_args()

def check_args():
    """checks and validates command line options"""
    # Does -p -c have the same number of arguments?
    if len(list(args.pieces.split(','))) != len(list(args.coordinates.split(','))):
        print("Number of arguments for -p and -c needs to be equal. Please try again...")
        sys.exit()

    # Are the coordinates in -c legal squares?
    # Check if a coordinate is listed more than once
    coordinates = args.coordinates.split(',')
    if len(coordinates) != len(set(coordinates)):
        print(
            "You cannot have a coordinate more than once, you can only put one piece on one square. Please try again...")
        sys.exit()

    # Check if coordinates are not outside of the board
    allCoordinates = []
    for i in range(1, args.boardsize + 1):
        for j in range(1, args.boardsize + 1):
            coordinate = Board.alphabet[i - 1] + str(j)
            allCoordinates.append(coordinate)
    if not set(coordinates).issubset(set(allCoordinates)):
        print(coordinates, allCoordinates)
        print("At least one coordinate is not valid. Please try again...")
        sys.exit()

# Generate list with tuples of pieces and coordinates and process it for further stuff
piecesWithCoordinates = list(zip(args.pieces.split(','), args.coordinates.split(',')))
for item in piecesWithCoordinates:
    piece = item[0]
    match = re.match(r'([a-z]+)([0-9]+)', item[1], re.I)
    items = match.groups()
    x = Board.alphabet.index(items[0])
    y = int(items[1]) - 1

# Main stuff...
check_args()
board1 = Board(args.boardsize)
db = DB()
rookSquares, bishopSquares, kingSquares, knightSquares, whitePawnSquares, blackPawnSquares = board1.rook_squares(x, y), board1.bishop_squares(x, y), board1.king_squares(x, y), board1.knight_squares(x, y), board1.white_pawn_squares(x, y), board1.black_pawn_squares(x, y)

if piece == "K" or piece == "k":
    board1.print(piece, x, y, kingSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "Q" or piece == "q":
    board1.print(piece, x, y, rookSquares + bishopSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "R" or piece == "r":
    board1.print(piece, x, y, rookSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "B" or piece == "b":
    board1.print(piece, x, y, bishopSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "N" or piece == "n":
    board1.print(piece, x, y, knightSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "P":
    board1.print(piece, x, y, whitePawnSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "p":
    board1.print(piece, x, y, blackPawnSquares, args.flip, args.displayReachableSquares, args.target)

if  (piece == "R" or piece == "r") and Board.try_to_catch_piece(args.target, rookSquares)                   or\
    (piece == "Q" or piece == "q") and Board.try_to_catch_piece(args.target, rookSquares + bishopSquares)   or\
    (piece == "B" or piece == "b") and Board.try_to_catch_piece(args.target, bishopSquares)                 or\
    (piece == "K" or piece == "k") and Board.try_to_catch_piece(args.target, kingSquares)                   or\
    (piece == "P") and Board.try_to_catch_piece(args.target, whitePawnSquares)                              or\
    (piece == "p") and Board.try_to_catch_piece(args.target, blackPawnSquares)                              or\
    (piece == "N" or piece == "n") and Board.try_to_catch_piece(args.target, knightSquares):
        print("Catch!")
else:
        print("No catch!")

if args.boardsize == 8 and args.fen:
    board1.draw_fen(board1.convert_fen_to_board_representation(args.fen))
    if args.saveFEN:
        db.insertFEN(args.fen)    


if piece == "K" or piece == "k":
    board1.draw(piece, x, y, kingSquares, args.flip, args.displayReachableSquares ,args.target)
elif piece == "Q" or piece == "q":
    board1.draw(piece, x, y, rookSquares + bishopSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "R" or piece == "r":
    board1.draw(piece, x, y, rookSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "B" or piece == "b":
    board1.draw(piece, x, y, bishopSquares, args.flip,args. displayReachableSquares, args.target)
elif piece == "N" or piece == "n":
    board1.draw(piece, x, y, knightSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "P":
    board1.draw(piece, x, y, whitePawnSquares, args.flip, args.displayReachableSquares, args.target)
elif piece == "p":
    board1.draw(piece, x, y, blackPawnSquares, args.flip, args.displayReachableSquares, args.target)

if not os.path.exists("preferences.json"):
    Board.dump_preferences_to_json()

board1.new_draw(board1.convert_console_input_to_board_representation(piecesWithCoordinates))

# 1st new UI try with wxpython - pushed UI to UI.py
app = wx.App(False)
ui1 = UI(None, 'The Ultimate Chessboard v0.1 - wxphyton', args.boardsize)
app.MainLoop()
