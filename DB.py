import sqlite3
import os
from stockfish import Stockfish


class DB:

    def __init__(self):
        """Constructor creating a database, a connection and a cursor"""
        self.createDB()
        self.connection = sqlite3.connect("playground.db")
        self.cursor = self.connection.cursor()

    def createDB(self):
        """Is creating a database if not already there"""
        if not os.path.exists("playground.db"):
            print("Datenbank playground.db nicht vorhanden - Datenbank wird anglegt...")
            self.connection = sqlite3.connect("playground.db")
            self.cursor = self.connection.cursor()
            sql = "create table FEN(fen UNIQUE, bestmove)"
            self.cursor.execute(sql)
            print("Datenbank playground.db angelegt.")

    def insertFEN(self, fen):
        """Is inserting FEN into sqlite
        :param fen: chess position in Forsyth-Edwards-Notation (FEN), e.g. r4rnk/1pp4p/3p4/3P1b2/1PPbpBPq/8/2QNB1KP/1R3R2 w KQkq - 0 25
        """
        self.cursor.execute("select count(*) from FEN where fen = ?;", [fen])
        data = self.cursor.fetchone()[0]
        if data == 0: 
            stockfish = Stockfish('/usr/games/stockfish')
            stockfish.set_fen_position("r4rnk/1pp4p/3p4/3P1b2/1PPbpBPq/8/2QNB1KP/1R3R2 w KQkq - 0 25")
            bestmove = stockfish.get_best_move()
        try:
           self.cursor.execute("insert into FEN(fen, bestmove) values(?,?);", (str([fen]), bestmove))
        except sqlite3.IntegrityError:
            pass

    def __del__(self):
        """Destructor"""
        self.connection.commit()
        self.connection.close()
