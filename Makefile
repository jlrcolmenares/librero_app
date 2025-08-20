# Makefile for Camus Recommender CLI

VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: venv install run clean

venv:
	python3 -m venv $(VENV_DIR)

setup: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) camus_recommender.py recommend

clean:
	rm -rf $(VENV_DIR)
