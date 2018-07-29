import sqlite3
import os

class DB:

    def __init__(self):
        self.createDB()
        self.connection = sqlite3.connect("playground.db")
        self.cursor = self.connection.cursor()

    def createDB(self):
        if not os.path.exists("playground.db"):
            print("Datenbank playground.db nicht vorhanden - Datenbank wird anglegt...")
            self.connection = sqlite3.connect("playground.db")
            self.cursor = self.connection.cursor()
            sql = "create table FEN(fen)"
            self.cursor.execute(sql)
            print("Datenbank playground.db angelegt.")

    def insertFEN(self, fen):
        sql = "insert into FEN values(?);"
        self.cursor.execute(sql, [fen])

    def __del__(self):
        self.connection.commit()
        self.connection.close()
