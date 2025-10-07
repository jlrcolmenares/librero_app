import random
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .db import get_connection


# Sample data of Albert Camus' works
@dataclass
class Book:
    title: str
    year: int
    genre: str

# Default books in case database is not available
CAMUS_BOOKS: List[Book] = [
    Book(title="The Stranger", year=1942, genre="Absurdist fiction"),
    Book(title="The Plague", year=1947, genre="Philosophical novel"),
    Book(title="The Fall", year=1956, genre="Philosophical fiction"),
    Book(title="The Myth of Sisyphus", year=1942, genre="Philosophical essay"),
    Book(title="The Rebel", year=1951, genre="Philosophical essay"),
    Book(title="The First Man", year=1994, genre="Autobiographical novel"),
    Book(title="A Happy Death", year=1971, genre="Philosophical fiction"),
]

def get_books_from_db(limit: int = 10) -> List[Tuple[str, str]]:
    """Get books from the database.

    Args:
        limit: Maximum number of books to return

    Returns:
        List of tuples containing (title, authors)
    """
    con = None
    try:
        con = get_connection()
        cur = con.cursor()
        # First try to get books from the database
        cur.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='books'
        """)
        if cur.fetchone():
            # Table exists, fetch books
            rows = cur.execute("""
                SELECT title, authors FROM books
                ORDER BY title
                LIMIT ?
            """, (limit,)).fetchall()
            if rows:
                return rows

        # If we get here, either table doesn't exist or it's empty
        # Create the table and insert default books if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                authors TEXT NOT NULL,
                language_code TEXT,
                isbn TEXT,
                publication_date TEXT
            )
        """)

        # Check if table is empty
        count = cur.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if count == 0:
            # Insert default books
            books_to_insert = [
                (book.title, "Albert Camus", "fr", "", str(book.year))
                for book in CAMUS_BOOKS
            ]
            cur.executemany(
                """
                INSERT INTO books (title, authors, language_code, isbn, publication_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                books_to_insert
            )
            con.commit()

            # Fetch the newly inserted books
            rows = cur.execute("""
                SELECT title, authors FROM books
                ORDER BY title
                LIMIT ?
            """, (limit,)).fetchall()
            return rows

        return []

    except Exception as e:
        print(f"Error accessing database: {e}")
        # Fall back to default books if database access fails
        return [(book.title, "Albert Camus") for book in CAMUS_BOOKS[:limit]]
    finally:
        if con:
            con.close()

def recommend_book(books_read: Optional[List[str]] = None) -> Book:
    """
    Recommend a book from the database that the user hasn't read yet.
    Falls back to CAMUS_BOOKS if database is not available.

    Args:
        books_read: List of book titles the user has already read

    Returns:
        Book: A randomly selected unread book or a random book if all have been read
    """
    if books_read is None:
        books_read = []

    # Try to get books from database first
    try:
        db_books = get_books_from_db()
        if db_books:
            # Convert database rows to Book objects
            available_books = [
                Book(title=title, year=0, genre="")
                for title, _ in db_books
            ]

            # Convert all book titles to lowercase for case-insensitive comparison
            books_read_lower = [book.lower() for book in books_read]

            # Find unread books from database
            unread_books = [
                book for book in available_books
                if book.title.lower() not in books_read_lower
            ]

            # Return a random unread book if available
            if unread_books:
                return random.choice(unread_books)

            # If all books read, return a random one
            if available_books:
                return random.choice(available_books)

    except Exception as e:
        print(f"Warning: Error getting books from database: {e}")

    # Fall back to CAMUS_BOOKS if database is not available or empty
    print("Using fallback book list")
    available_books = CAMUS_BOOKS
    books_read_lower = [book.lower() for book in books_read]
    unread_books = [
        book for book in available_books
        if book.title.lower() not in books_read_lower
    ]

    return random.choice(unread_books) if unread_books else random.choice(available_books)


def has_read_all_books(books_read: Optional[List[str]] = None) -> bool:
    """
    Check if the user has read all available books.

    Args:
        books_read: List of book titles the user has already read

    Returns:
        bool: True if all books have been read, False otherwise
    """
    if books_read is None:
        books_read = []

    # Try to get books from database first
    try:
        db_books = get_books_from_db()
        if db_books:
            books_read_lower = [book.lower() for book in books_read]
            unread_books = [
                title for title, _ in db_books
                if title.lower() not in books_read_lower
            ]
            return len(unread_books) == 0
    except Exception:
        pass

    # Fall back to CAMUS_BOOKS
    books_read_lower = [book.lower() for book in books_read]
    unread_camus_books: List[Book] = [
        book for book in CAMUS_BOOKS if book.title.lower() not in books_read_lower
    ]
    return len(unread_camus_books) == 0
