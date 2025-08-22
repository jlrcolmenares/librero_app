import random
from typing import List, Dict

# Collection of Albert Camus' notable works
CAMUS_BOOKS = [
    {"title": "The Stranger", "year": 1942, "genre": "Philosophical fiction"},
    {"title": "The Plague", "year": 1947, "genre": "Philosophical novel"},
    {"title": "The Fall", "year": 1956, "genre": "Philosophical fiction"},
    {"title": "The Myth of Sisyphus", "year": 1942, "genre": "Philosophical essay"},
    {"title": "The Rebel", "year": 1951, "genre": "Philosophical essay"},
    {"title": "A Happy Death", "year": 1971, "genre": "Philosophical fiction"},
    {"title": "The First Man", "year": 1994, "genre": "Autobiographical novel"},
]

def recommend_book(books_read: List[str] = None) -> str:
    """
    Recommends a random book by Albert Camus.
    If books_read is provided, only recommends books that haven't been read yet.
    """
    if not books_read:
        return random.choice(CAMUS_BOOKS)["title"]
        
    books_read_lower = [book.lower() for book in books_read]
    unread_books = [
        book for book in CAMUS_BOOKS 
        if book["title"].lower() not in books_read_lower
    ]
    
    if not unread_books:
        return "You've read all of Camus' major works! Consider re-reading your favorites."
        
    return random.choice(unread_books)["title"]
