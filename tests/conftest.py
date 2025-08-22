"""Test configuration and fixtures for pytest."""

import os
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test configuration
import pytest


@pytest.fixture
def sample_books_read():
    """Fixture providing sample list of read books."""
    return ["The Stranger", "The Plague"]


@pytest.fixture
def all_camus_books():
    """Fixture providing all Camus books for testing."""
    from librero.recommender import CAMUS_BOOKS

    return CAMUS_BOOKS


@pytest.fixture
def cli_runner():
    """Fixture providing Click CLI test runner."""
    from click.testing import CliRunner

    return CliRunner()
