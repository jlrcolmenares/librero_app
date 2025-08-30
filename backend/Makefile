PYTHON := python3
VENV_DIR := .venv

# Run tests
pytest:
	PYTHONPATH=.. pytest -v --cov=librero --cov=cli tests/

# Run tests with coverage report
test: pytest
	coverage report -m

# Install pre-commit hooks
pre-commit-install:
	pre-commit install

# Run pre-commit on all files
pre-commit-run: pre-commit-install
	pre-commit run --all-files

# Alias for pre-commit-run
pre-commit: pre-commit-run

# Clean up
clean:
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf htmlcov/
