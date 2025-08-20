# Book Recommender CLI - Librero App

A simple command-line Python application that recommends a book by Albert Camus based on what you have already read.

## Features
- Recommends a Camus book from a fixed list
- Lists all notable works by Camus
- Filters books by title, year, or genre

## Requirements
- Python 3.7+

## Setup
Clone the repository and navigate to the `librero_app` directory:

```sh
cd librero_app
```

Create a virtual environment and install dependencies:

```sh
make setup
```

## Usage

### Get a Book Recommendation
```sh
make run
```
Or run manually:
```sh
.venv/bin/python camus_recommender.py recommend
```
You can specify books you've already read:
```sh
.venv/bin/python camus_recommender.py recommend --read "The Plague" --read "The Fall"
```

### List All Books
```sh
.venv/bin/python camus_recommender.py list-books
```

## Clean Up
Remove the virtual environment:
```sh
make clean
```

## Project Structure
- `camus_recommender.py` — Main CLI application
- `requirements.txt` — Python dependencies
- `Makefile` — Automation for setup and running

---

Feel free to contribute or suggest improvements!
