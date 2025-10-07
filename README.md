# Librero App

A web application and CLI tool that recommends books based on what you have already read.

## Features
- Web interface for getting book recommendations
- CLI tool for command-line recommendations
- Tracks reading history
- Smart recommendations based on unread books
- Full type checking and test coverage

## Requirements
- Docker and Docker Compose
- Python 3.8+ (for local development)
- pipenv (for local development)
- SQLite3 (included with Python)

## Database Setup
The application uses SQLite3 for data storage. The database is automatically initialized when you first run the application.

### Database Schema
```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    authors TEXT,
    language_code TEXT,
    isbn TEXT,
    publication_date TEXT
);
```

### Initializing the Database
1. Place your `books.csv` file in the `backend/librero/data/` directory
2. Run the database initialization script:
   ```sh
   cd backend
   python3 -c "from librero.script.load_books import create_db, load_data; create_db(); load_data()"
   ```
   This will:
   - Create a new SQLite database at `backend/librero/data/books.db`
   - Load all books from the CSV file into the database

### Sample Data
For testing, you can load a small subset of the data:
```sh
python3 -c "from librero.script.load_books import create_db, load_data; create_db(); load_data(limit=50)"
```

## Setup with Docker (Recommended)
```sh
make up
```

This will:
1. Build the Docker containers
2. Set up all dependencies
3. Start both the frontend and backend services

## Local Development Setup
If you need to run the services locally without Docker:

1. Set up the backend:
```sh
cd backend
pipenv install --dev
pipenv shell
```

2. Set up the frontend:
```sh
cd ../frontend
npm install
```

## Usage

## Running the Application

### Web Interface
To start the web application:

```sh
make up
```

This will start both the frontend and backend services using Docker. Once started, you can access:
- Web interface: http://localhost
- API documentation: http://localhost/docs

### CLI Interface
For command-line usage, you can run the CLI tool directly:

```sh
cd backend
python -m cli.camus_recommender --current "The Stranger" --read "The Myth of Sisyphus"
```

#### Local Development
To run the application locally without Docker:

1. Start the backend server:
```sh
cd backend
pipenv run uvicorn librero.app:app --reload
```

2. In a new terminal, start the frontend development server:
```sh
cd frontend
npm run dev
```

3. The web interface will be available at http://localhost:8080

#### Docker Setup
Run with Docker Compose:
```sh
make docker
```
Visit http://localhost in your browser.

#### API Documentation
The API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Both provide interactive documentation where you can:
- View all endpoints and models
- Try out API calls
- See request/response examples

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
