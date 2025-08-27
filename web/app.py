#!/usr/bin/env python3
"""
FastAPI backend for the Librero book recommender SPA.
Exposes a single endpoint to get book recommendations.
"""

import os
import sys
from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from librero.recommender import CAMUS_BOOKS, has_read_all_books, recommend_book

# Add the parent directory to the path so we can import from librero
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


app = FastAPI(title="Librero Book Recommender", version="1.0.0")

# Response model for the API
class RecommendationResponse(BaseModel):
    recommendation: str
    message: str
    total_books: int

# Request model (optional, for future extensibility)
class RecommendationRequest(BaseModel):
    books_read: Optional[List[str]] = None

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendation(request: Optional[RecommendationRequest] = None) -> RecommendationResponse:
    """
    Get a book recommendation using the existing recommend_book logic.

    Returns:
        JSON with recommendation string and a user-friendly message
    """
    # Extract books_read from request, default to empty list for simple recommendation
    books_read = request.books_read if request and request.books_read else []

    try:
        # Use the existing recommendation logic
        result = recommend_book(books_read)
        message = (
            f"I recommend reading: '{result.title}' ({result.year}), "
            f"a {result.genre.lower()}. It's one of Camus' most celebrated works!"
        )
        return RecommendationResponse(
            recommendation=result.title,
            message=message,
            total_books=len(CAMUS_BOOKS)
        )
    except ValueError as e:
        if has_read_all_books(books_read):
            message = "Looks like you've read everything! Time for a re-read."
        else:
            message = str(e)
        return RecommendationResponse(
            recommendation="No recommendation available",
            message=message,
            total_books=len(CAMUS_BOOKS)
        )

# Mount static files (for serving the HTML/CSS/JS)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_spa() -> FileResponse:
    """Serve the main SPA HTML file"""
    static_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_path):
        return FileResponse(static_path)
    return {"message": "SPA not found. Please ensure static/index.html exists."}

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "librero-recommender"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
