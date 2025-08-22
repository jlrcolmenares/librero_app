"""Unit tests for the librero recommender module."""

import unittest
from librero.recommender import recommend_book, filter_books, CAMUS_BOOKS, DEFAULT_RECOMMENDATION


class TestRecommenderModule(unittest.TestCase):
    """Test cases for the recommender functionality."""

    def test_default_recommendation_when_no_books_read(self):
        """Test that default recommendation is returned when no books are provided."""
        result = recommend_book()
        self.assertEqual(result, DEFAULT_RECOMMENDATION)
        
        result = recommend_book([])
        self.assertEqual(result, DEFAULT_RECOMMENDATION)

    def test_recommendation_with_books_read(self):
        """Test recommendation logic when books have been read."""
        # Test with The Stranger read
        result = recommend_book(["The Stranger"])
        self.assertEqual(result, "The Plague")
        
        # Test with multiple books read
        result = recommend_book(["The Stranger", "The Plague"])
        self.assertEqual(result, "The Fall")
        
        # Test with famous books read
        result = recommend_book(["The Stranger", "The Plague", "The Fall"])
        self.assertEqual(result, "The Myth of Sisyphus")

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
