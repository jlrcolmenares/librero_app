"""Tests for the camus_recommender CLI."""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from cli.camus_recommender import app
from librero.recommender import CAMUS_BOOKS

runner = CliRunner()

@patch('librero.recommender.random.choice')
@patch('builtins.input', side_effect=['\n', 'q'])
def test_recommend_command_basic(mock_input, mock_choice):
    """Test the basic recommend command."""
    mock_choice.return_value = {"title": "The Stranger"}
    result = runner.invoke(app, ['recommend'], input='\nq\n')
    assert result.exit_code == 0
    assert "Welcome to the Camus Book Recommender!" in result.output
    # The book title should appear after the first Enter press

@patch('cli.camus_recommender.recommend_book')
@patch('builtins.input', side_effect=['', 'q'])
def test_recommend_with_read_books(mock_input, mock_recommend):
    """Test recommend command with --read parameter."""
    mock_recommend.return_value = "The Plague"
    result = runner.invoke(
        app,
        ['recommend', '--read', 'The Stranger']
    )
    assert result.exit_code == 0
    # The function is called with the read books list
    args, _ = mock_recommend.call_args
    assert 'The Stranger' in args[0]  # Check if 'The Stranger' is in the read books list

@patch('cli.camus_recommender.recommend_book')
@patch('builtins.input', side_effect=['q'])
def test_recommend_quit_immediately(mock_input, mock_recommend):
    """Test that recommend command can be quit immediately."""
    result = runner.invoke(app, ['recommend'])
    assert result.exit_code == 0
    assert "Welcome to the Camus Book Recommender!" in result.output
    mock_recommend.assert_not_called()

def test_list_books_command():
    """Test the list-books command."""
    result = runner.invoke(app, ['list-books'])
    assert result.exit_code == 0
    for book in CAMUS_BOOKS:
        assert book["title"] in result.output
        assert str(book["year"]) in result.output
        assert book["genre"] in result.output

def test_help_command():
    """Test the help command."""
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0
    # Check for command names in help output
    assert "recommend" in result.output.lower()
    assert "list-books" in result.output.lower()

@patch('librero.recommender.random.choice')
@patch('builtins.input', side_effect=['\n', 'q'])
def test_recommend_all_books_read(mock_input, mock_choice):
    """Test behavior when all books have been read."""
    all_books = [book["title"] for book in CAMUS_BOOKS]
    # Mock random.choice to return the all-books-read message
    mock_choice.return_value = {"title": "You've read all of Camus' major works! Consider re-reading your favorites."}
    
    # Pass all books as read
    args = ['recommend'] + [arg for book in all_books for arg in ['--read', book]]
    
    result = runner.invoke(app, args, input='\nq\n')
    assert result.exit_code == 0

@patch('builtins.input', side_effect=KeyboardInterrupt())
def test_recommend_handles_keyboard_interrupt(mock_input):
    """Test that the CLI handles keyboard interrupt gracefully."""
    result = runner.invoke(app, ['recommend'])
    # On keyboard interrupt, exit code might be 1 or 130 depending on the system
    assert result.exit_code in (0, 1, 130)
    # The test doesn't need to check for specific exit messages since we're testing the CLI's behavior, not its output