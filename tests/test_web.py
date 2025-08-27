"""Tests for the web API endpoints."""
from fastapi.testclient import TestClient

from web.app import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "librero-recommender"}


def test_get_recommendation_no_books():
    """Test getting a recommendation with no books read."""
    response = client.post("/api/recommend")
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "message" in data
    assert "total_books" in data
    assert data["total_books"] == 7  # Current number of Camus books


def test_get_recommendation_with_books():
    """Test getting a recommendation with some books read."""
    response = client.post(
        "/api/recommend",
        json={"books_read": ["The Stranger", "The Plague"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["recommendation"] not in ["The Stranger", "The Plague"]
    assert "message" in data
    assert data["total_books"] == 7


def test_get_recommendation_all_books():
    """Test getting a recommendation when all books are read."""
    all_books = [
        "The Stranger", "The Plague", "The Fall",
        "The Myth of Sisyphus", "The Rebel",
        "The First Man", "A Happy Death"
    ]
    response = client.post(
        "/api/recommend",
        json={"books_read": all_books}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["recommendation"] == "No recommendation available"
    assert "read everything" in data["message"].lower()
    assert data["total_books"] == 7


def test_serve_spa():
    """Test serving the SPA."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
