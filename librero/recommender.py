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

DEFAULT_RECOMMENDATION = "The Stranger"

def recommend_book(books_read: List[str] = None) -> str:
    """
    Recommends a book by Albert Camus based on what the user has already read.
    """
    if not books_read:
        return DEFAULT_RECOMMENDATION
    books_read_lower = [book.lower() for book in books_read]
    unread_books = [
        book for book in CAMUS_BOOKS 
        if book["title"].lower() not in books_read_lower
    ]
    if not unread_books:
        return "You've read all of Camus' major works! Consider re-reading your favorites."
    famous_order = ["The Stranger", "The Plague", "The Fall", "The Myth of Sisyphus"]
    for title in famous_order:
        if title.lower() not in books_read_lower:
            return title
    return unread_books[0]["title"]

def filter_books(title: str = None, year: int = None, genre: str = None) -> List[Dict[str, str]]:
    filtered_books = CAMUS_BOOKS
    if title:
        filtered_books = [b for b in filtered_books if title.lower() in b["title"].lower()]
    if year:
        filtered_books = [b for b in filtered_books if b["year"] == year]
    if genre:
        filtered_books = [b for b in filtered_books if genre.lower() in b["genre"].lower()]
    return filtered_books
