import random
from dataclasses import dataclass
from typing import List, Optional


# Sample data of Albert Camus' works
@dataclass
class Book:
    title: str
    year: int
    genre: str


CAMUS_BOOKS: List[Book] = [
    Book(title="The Stranger", year=1942, genre="Absurdist fiction"),
    Book(title="The Plague", year=1947, genre="Philosophical novel"),
    Book(title="The Fall", year=1956, genre="Philosophical fiction"),
    Book(title="The Myth of Sisyphus", year=1942, genre="Philosophical essay"),
    Book(title="The Rebel", year=1951, genre="Philosophical essay"),
    Book(title="The First Man", year=1994, genre="Autobiographical novel"),
    Book(title="A Happy Death", year=1971, genre="Philosophical fiction"),
]


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

    # Convert all book titles to lowercase for case-insensitive comparison
    books_read_lower = [book.lower() for book in books_read]

    # Find unread books
    unread_books = [
        book for book in CAMUS_BOOKS if book.title.lower() not in books_read_lower
    ]

    return len(unread_books) == 0


def recommend_book(books_read: Optional[List[str]] = None) -> Book:
    """
    Recommend a book by Albert Camus that the user hasn't read yet.

    Args:
        books_read: List of book titles the user has already read

    Returns:
        Book: A randomly selected unread book or a random book if all have been read

    Raises:
        ValueError: If an unknown book title is provided
    """
    if books_read is None:
        books_read = []

    # Convert all book titles to lowercase for case-insensitive comparison
    books_read_lower = [book.lower() for book in books_read]

    # Validate book titles
    known_titles = {book.title.lower() for book in CAMUS_BOOKS}
    unknown_titles = [title for title in books_read_lower if title not in known_titles]
    if unknown_titles:
        raise ValueError(f"Unknown book title(s): {', '.join(unknown_titles)}")

    # Find unread books
    unread_books: List[Book] = [
        book for book in CAMUS_BOOKS if book.title.lower() not in books_read_lower
    ]

    # If all books read, return a random book for re-reading
    if not unread_books:
        return random.choice(CAMUS_BOOKS)

    # Otherwise select a random unread book
    return random.choice(unread_books)