#!/usr/bin/env python3
"""
FastAPI backend for the Librero book recommender SPA.
Exposes a single endpoint to get book recommendations.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Add the parent directory to the path so we can import from librero
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from librero.recommender import recommend_book

app = FastAPI(title="Librero Book Recommender", version="1.0.0")

# Response model for the API
class RecommendationResponse(BaseModel):
    recommendation: str
    message: str

# Request model (optional, for future extensibility)
class RecommendationRequest(BaseModel):
    books_read: Optional[List[str]] = None

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendation(request: RecommendationRequest = None):
    """
    Get a book recommendation using the existing recommend_book logic.
    
    Returns:
        JSON with recommendation string and a user-friendly message
    """
    # Extract books_read from request, default to empty list for simple recommendation
    books_read = request.books_read if request and request.books_read else []
    
    # Use the existing recommendation logic
    recommendation = recommend_book(books_read)
    
    # Create a user-friendly message
    if recommendation == "You've read all of Camus' major works! Consider re-reading your favorites.":
        message = "Looks like you've read everything! Time for a re-read."
    else:
        message = f"I recommend: {recommendation}"
    
    return RecommendationResponse(
        recommendation=recommendation,
        message=message
    )

# Mount static files (for serving the HTML/CSS/JS)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_spa():
    """Serve the main SPA HTML file"""
    static_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_path):
        return FileResponse(static_path)
    return {"message": "SPA not found. Please ensure static/index.html exists."}

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "librero-recommender"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
