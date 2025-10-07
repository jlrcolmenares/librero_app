import os
import sqlite3

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "books.db")

def get_connection():
    return sqlite3.connect(DB_PATH)
