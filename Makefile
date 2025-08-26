# Makefile for Camus Recommender CLI

VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: venv setup run clean web

venv:
	python3 -m venv $(VENV_DIR)

setup: venv
	. $(VENV_DIR)/bin/activate && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt

run_cli:
	PYTHONPATH=. $(PYTHON) -m cli.camus_recommender recommend

web:
	@echo "Starting Librero web server..."
	@echo "Visit http://localhost:8000 to use the book recommender"
	cd web && PYTHONPATH=.. ../$(PYTHON) app.py

clean:
	rm -rf $(VENV_DIR)
