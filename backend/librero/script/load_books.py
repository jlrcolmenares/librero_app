import csv
import sqlite3
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "books.csv"     # put your Kaggle CSV here
DB_PATH = DATA_DIR / "books.db"

# Schema we want (simple, no ratings/num_pages/etc.)
SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    authors TEXT,
    language_code TEXT,
    isbn TEXT,
    publication_date TEXT
);
"""

def create_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(SCHEMA)
    con.commit()
    con.close()
    print(f"✅ Database ready at {DB_PATH}")

from typing import Optional

def load_data(limit: Optional[int] = None):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            cur.execute(
                """
                INSERT INTO books (title, authors, language_code, isbn, publication_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    row["title"],
                    row["authors"],
                    row["language_code"],
                    row["isbn"],
                    row["publication_date"],
                ),
            )
            if limit and i >= limit:
                break

    con.commit()
    con.close()
    print(f"✅ Loaded {i} rows into {DB_PATH}")

if __name__ == "__main__":
    create_db()
    load_data()  
