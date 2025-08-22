# Makefile for Camus Recommender CLI

VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: venv setup run clean

venv:
	python3 -m venv $(VENV_DIR)

setup:
	pipenv install --dev

run_cli:
	pipenv run python -m cli.camus_recommender recommend

test:
	pipenv run pytest tests/

clean:
	rm -rf $(VENV_DIR)
