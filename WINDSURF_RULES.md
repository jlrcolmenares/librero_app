# Librero App - Development Guide for AI Assistants

## Project Overview
A full-stack book recommendation web application with:
- **Backend**: Python FastAPI serving book recommendations from SQLite database
- **Frontend**: Vanilla JavaScript SPA with client-side routing
- **Deployment**: Docker Compose with nginx reverse proxy

---

## 🏗️ Architecture

### Tech Stack
- **Backend**: Python 3.12, FastAPI, SQLite3, Uvicorn
- **Frontend**: Vanilla JavaScript, HTML5, CSS3, nginx
- **Infrastructure**: Docker, Docker Compose
- **Package Management**: pipenv (backend), npm (frontend)

### Data Flow
```
Browser → nginx (port 80) → FastAPI (port 8000) → SQLite DB
         ↓
    Static Files (HTML/JS/CSS)
```

### Request Flow
1. User clicks "Recommend a Book" button
2. Frontend (`app.js`) calls `getRecommendation()`
3. Fetches from `/api/recommend` (proxied by nginx)
4. Backend (`app.py`) receives request
5. Backend calls `recommend_book()` in `recommender.py`
6. `recommender.py` queries SQLite database via `db.py`
7. Returns random unread book to frontend
8. Frontend displays recommendation

---

## 📁 Project Structure

```
librero_app/
├── backend/                      # Python FastAPI application
│   ├── librero/                  # Core library package
│   │   ├── __init__.py
│   │   ├── app.py               # FastAPI endpoints (MAIN API)
│   │   ├── recommender.py       # Book recommendation logic
│   │   ├── db.py                # Database connection (SQLite)
│   │   ├── data/
│   │   │   ├── books.db         # SQLite database file
│   │   │   └── books.csv        # Source data (1.5MB)
│   │   └── script/
│   │       └── load_books.py    # Database initialization
│   ├── cli/                     # CLI application
│   │   └── camus_recommender.py
│   ├── tests/                   # Backend tests
│   ├── Pipfile                  # Python dependencies
│   └── Pipfile.lock
│
├── frontend/                    # Static web application
│   ├── static/                  # All frontend files served by nginx
│   │   ├── index.html          # Landing page
│   │   ├── recommendations.html # Main app page (IMPORTANT)
│   │   ├── app.js              # Main application logic (CRITICAL)
│   │   ├── main.js             # Router initialization
│   │   ├── style.css           # Main styles
│   │   ├── landing.css         # Landing page styles
│   │   └── services/
│   │       ├── bookStorage.js  # localStorage management
│   │       └── router.js       # Client-side routing
│   ├── tests/                  # Frontend tests
│   ├── nginx.conf              # nginx configuration (IMPORTANT)
│   └── package.json
│
├── backend.Dockerfile          # Backend container definition
├── frontend.Dockerfile         # Frontend container definition
├── docker-compose.yml          # Service orchestration
├── Makefile                    # Build automation
└── README.md                   # Project documentation
```

---

## 🔑 Key Files & Their Purpose

### Backend Files

#### `backend/librero/app.py` (Main API)
- **Purpose**: FastAPI application with REST endpoints
- **Key Endpoints**:
  - `POST /api/recommend` - Get book recommendation
  - `GET /api/books?limit=N` - List books from database
  - `GET /health` - Health check
- **Important**: Uses Pydantic models for validation
- **CORS**: Enabled for all origins (change in production)

#### `backend/librero/recommender.py` (Core Logic)
- **Purpose**: Book recommendation algorithm
- **Key Functions**:
  - `get_books_from_db(limit)` - Fetches books from SQLite
  - `recommend_book(books_read)` - Returns random unread book
  - `has_read_all_books(books_read)` - Checks if all books read
- **Important**:
  - Has fallback to `CAMUS_BOOKS` if DB fails
  - Case-insensitive book matching
  - Returns `Book` dataclass with title, year, genre

#### `backend/librero/db.py` (Database)
- **Purpose**: SQLite connection management
- **Database Path**: Uses absolute path `os.path.join(BASE_DIR, "data", "books.db")`
- **Important**: Path must be absolute for Docker compatibility
- **Schema**: `books(id, title, authors, language_code, isbn, publication_date)`

### Frontend Files

#### `frontend/static/recommendations.html` (Main Page)
- **Purpose**: Main application UI
- **Key Elements**:
  - `#recommendBtn` - Trigger recommendation button
  - `#lastBookInput` - Input for adding books to history
  - `#readingHistoryList` - Display user's reading history
  - `#currentRecommendation` - Show latest recommendation
  - `#recommendations-view` - Container div (used for initialization check)
- **Scripts Loaded** (in order):
  1. `services/bookStorage.js` - Must load first
  2. `services/router.js`
  3. `app.js` - Main logic
  4. `main.js` - Router init
- **CRITICAL**: Does NOT declare `API_URL` (removed to avoid conflicts)

#### `frontend/static/app.js` (Main Logic)
- **Purpose**: Core application functionality
- **Key Variables**:
  - `API_URL = '/api'` - Base API path (proxied by nginx)
  - `previousBooks` - Array of recommended books in current session
- **Key Functions**:
  - `getRecommendation()` - Fetches recommendation from API
  - `initDomElements()` - Initializes all DOM element references
  - `addEventListeners()` - Attaches event handlers
  - `displayReadingHistory()` - Shows books from localStorage
  - `updateLastEnteredBook()` - Saves book to localStorage
- **Important**:
  - DOM elements initialized AFTER DOMContentLoaded
  - Uses `bookStorage` service for localStorage operations
  - Only initializes if `#recommendations-view` exists

#### `frontend/static/services/bookStorage.js`
- **Purpose**: localStorage abstraction layer
- **Key Methods**:
  - `saveBook(title)` - Save book, returns false if duplicate
  - `getBooks()` - Returns array of book titles
  - `clearBooks()` - Removes all books
- **Storage Key**: `librero_books`
- **Important**: Exposes `window.bookStorage` globally

#### `frontend/nginx.conf` (Reverse Proxy)
- **Purpose**: Routes requests and serves static files
- **Key Routes**:
  - `/` → serves `index.html` (landing page)
  - `/recommendations` → serves `recommendations.html`
  - `/api/*` → proxies to `http://backend:8000`
  - `/docs` → proxies to backend (Swagger UI)
- **Important**: All API calls go through nginx proxy

---

## 🐳 Docker Setup

### Services
1. **backend** (port 8000)
   - Built from `backend.Dockerfile`
   - Runs: `uvicorn app:app --host 0.0.0.0 --port 8000`
   - Volume: `./backend:/app` (live reload)

2. **frontend** (port 80)
   - Built from `frontend.Dockerfile`
   - Uses nginx:alpine
   - Volume: `./frontend/static:/usr/share/nginx/html:ro`
   - Depends on: backend

### Starting the App
```bash
# Start services
make up
# OR
docker compose up --build

# Access:
# - Frontend: http://localhost
# - API Docs: http://localhost/docs
# - Backend Direct: http://localhost:8000
```

---

## 🔧 Common Issues & Solutions

### Issue: Button Not Working
**Symptoms**: Click does nothing, console shows `getRecommendation is not defined`
**Causes**:
1. `API_URL` declared twice (HTML + JS) → Remove from HTML
2. DOM elements not initialized → Check `initDomElements()` runs
3. Scripts load in wrong order → Check HTML script tags
**Solution**: Ensure `recommendations.html` does NOT declare `API_URL`

### Issue: Database Not Found
**Symptoms**: `Error accessing database: unable to open database file`
**Cause**: Relative path in `db.py` doesn't work in Docker
**Solution**: Use absolute path with `os.path.join(BASE_DIR, "data", "books.db")`

### Issue: API Returns 404
**Symptoms**: `fetch('/api/recommend')` fails with 404
**Cause**: nginx proxy not configured or wrong path
**Solution**: Check `nginx.conf` has `location /api/` proxy rule

### Issue: CORS Errors
**Symptoms**: Browser blocks API requests
**Cause**: Frontend on different origin than API
**Solution**: nginx proxy handles this (all requests through port 80)

---

## 🧪 Testing

### Manual Frontend Test
```javascript
// In browser console on http://localhost/recommendations

// 1. Check button exists
console.log(document.getElementById('recommendBtn'));

// 2. Check bookStorage loaded
console.log(typeof bookStorage); // should be 'object'

// 3. Test API directly
fetch('/api/recommend', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({books_read: []})
}).then(r => r.json()).then(console.log);

// 4. Trigger recommendation
getRecommendation();
```

### Backend API Test
```bash
# Health check
curl http://localhost:8000/health

# List books
curl http://localhost:8000/api/books?limit=5

# Get recommendation
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"books_read": []}'
```

---

## 📝 Development Workflow

### Making Frontend Changes
1. Edit files in `frontend/static/`
2. Changes are live (nginx volume mount)
3. Refresh browser (Ctrl+Shift+R for hard refresh)

### Making Backend Changes
1. Edit files in `backend/`
2. Restart backend: `docker compose restart backend`
3. Check logs: `docker compose logs backend --tail 20`

### Database Changes
1. Modify `backend/librero/data/books.db` or CSV
2. Restart backend to pick up changes
3. Or run: `python -c "from librero.script.load_books import create_db, load_data; create_db(); load_data()"`

---

## 🎯 API Endpoints Reference

### POST /api/recommend
**Purpose**: Get book recommendation
**Request**:
```json
{
  "books_read": ["The Stranger", "The Plague"]
}
```
**Response**:
```json
{
  "recommendation": "The Fall",
  "message": "Next up: 'The Fall' (1956), a philosophical fiction. 4 more books to explore!",
  "total_books": 7
}
```

### GET /api/books?limit=N
**Purpose**: List books from database
**Response**:
```json
{
  "books": [
    {"title": "The Stranger", "authors": "Albert Camus"},
    {"title": "The Plague", "authors": "Albert Camus"}
  ]
}
```

### GET /health
**Purpose**: Health check
**Response**:
```json
{
  "status": "healthy",
  "service": "librero-recommender"
}
```

---

## 🚨 Critical Rules for AI Assistants

1. **NEVER declare `API_URL` in HTML files** - Only in `app.js`
2. **ALWAYS use absolute paths in `db.py`** - Docker needs them
3. **Check `#recommendations-view` exists** before initializing app.js
4. **Load `bookStorage.js` BEFORE `app.js`** - Dependency requirement
5. **Use `/api` prefix for all API calls** - nginx proxy requirement
6. **Restart backend after Python changes** - No hot reload
7. **Hard refresh browser after JS changes** - Cache issues
8. **Check Docker logs for errors** - `docker compose logs backend`
9. **Preserve folder structure** - Don't reorganize without user approval
10. **Test in browser console first** - Faster than full deployments

---

## 📚 Database Information

- **File**: `backend/librero/data/books.db`
- **Size**: ~2.1 MB
- **Records**: 10+ books (expandable)
- **Schema**: SQLite3 with books table
- **Initialization**: Auto-creates and populates if empty
- **Fallback**: Uses `CAMUS_BOOKS` constant if DB unavailable

---

## 🔄 State Management

### Frontend State
- **Reading History**: Stored in `localStorage` as `librero_books` (JSON array)
- **Current Session**: `previousBooks` array in `app.js` (recommendations shown)
- **Persistence**: Only reading history persists across sessions

### Backend State
- **Stateless**: No session management
- **Database**: Single source of truth for available books
- **No user accounts**: All users see same book pool

---

## 🎨 UI Components

### Key CSS Classes
- `.recommend-btn` - Main action button
- `.book-input` - Text input for book titles
- `.loading` - Loading state indicator
- `.recommendation` - Recommendation display card
- `.error` - Error message display

### Responsive Design
- Mobile-first approach
- Breakpoints in `style.css`
- Navigation adapts to screen size

---

## 🔐 Security Notes

- **CORS**: Currently allows all origins (change for production)
- **Input Validation**: Pydantic models validate API inputs
- **SQL Injection**: Protected by parameterized queries
- **XSS**: Minimal risk (no user-generated HTML rendering)
- **API Keys**: None required (public API)

---

## 📦 Dependencies

### Backend (Pipfile)
- fastapi
- uvicorn
- pydantic
- sqlite3 (built-in)

### Frontend (package.json)
- No runtime dependencies (vanilla JS)
- Dev dependencies for testing

---

## 🎓 Learning Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- SQLite Docs: https://www.sqlite.org/docs.html
- nginx Docs: https://nginx.org/en/docs/

---

## 📞 Quick Reference Commands

```bash
# Start app
make up

# Stop app
docker compose down

# View logs
docker compose logs -f

# Restart backend
docker compose restart backend

# Rebuild everything
docker compose up --build --force-recreate

# Clean up
make clean

# Run backend tests
cd backend && pipenv run pytest

# Run frontend tests
cd frontend && npm test
```

---

**Last Updated**: 2025-10-07
**Version**: 1.0
**Maintained by**: Development Team
