"""Integration tests for the CLI functionality."""

import unittest
import re
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from cli.camus_recommender import cli
from librero.recommender import CAMUS_BOOKS


def strip_ansi_codes(text):
    """Remove ANSI color codes from text for testing."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class TestCLIFunctionality(unittest.TestCase):
    """Test cases for CLI commands and validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_recommend_command_missing_current_book(self):
        """Test that recommend command requires --current parameter."""
        result = self.runner.invoke(cli, ['recommend'])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Missing option '--current'", result.output)

    def test_recommend_command_with_valid_current_book(self):
        """Test recommend command with valid current book."""
        result = self.runner.invoke(cli, ['recommend', '--current', 'The Stranger'])
        clean_output = strip_ansi_codes(result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Since you're currently reading 'The Stranger'", clean_output)
        self.assertIn("I recommend:", clean_output)

    def test_recommend_command_with_invalid_current_book(self):
        """Test recommend command with invalid current book."""
        result = self.runner.invoke(cli, ['recommend', '--current', 'Invalid Book'])
        clean_output = strip_ansi_codes(result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("'Invalid Book' is not a recognized Camus book", clean_output)
        self.assertIn("Available books:", clean_output)

    def test_recommend_command_with_current_and_read_books(self):
        """Test recommend command with current book and previously read books."""
        result = self.runner.invoke(cli, [
            'recommend', 
            '--current', 'The Stranger',
            '--read', 'The Plague',
            '--read', 'The Fall'
        ])
        clean_output = strip_ansi_codes(result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Since you're currently reading 'The Stranger'", clean_output)

    def test_recommend_command_case_insensitive_validation(self):
        """Test that current book validation is case insensitive."""
        result = self.runner.invoke(cli, ['recommend', '--current', 'the stranger'])
        clean_output = strip_ansi_codes(result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Since you're currently reading 'the stranger'", clean_output)

    def test_list_books_command(self):
        """Test list-books command functionality."""
        result = self.runner.invoke(cli, ['list-books'])
        self.assertEqual(result.exit_code, 0)
        # Should display all books
        for book in CAMUS_BOOKS:
            self.assertIn(book["title"], result.output)

    def test_list_books_with_title_filter(self):
        """Test list-books command with title filter."""
        result = self.runner.invoke(cli, ['list-books', '--title', 'Stranger'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("The Stranger", result.output)
        # Should not contain other books
        self.assertNotIn("The Plague", result.output)

    def test_list_books_with_year_filter(self):
        """Test list-books command with year filter."""
        result = self.runner.invoke(cli, ['list-books', '--year', '1942'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("The Stranger", result.output)
        self.assertIn("The Myth of Sisyphus", result.output)

    def test_list_books_with_genre_filter(self):
        """Test list-books command with genre filter."""
        result = self.runner.invoke(cli, ['list-books', '--genre', 'essay'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("The Myth of Sisyphus", result.output)
        self.assertIn("The Rebel", result.output)

    def test_list_books_no_matches(self):
        """Test list-books command when no books match criteria."""
        result = self.runner.invoke(cli, ['list-books', '--title', 'Nonexistent'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("No books match your criteria", result.output)

    def test_cli_help_command(self):
        """Test that help command works."""
        result = self.runner.invoke(cli, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("A simple CLI for recommending books by Albert Camus", result.output)

    def test_recommend_help_command(self):
        """Test help for recommend command."""
        result = self.runner.invoke(cli, ['recommend', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Your current book by Camus (required)", result.output)
        self.assertIn("Books you've already read by Camus", result.output)


class TestCLIValidationLogic(unittest.TestCase):
    """Test cases for CLI validation logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_current_book_added_to_read_list(self):
        """Test that current book is properly added to read books list."""
        # This tests the internal logic that current book gets added to books_read
        result = self.runner.invoke(cli, [
            'recommend', 
            '--current', 'The Stranger'
        ])
        self.assertEqual(result.exit_code, 0)
        # The recommendation should be different than if The Stranger wasn't read
        self.assertIn("The Plague", result.output)

    def test_duplicate_current_and_read_book_handling(self):
        """Test handling when current book is also in read list."""
        result = self.runner.invoke(cli, [
            'recommend', 
            '--current', 'The Stranger',
            '--read', 'The Stranger'  # Duplicate
        ])
        clean_output = strip_ansi_codes(result.output)
        self.assertEqual(result.exit_code, 0)
        # Should still work correctly
        self.assertIn("Since you're currently reading 'The Stranger'", clean_output)

    def test_valid_camus_books_recognition(self):
        """Test that all valid Camus books are recognized."""
        for book in CAMUS_BOOKS:
            result = self.runner.invoke(cli, ['recommend', '--current', book["title"]])
            self.assertEqual(result.exit_code, 0)
            self.assertNotIn("is not a recognized Camus book", result.output)


if __name__ == "__main__":
    unittest.main()
