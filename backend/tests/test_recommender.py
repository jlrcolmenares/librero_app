"""Unit tests for the librero.recommender module."""

from unittest.mock import MagicMock, patch

import pytest

from librero.recommender import CAMUS_BOOKS, Book, has_read_all_books, recommend_book


def test_recommend_book_returns_book_object() -> None:
    """Test that recommend_book returns a Book object."""
    result = recommend_book()
    assert isinstance(result, Book)
    assert all(hasattr(result, key) for key in ['title', 'year', 'genre'])


def test_recommend_book_with_no_books_read() -> None:
    """Test that recommend_book returns a book when no books are read."""
    result = recommend_book()
    assert any(book.title == result.title for book in CAMUS_BOOKS)


def test_recommend_book_with_all_read():
    """Test recommending a book when all books have been read."""
    # Create a list of all book titles
    all_books = [book.title for book in CAMUS_BOOKS]

    # Should raise ValueError when all books are read
    with pytest.raises(ValueError) as exc_info:
        recommend_book(all_books)
    assert "read all" in str(exc_info.value).lower()


def test_has_read_all_books():
    """Test checking if all books have been read."""
    # Create a list of all book titles
    all_books = [book.title for book in CAMUS_BOOKS]

    # Test with all books read
    assert has_read_all_books(all_books) is True

    # Test with no books read
    assert has_read_all_books([]) is False

    # Test with some books read
    some_books = all_books[:-1]
    assert has_read_all_books(some_books) is False


@patch("librero.recommender.random.choice")
def test_recommendation_uses_random_choice(mock_choice: MagicMock) -> None:
    """Test that recommendation uses random.choice for selection."""
    test_book = Book(title="Test Book", year=2000, genre="Test")
    mock_choice.return_value = test_book
    result = recommend_book()
    assert result == test_book
    mock_choice.assert_called_once()


def test_recommend_book_case_insensitive() -> None:
    """Test that book matching is case insensitive."""
    result = recommend_book(["the stranger"])
    assert result.title != "The Stranger"
    assert any(book.title == result.title for book in CAMUS_BOOKS if book.title != "The Stranger")


def test_camus_books_structure() -> None:
    """Test that CAMUS_BOOKS has the expected structure."""
    assert isinstance(CAMUS_BOOKS, list)
    assert len(CAMUS_BOOKS) > 0

    for book in CAMUS_BOOKS:
        assert isinstance(book, Book)
        assert hasattr(book, 'title')
        assert hasattr(book, 'year')
        assert hasattr(book, 'genre')

        assert isinstance(book.title, str)
        assert isinstance(book.year, int)
        assert isinstance(book.genre, str)


@patch("librero.recommender.random.choice")
def test_recommend_book_with_read_books(mock_choice: MagicMock) -> None:
    """Test that recommend_book doesn't recommend already read books."""
    read_books = [CAMUS_BOOKS[0].title, CAMUS_BOOKS[1].title]
    remaining_books = [book for book in CAMUS_BOOKS if book.title not in read_books]

    # Mock random.choice to return the first remaining book
    mock_choice.return_value = remaining_books[0]

    result = recommend_book(read_books)
    assert result == remaining_books[0]
    assert result.title not in read_books
