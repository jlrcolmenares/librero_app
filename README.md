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

## Development Guide

### Core Concepts
- Book recommendations are handled by `librero/recommender.py`
- Books are stored as dataclass objects with title, year, and genre
- Recommendations avoid previously read books
- Case-insensitive book title matching

### Data Model
```python
@dataclass
class Book:
    title: str
    year: int
    genre: str
```

### Extensibility Points
1. Adding New Books
   - Extend `CAMUS_BOOKS` in `recommender.py`
   - Each book needs title, year, and genre

2. New Recommendation Logic
   - Modify `recommend_book()` in `recommender.py`
   - Current: Random selection from unread books
   - Possible: Genre-based, chronological, or difficulty-based

3. User Preferences
   - Could extend `Book` dataclass with new fields
   - Add preference filters to recommendation logic

### Adding Features
1. Core Logic
   - Add new features to `librero/recommender.py`
   - Ensure 100% test coverage in `tests/test_recommender.py`
   - Use type hints and docstrings

2. CLI Features
   - Extend `cli/camus_recommender.py`
   - Follow Typer's command pattern
   - Add tests in `tests/test_cli.py`

3. Web Features
   - Backend: Add endpoints to `web/app.py`
   - Frontend: Modify `web/static/app.js`
   - Add tests in `tests/test_web.py`

### API and Data Flow
1. Web Endpoints
   ```python
   # Main recommendation endpoint
   POST /api/recommend
   Request: { "books_read": ["string"] }
   Response: {
     "recommendation": "string",
     "message": "string",
     "total_books": int
   }

   # Health check
   GET /health
   Response: { "status": "healthy", "service": "librero-recommender" }
   ```

2. Data Flow
   - Frontend (`app.js`) → API (`app.py`) → Core Logic (`recommender.py`)
   - All book operations are case-insensitive
   - Validation happens at API level using Pydantic
   - Error handling for unknown/invalid books

### Quality Standards
- All code must pass `make pre-commit` (ruff, mypy, isort)
- New features require tests
- Maintain >95% test coverage
- Follow existing code style

Feel free to contribute or suggest improvements!
