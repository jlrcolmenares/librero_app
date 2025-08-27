# Librero App

A web application and CLI tool that recommends books by Albert Camus based on what you have already read.

## Features
- Web interface for getting book recommendations
- CLI tool for command-line recommendations
- Tracks reading history
- Smart recommendations based on unread books
- Full type checking and test coverage

## Requirements
- Python 3.13+
- pipenv (for dependency management)

## Setup
Run the setup:
```sh
make setup
```

## Usage

### CLI Interface
This is a CLI interface made with Typer. Run it with:

```sh
make run
```

### Web Interface
To start the web server and use the SPA interface:

```sh
make web
```
Then visit http://localhost:8000 in your browser.

### Development
Run the test suite:
```sh
make test
```

Run pre-commit hooks on all files:
```sh
make pre-commit
```

## Clean Up
Remove the virtual environment:
```sh
make clean
```

## Project Structure

```
├── cli/                    # CLI application
│   └── camus_recommender.py  # Main CLI interface
├── librero/               # Core library
│   └── recommender.py       # Book recommendation logic
├── tests/                 # Test suite
│   ├── test_cli.py         # CLI tests
│   ├── test_recommender.py  # Core logic tests
│   └── test_web.py         # Web API tests
├── web/                   # Web application
│   ├── static/             # Static assets
│   │   ├── app.js          # Frontend JavaScript
│   │   ├── index.html      # Main SPA page
│   │   └── style.css       # Styling
│   └── app.py             # FastAPI backend
├── Makefile              # Build automation
├── Pipfile               # Dependencies
├── Pipfile.lock          # Locked dependencies
└── pyproject.toml        # Project configuration
```

## Dependencies

### Production
- FastAPI - Web framework
- Typer - CLI interface
- Pydantic - Data validation
- uvicorn - ASGI server

### Development
- pytest - Testing
- mypy - Type checking
- ruff - Linting
- isort - Import sorting
- pre-commit - Git hooks

---

Feel free to contribute or suggest improvements!
