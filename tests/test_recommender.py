"""Unit tests for the librero recommender module."""

import unittest
from unittest.mock import patch
from librero.recommender import recommend_book, CAMUS_BOOKS


class TestRecommenderModule(unittest.TestCase):
    """Test cases for the recommender functionality."""

    def test_recommendation_returns_string(self):
        """Test that recommendation returns a string."""
        result = recommend_book()
        self.assertIsInstance(result, str)
    
    def test_recommendation_with_no_books_read(self):
        """Test that recommendation returns a book when no books are read."""
        result = recommend_book()
        self.assertIn(result, [book["title"] for book in CAMUS_BOOKS])

    def test_recommendation_with_all_books_read(self):
        """Test that recommendation handles case when all books are read."""
        all_books = [book["title"] for book in CAMUS_BOOKS]
        result = recommend_book(all_books)
        self.assertEqual(result, "You've read all of Camus' major works! Consider re-reading your favorites.")
    
    @patch('librero.recommender.random.choice')
    def test_recommendation_uses_random_choice(self, mock_choice):
        """Test that recommendation uses random.choice for selection."""
        mock_choice.return_value = {"title": "Test Book", "year": 2000, "genre": "Test"}
        result = recommend_book()
        self.assertEqual(result, "Test Book")
        mock_choice.assert_called()

    def test_all_books_read_scenario(self):
        """Test when all major works have been read."""
        all_titles = [book["title"] for book in CAMUS_BOOKS]
        result = recommend_book(all_titles)
        expected_message = "You've read all of Camus' major works! Consider re-reading your favorites."
        self.assertEqual(result, expected_message)

    def test_case_insensitive_book_matching(self):
        """Test that book matching is case insensitive."""
        result = recommend_book(["the stranger"])
        self.assertEqual(result, "The Plague")
        
        result = recommend_book(["THE STRANGER", "the plague"])
        self.assertEqual(result, "The Fall")

    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        result = filter_books(title="Stranger")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "The Stranger")
        
        result = filter_books(title="The")
        self.assertGreater(len(result), 1)

    def test_filter_books_by_year(self):
        """Test filtering books by publication year."""
        result = filter_books(year=1942)
        self.assertEqual(len(result), 2)  # The Stranger and The Myth of Sisyphus
        
        result = filter_books(year=1947)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "The Plague")

    def test_filter_books_by_genre(self):
        """Test filtering books by genre."""
        result = filter_books(genre="fiction")
        fiction_books = [book for book in result if "fiction" in book["genre"].lower()]
        self.assertEqual(len(result), len(fiction_books))
        
        result = filter_books(genre="essay")
        essay_books = [book for book in result if "essay" in book["genre"].lower()]
        self.assertEqual(len(result), len(essay_books))

    def test_filter_books_multiple_criteria(self):
        """Test filtering books with multiple criteria."""
        result = filter_books(year=1942, genre="fiction")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "The Stranger")

    def test_filter_books_no_matches(self):
        """Test filtering with criteria that match no books."""
        result = filter_books(title="Nonexistent Book")
        self.assertEqual(len(result), 0)
        
        result = filter_books(year=2000)
        self.assertEqual(len(result), 0)

    def test_camus_books_structure(self):
        """Test that CAMUS_BOOKS has the expected structure."""
        self.assertIsInstance(CAMUS_BOOKS, list)
        self.assertGreater(len(CAMUS_BOOKS), 0)
        
        for book in CAMUS_BOOKS:
            self.assertIn("title", book)
            self.assertIn("year", book)
            self.assertIn("genre", book)
            self.assertIsInstance(book["title"], str)
            self.assertIsInstance(book["year"], int)
            self.assertIsInstance(book["genre"], str)


if __name__ == "__main__":
    unittest.main()
