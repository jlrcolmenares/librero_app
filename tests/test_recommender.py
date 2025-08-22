"""Unit tests for the librero.recommender module."""

import pytest
from unittest.mock import patch, MagicMock
from librero.recommender import recommend_book, CAMUS_BOOKS

def test_recommend_book_returns_string():
    """Test that recommend_book returns a string."""
    result = recommend_book()
    assert isinstance(result, str)

def test_recommend_book_with_no_books_read():
    """Test that recommend_book returns a book when no books are read."""
    result = recommend_book()
    assert result in [book["title"] for book in CAMUS_BOOKS]

def test_recommend_book_with_all_books_read():
    """Test that recommend_book handles case when all books are read."""
    all_books = [book["title"] for book in CAMUS_BOOKS]
    result = recommend_book(all_books)
    assert result == "You've read all of Camus' major works! Consider re-reading your favorites."

@patch('librero.recommender.random.choice')
def test_recommendation_uses_random_choice(mock_choice):
    """Test that recommendation uses random.choice for selection."""
    test_book = {"title": "Test Book", "year": 2000, "genre": "Test"}
    mock_choice.return_value = test_book
    result = recommend_book()
    assert result == test_book["title"]
    mock_choice.assert_called()

def test_recommend_book_case_insensitive():
    """Test that book matching is case insensitive."""
    result = recommend_book(["the stranger"])
    assert result != "The Stranger"  # Should recommend something else
    assert result in [book["title"] for book in CAMUS_BOOKS if book["title"] != "The Stranger"]

def test_camus_books_structure():
    """Test that CAMUS_BOOKS has the expected structure."""
    assert isinstance(CAMUS_BOOKS, list)
    assert len(CAMUS_BOOKS) > 0
    
    for book in CAMUS_BOOKS:
        assert "title" in book
        assert "year" in book
        assert "genre" in book
        assert isinstance(book["title"], str)
        assert isinstance(book["year"], int)
        assert isinstance(book["genre"], str)

@patch('librero.recommender.random.choice')
def test_recommend_book_with_read_books(mock_choice):
    """Test that recommend_book doesn't recommend already read books."""
    read_books = [CAMUS_BOOKS[0]["title"], CAMUS_BOOKS[1]["title"]]
    remaining_books = [book for book in CAMUS_BOOKS if book["title"] not in read_books]
    
    # Mock random.choice to return the first remaining book
    mock_choice.return_value = remaining_books[0]
    
    result = recommend_book(read_books)
    assert result == remaining_books[0]["title"]
    assert result not in read_books