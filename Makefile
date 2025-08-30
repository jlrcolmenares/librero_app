# Makefile for Camus Recommender CLI

VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: venv setup test run clean pre-commit-install
.PHONY: docker docker-build docker-clean

# Default target
docker: docker-build

# Build and start services
docker-build:
	@echo "Starting Librero with Docker Compose..."
	@echo "Visit http://localhost to use the book recommender"
	docker compose up --build

# Clean up docker resources
docker-clean:
	docker compose down --rmi all --volumes --remove-orphans
