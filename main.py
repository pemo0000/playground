#!/usr/bin/python3
import argparse
import sys

from Board import *

print("Running...\n")

# Define and parse command line options with argparse
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--boardsize",
                    help="integer [1-26] to define the boardsize to be drawn. Default is 8 -> chessboard.", type=int,
                    choices=range(1, 27), default=8)
parser.add_argument("-p", "--pieces",
                    help="comma separated list of chess piece [e.g. K,K,Q,...] you want to put on a square. Options are [K]ing, [Q]ueen, [R]ook, [B]ishop and K[N]ight.",
                    default="Q")
parser.add_argument("-c", "--coordinates",
                    help="comma separated list of coordinates [e.g. a1,b2,c3,...], where the chesspieces defined with -p are placed on the board.",
                    default="c3")
parser.add_argument("-f", "--flip",
                    help="flips the board.", action="store_true")
parser.add_argument("-t", "--target",
                    help="coordinate of the piece in question to be captured or not..", default="b2")
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
# try to implement the piece to catch and therefore take 1st piece as the piece to be captured
coordinateOfPieceToBeCaptured = args.target

# Main stuff...
check_args()
board1 = Board(args.boardsize)
rookSquares, diagonalSquares, kingSquares, knightSquares = board1.rook_squares(x, y), board1.diagonal_squares(x, y), board1.king_squares(x, y), board1.knight_squares(x, y)
board1.put_piece(piece, x, y)
board1.set_squares(piece, rookSquares, diagonalSquares, kingSquares, knightSquares)
board1.print(args.flip)
if piece == "R":
    if board1.try_to_catch_piece(coordinateOfPieceToBeCaptured, rookSquares):
        print("Catch!")
    else:
        print("No catch!")
elif piece == "Q":
    if board1.try_to_catch_piece(coordinateOfPieceToBeCaptured, rookSquares + diagonalSquares):
        print("Catch!")
    else:
        print("No catch!")
elif piece == "B":
    if board1.try_to_catch_piece(coordinateOfPieceToBeCaptured, diagonalSquares):
        print("Catch!")
    else:
        print("No catch!")
elif piece == "K":
    if board1.try_to_catch_piece(coordinateOfPieceToBeCaptured, kingSquares):
        print("Catch!")
    else:
        print("No catch!")
elif piece == "N":
    if board1.try_to_catch_piece(coordinateOfPieceToBeCaptured, knightSquares):
        print("Catch!")
    else:
        print("No catch!")
