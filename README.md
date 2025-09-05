# Librero App

A web application and CLI tool that recommends books based on what you have already read.

## Features
- Web interface for getting book recommendations
- CLI tool for command-line recommendations
- Tracks reading history
- Smart recommendations based on unread books
- Full type checking and test coverage

## Requirements
- Python 3.12+
- pipenv (for dependency management)

## Project Structure

```
├── backend/                # Backend application
│   ├── cli/                # CLI application
│   │   └── camus_recommender.py  # Main CLI interface
│   ├── librero/           # Core library
│   │   └── recommender.py  # Book recommendation logic
│   ├── pyproject.toml     # Backend configuration
│   └── Pipfile            # Backend dependencies
├── frontend/              # Frontend application
│   ├── static/            # Static assets
│   │   ├── services/      # Frontend services
│   │   │   └── bookStorage.js  # Book storage service
│   │   ├── app.js         # Frontend JavaScript
│   │   ├── index.html     # Main SPA page
│   │   └── style.css      # Styling
│   ├── tests/             # Frontend test suite
│   │   ├── book_storage.test.js  # Book storage tests
│   │   ├── button_element.test.js  # Button tests
│   │   ├── input_element.test.js  # Input tests
│   │   └── local_storage.test.js  # LocalStorage tests
│   ├── package.json       # Frontend dependencies
│   └── .gitignore         # Frontend-specific gitignore
├── Makefile              # Build automation
├── docker-compose.yml    # Docker configuration
├── backend.Dockerfile    # Backend Docker image
├── frontend.Dockerfile   # Frontend Docker image
└── README.md             # Project documentation
```

## Local Development Environment

### Full Stack Development
- Use Docker Compose to run both frontend and backend together:
  ```sh
  make up
  ```
- This will start both services and make the application available at http://localhost
- Changes to the frontend will be reflected immediately
- Backend changes require restarting the containers

### Backend-only Development
- For backend development without Docker:
  ```sh
  cd backend
  make setup  # Install dependencies
  make test   # Run backend tests
  make run    # Run the backend server
  ```
- The backend API will be available at http://localhost:8000

### Frontend-only Development
- For frontend development without Docker:
  ```sh
  cd frontend
  npm install  # Install dependencies
  npm test     # Run frontend tests
  npm start    # Start development server
  ```
- The frontend will be available at http://localhost:3000
- You may need to configure API endpoints to point to your backend

## Development Guide

### Core Concepts
- Book recommendations are handled by `librero/recommender.py`
- Books are stored as dataclass objects with title, year, and genre
- Recommendations avoid previously read books
- Case-insensitive book title matching

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
