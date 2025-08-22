"""Integration tests for the CLI functionality."""

import unittest
import re
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from cli.camus_recommender import app
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

    @patch('builtins.input', side_effect=['', 'q'])
    @patch('cli.camus_recommender.recommend_book')
    def test_recommend_command(self, mock_recommend, mock_input):
        """Test that recommend command works with interactive input."""
        mock_recommend.return_value = "The Stranger"
        result = self.runner.invoke(app, ['recommend'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Welcome to the Camus Book Recommender!", result.output)
        mock_recommend.assert_called_once()

    @patch('builtins.input', side_effect=['q'])
    @patch('cli.camus_recommender.recommend_book')
    def test_recommend_command_quit_immediately(self, mock_recommend, mock_input):
        """Test that recommend command can be quit with 'q'."""
        result = self.runner.invoke(app, ['recommend'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Welcome to the Camus Book Recommender!", result.output)
        mock_recommend.assert_not_called()

    @patch('builtins.input', side_effect=['', 'q'])
    @patch('cli.camus_recommender.recommend_book')
    def test_recommend_command_with_read_books(self, mock_recommend, mock_input):
        """Test recommend command with read books parameter."""
        mock_recommend.return_value = "The Plague"
        result = self.runner.invoke(app, ['recommend', '--read', 'The Stranger'])
        self.assertEqual(result.exit_code, 0)
        mock_recommend.assert_called_once_with(['The Stranger'])
        self.assertIn("Books read so far: The Stranger", result.output)
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
        result = self.runner.invoke(app, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Camus Book Recommender", result.output)
        self.assertIn("recommend", result.output)
        self.assertIn("list-books", result.output)

    def test_recommend_help_command(self):
        """Test help for recommend command."""
        result = self.runner.invoke(app, ['recommend', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Get a random book recommendation from Albert Camus' works.", result.output)
        self.assertIn("--read", result.output)
        self.assertIn("-r", result.output)


class TestCLIListCommand(unittest.TestCase):
    """Test cases for the list-books command."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_list_books_command(self):
        """Test that list-books command shows all books."""
        result = self.runner.invoke(app, ['list-books'])
        self.assertEqual(result.exit_code, 0)
        for book in CAMUS_BOOKS:
            self.assertIn(book["title"], result.output)


class TestCLIWithReadBooks(unittest.TestCase):
    """Test CLI with --read parameter."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch('builtins.input', side_effect=['', 'q'])
    @patch('cli.camus_recommender.recommend_book')
    def test_recommend_with_read_books(self, mock_recommend, mock_input):
        """Test that --read parameter is passed correctly."""
        mock_recommend.return_value = "The Fall"
        result = self.runner.invoke(
            app,
            ['recommend', '--read', 'The Stranger', '--read', 'The Plague']
        )
        self.assertEqual(result.exit_code, 0)
        mock_recommend.assert_called_once_with(['The Stranger', 'The Plague'])
        self.assertIn("Books read so far: The Stranger, The Plague", result.output)


if __name__ == "__main__":
    unittest.main()
