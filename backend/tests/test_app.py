"""Tests for the web API endpoints."""
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "librero-recommender"}


def test_get_recommendation_no_books():
    """Test getting a recommendation with no books read."""
    response = client.post("/api/recommend", json={"books_read": []})
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "message" in data
    assert "total_books" in data
    assert data["recommendation"] != "No recommendation available"
    assert data["total_books"] > 0
    assert isinstance(data["total_books"], int)


def test_get_recommendation_with_books():
    """Test getting a recommendation with some books read."""
    response = client.post(
        "/api/recommend",
        json={"books_read": ["The Stranger", "The Plague"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "message" in data
    assert "total_books" in data
    assert data["recommendation"] != "No recommendation available"
    assert data["total_books"] > 0
    assert isinstance(data["total_books"], int)
    assert data["recommendation"] not in ["The Stranger", "The Plague"]


def test_get_recommendation_all_books():
    """Test getting a recommendation when all books are read."""
    from librero.recommender import CAMUS_BOOKS
    all_books = [book.title for book in CAMUS_BOOKS]

    response = client.post(
        "/api/recommend",
        json={"books_read": all_books}
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "message" in data
    assert "total_books" in data
    assert data["recommendation"] == "No recommendation available"
    assert "Time for a re-read" in data["message"]
    assert data["total_books"] == len(CAMUS_BOOKS)


def test_get_recommendation_invalid_request():
    """Test getting a recommendation with invalid request body."""
    response = client.post(
        "/api/recommend",
        json={"invalid_field": []}
    )
    assert response.status_code == 422  # Unprocessable Entity

    response = client.post(
        "/api/recommend",
        json={"books_read": "not a list"}
    )
    assert response.status_code == 422  # Unprocessable Entity


def test_get_recommendation_unknown_book():
    """Test getting a recommendation with unknown book in read list."""
    response = client.post(
        "/api/recommend",
        json={"books_read": ["Unknown Book"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "message" in data
    assert "total_books" in data
    assert data["recommendation"] == "No recommendation available"
    assert "Unknown book title(s)" in data["message"]
    assert "Unknown Book" in data["message"]
    assert data["total_books"] > 0
