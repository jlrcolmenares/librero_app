#!/usr/bin/env python3
"""
FastAPI backend for the Librero book recommender SPA.
Exposes a single endpoint to get book recommendations.
"""

import logging
import os
import sys
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from librero.recommender import CAMUS_BOOKS, has_read_all_books, recommend_book

# Add the parent directory to the path so we can import from librero
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


app = FastAPI(title="Librero Book Recommender", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Response model for the API
class RecommendationResponse(BaseModel):
    recommendation: str
    message: str
    total_books: int

# Request model (optional, for future extensibility)
class RecommendationRequest(BaseModel):
    books_read: List[str]

    class Config:
        extra = "forbid"

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendation(request: RecommendationRequest) -> RecommendationResponse:
    """
    Get a book recommendation using the existing recommend_book logic.

    Returns:
        JSON with recommendation string and a user-friendly message
    """
    # Extract books_read from request, default to empty list for simple recommendation
    books_read = request.books_read if request.books_read else []

    try:
        logger.info(f"Received recommendation request with books_read: {books_read}")
        # Use the existing recommendation logic
        result = recommend_book(books_read)
        logger.info(f"Generated recommendation: {result}")
        remaining = len(CAMUS_BOOKS) - len(books_read)
        message = (
            f"Next up: '{result.title}' ({result.year}), "
            f"a {result.genre.lower()}. {remaining} more books to explore!"
        )
        return RecommendationResponse(
            recommendation=result.title,
            message=message,
            total_books=len(CAMUS_BOOKS)
        )
    except ValueError as e:
        if has_read_all_books(books_read):
            message = "You've read all of Camus' major works! Time for a re-read."
        else:
            message = str(e)
        return RecommendationResponse(
            recommendation="No recommendation available",
            message=message,
            total_books=len(CAMUS_BOOKS)
        )



@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "librero-recommender"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
