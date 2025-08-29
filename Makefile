# Makefile for Camus Recommender CLI

VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: venv setup test run clean pre-commit-install pre-commit-run web

venv:
	python3 -m venv $(VENV_DIR)

setup:
	pipenv install --dev
	pip install pre-commit
	pre-commit install

# Run tests
pytest:
	pytest -v --cov=librero --cov=cli tests/

# Run tests with coverage report
test: pytest
	coverage report -m

# Run the CLI
run:
	PYTHONPATH=. $(PYTHON) -m cli.camus_recommender recommend

# Install pre-commit hooks
pre-commit-install:
	pre-commit install

# Run pre-commit on all files
pre-commit-run: pre-commit-install
	pre-commit run --all-files

# Alias for pre-commit-run
pre-commit: pre-commit-run

# Start web server for local development
web:
	@echo "Starting Librero web server (local development)..."
	@echo "Visit http://localhost:8080 to use the book recommender"
	cd web && PYTHONPATH=.. pipenv run python app.py

# Start with Docker Compose
docker:
	@echo "Starting Librero with Docker Compose..."
	@echo "Visit http://localhost to use the book recommender"
	docker compose up --build

# Clean up
clean:
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf htmlcov/
