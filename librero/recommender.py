from __future__ import annotations

import random
from typing import List, Optional

# Sample data of Albert Camus' works
CAMUS_BOOKS = [
    {"title": "The Stranger", "year": 1942, "genre": "Absurdist fiction"},
    {"title": "The Plague", "year": 1947, "genre": "Philosophical novel"},
    {"title": "The Fall", "year": 1956, "genre": "Philosophical fiction"},
    {"title": "The Myth of Sisyphus", "year": 1942, "genre": "Philosophical essay"},
    {"title": "The Rebel", "year": 1951, "genre": "Philosophical essay"},
    {"title": "The First Man", "year": 1994, "genre": "Autobiographical novel"},
    {"title": "A Happy Death", "year": 1971, "genre": "Philosophical fiction"},
]


def recommend_book(books_read: Optional[List[str]] = None) -> str:
    """
    Recommend a book by Albert Camus that the user hasn't read yet.

    Args:
        books_read: List of book titles the user has already read

    Returns:
        str: A recommendation message with a book title and information
    """
    if books_read is None:
        books_read = []

    # Convert all book titles to lowercase for case-insensitive comparison
    books_read_lower = [book.lower() for book in books_read]

    # Find unread books
    unread_books = [book for book in CAMUS_BOOKS if book["title"].lower() not in books_read_lower]

    if not unread_books:
        return "You've read all of Camus' major works! Consider re-reading your favorites."

    # Select a random unread book
    selected_book = random.choice(unread_books)

    return (
        f"I recommend reading '{selected_book['title']}' ({selected_book['year']}), "
        f"a {selected_book['genre'].lower()}. It's one of Camus' most "
        "celebrated works!"
    )
