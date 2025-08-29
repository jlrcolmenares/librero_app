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
from fastapi.responses import HTMLResponse
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


@app.get("/")
async def serve_spa() -> HTMLResponse:
    """Serve the main app HTML"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Librero - Camus Book Recommender</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Librero</h1>
            <p class="subtitle">Discover your next Albert Camus book</p>

            <button id="recommendBtn" class="recommend-btn">
                Recommend a Book
            </button>

            <div id="loading" class="loading">
                Getting your recommendation...
            </div>

            <div id="recommendations">
                <div id="currentRecommendation" class="recommendation">
                    <h3>Current Recommendation</h3>
                    <p id="recommendationText"></p>
                </div>
                <div id="recommendationHistory" class="recommendation-history">
                    <h3>Previous Books</h3>
                    <ul id="historyList"></ul>
                </div>
            </div>

            <div id="error" class="error">
                <p id="errorText"></p>
            </div>

            <div class="footer">
                <p>Powered by the wisdom of Albert Camus</p>
            </div>
        </div>

        <script>
            // Initialize state
            const previousBooks = [];

            // Get DOM elements
            const recommendBtn = document.getElementById('recommendBtn');
            const loading = document.getElementById('loading');
            const currentRecommendation = document.getElementById('currentRecommendation');
            const historyList = document.getElementById('historyList');
            const recommendationText = document.getElementById('recommendationText');
            const error = document.getElementById('error');
            const errorText = document.getElementById('errorText');

            // Hide all result elements initially
            function hideAllResults() {
                loading.style.display = 'none';
                currentRecommendation.style.display = 'none';
                error.style.display = 'none';
            }

            // Function to get recommendation from the API
            async function getRecommendation() {
                // Prevent multiple clicks
                if (recommendBtn.disabled) return;

                // Reset any previous state
                hideAllResults();
                error.style.display = 'none';
                loading.style.display = 'block';
                recommendBtn.disabled = true;
                recommendBtn.textContent = 'Finding your next book...';

                try {
                    // Make API call to our FastAPI backend
                    const response = await fetch('/api/recommend', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            books_read: previousBooks
                        })
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();

                    // Update UI with recommendation
                    hideAllResults();
                    currentRecommendation.style.display = 'block';
                    recommendationText.textContent = data.message;

                    // Calculate remaining books
                    const remainingBooks = data.total_books - previousBooks.length;

                    // Enable button for next recommendation unless all books are read
                    if (remainingBooks <= 0) {
                        recommendBtn.textContent = 'All Books Read!';
                        recommendBtn.disabled = true;
                    } else {
                        recommendBtn.textContent = `Get Next Book (${remainingBooks} remaining)`;
                        recommendBtn.disabled = false;
                    }

                    // Add to history if it's a valid book recommendation
                    if (data.recommendation !== 'No recommendation available') {
                        const historyItem = document.createElement('li');
                        historyItem.textContent = data.recommendation;
                        historyList.insertBefore(historyItem, historyList.firstChild);

                        // Add to previous books if not already there
                        if (!previousBooks.includes(data.recommendation)) {
                            previousBooks.push(data.recommendation);
                        }
                    }

                } catch (err) {
                    // Hide loading and show error
                    hideAllResults();
                    errorText.textContent = `Sorry, something went wrong: ${err.message}`;
                    error.style.display = 'block';
                    console.error('Error getting recommendation:', err);
                    // Reset button on error
                    recommendBtn.disabled = false;
                    recommendBtn.textContent = 'Try Again';
                }
            }

            // Add click event listener to the button
            recommendBtn.addEventListener('click', getRecommendation);

            // Optional: Allow Enter key to trigger recommendation
            document.addEventListener('keypress', function(event) {
                if (event.key === 'Enter' && !recommendBtn.disabled) {
                    getRecommendation();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "librero-recommender"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
