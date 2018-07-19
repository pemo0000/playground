#!/usr/bin/python3
import argparse, string, re, sys
from Board import *

print("Running...\n")

#Define and parse command line options with argparse
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--boardsize",
                    help="integer [1-26] to define the boardsize to be drawn. Default is 8 -> chessboard.", type=int,
                    choices=range(1, 27), default=8)
parser.add_argument("-p", "--pieces",
                    help="comma separated list of chess piece [e.g. K,K,Q,...] you want to put on a square. Options are [K]ing, [Q]ueen, [R]ook, [B]ishop and K[N]ight.",
                    default="Q")
parser.add_argument("-c", "--coordinates",
                    help="comma separated list of coordinates [e.g. a1,b2,c3,...], where the chesspieces defined with -p are placed on the board.", default="c3")
args = parser.parse_args()

def check_args():
    """checks and validates command line options"""
    #Does -p -c have the same number of arguments?
    if len(list(args.pieces.split(','))) != len(list(args.coordinates.split(','))):
        print("Number of arguments for -p and -c needs to be equal. Please try again...")
        sys.exit()
    
    #Are the coordinates in -c legal squares?
    coordinates = args.coordinates.split(',')
    allCoordinates = []
    for i in range(1, args.boardsize + 1):
        for j in range(1, args.boardsize + 1):
            coordinate = Board.alphabet[i - 1] + str(j)
            allCoordinates.append(coordinate)
    if not set(coordinates).issubset(set(allCoordinates)):
        print("At least one coordinate is not valid. Please try again...")
        sys.exit()

#Generate list with tuples of pieces and coordinates and process it for further stuff
piecesWithCoordinates = list(zip(args.pieces.split(','), args.coordinates.split(',')))
i = 0
for item in piecesWithCoordinates:
    piece = piecesWithCoordinates[i][0]
    match = re.match(r'([a-z]+)([0-9]+)', piecesWithCoordinates[i][1], re.I)
    items = match.groups()
    x = Board.alphabet.index(items[0])
    y = int(items[1]) - 1
    i += 1

#Main stuff...
check_args()
board1 = Board(args.boardsize)
horizontalSquares, verticalSquares, diagonalSquares, legalKingSquares, legalKnightSquares = board1.horizontal_squares(x, y), board1.vertical_squares(x, y), board1.diagonal_squares(x, y), board1.king_squares(x, y), board1.knight_squares(x, y)
board1.put_piece(piece, x, y)
board1.set_squares(piece, horizontalSquares, verticalSquares, diagonalSquares, legalKingSquares, legalKnightSquares)
board1.print()
