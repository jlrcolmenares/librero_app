import sqlite3

DB_PATH = "data/books.db"

def get_connection():
    return sqlite3.connect(DB_PATH)