from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from librero.recommender import Book, recommend_book, get_books_from_db
from pydantic import BaseModel

# Initialize FastAPI app with metadata for OpenAPI docs
app = FastAPI(
    title="Librero API",
    description="A book recommendation service for Albert Camus works",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    """Request model for book recommendations."""
    books_read: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "books_read": ["The Stranger", "The Plague"]
            }
        }

class RecommendResponse(BaseModel):
    """Response model for book recommendations."""
    recommendation: str
    message: str
    total_books: int

    class Config:
        json_schema_extra = {
            "example": {
                "recommendation": "The Fall",
                "message": "Next up: 'The Fall' (1956), a philosophical fiction. 4 more books to explore!",
                "total_books": 7
            }
        }

@app.get("/health",
    summary="Health Check",
    description="Returns the health status of the API",
    response_description="Health status of the API")
async def health_check() -> Dict[str, str]:
    """Check if the API is healthy."""
    return {"status": "healthy", "service": "librero-recommender"}

@app.post("/api/recommend",
    summary="Get Book Recommendation",
    description="Returns a recommended book by Albert Camus based on what you've already read",
    response_model=RecommendResponse,
    responses={
        200: {
            "description": "Successful recommendation",
            "content": {
                "application/json": {
                    "example": {
                        "recommendation": "The Fall",
                        "message": "Next up: 'The Fall' (1956), a philosophical fiction. 4 more books to explore!",
                        "total_books": 7
                    }
                }
            }
        },
        400: {
            "description": "All books have been read",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You've read all of Camus' major works! Consider re-reading your favorites."
                    }
                }
            }
        }
    })
async def get_recommendation(request: RecommendRequest) -> RecommendResponse:
    """
    Get a book recommendation based on previously read books.

    Args:
        request: RecommendRequest containing list of books already read

    Returns:
        RecommendResponse with book recommendation and status

    Raises:
        HTTPException: If all books have been read
    """
    # Get total number of books from database
    try:
        db_books = get_books_from_db()
        total_books = len(db_books) if db_books else 0
        if not total_books:
            return RecommendResponse(
                recommendation="No books available",
                message="No books found in the database",
                total_books=0
            )
    except Exception as e:
        return RecommendResponse(
            recommendation="Error",
            message=f"Failed to fetch books: {str(e)}",
            total_books=0
        )

    # Validate book titles against database
    try:
        db_books = get_books_from_db()
        known_titles = {title.lower() for title, _ in db_books}
        unknown_titles = [title for title in request.books_read if title.lower() not in known_titles]
        if unknown_titles:
            return RecommendResponse(
                recommendation="No recommendation available",
                message=f"Unknown book title(s): {', '.join(unknown_titles)}",
                total_books=total_books
            )
    except Exception as e:
        return RecommendResponse(
            recommendation="Error",
            message=f"Failed to validate book titles: {str(e)}",
            total_books=total_books
        )

    # Get recommendation
    book: Book = recommend_book(request.books_read)
    remaining_books = total_books - len(request.books_read)

    # Handle all books read case
    if remaining_books <= 0:
        return RecommendResponse(
            recommendation="No recommendation available",
            message="You've read all of Camus' major works! Time for a re-read.",
            total_books=total_books
        )

    # Return recommendation
    return RecommendResponse(
        recommendation=book.title,
        message=f"Next up: '{book.title}' ({book.year}), a {book.genre.lower()}. {remaining_books - 1} more books to explore!",
        total_books=total_books
    )

@app.get("/api/books")
def list_books(limit: int = 5):
    """Get a list of books from the database.
    
    Args:
        limit: Maximum number of books to return (default: 5)
        
    Returns:
        dict: A dictionary containing a list of books with their titles and authors
    """
    try:
        books = get_books_from_db(limit)
        return {"books": [{"title": title, "authors": authors} for title, authors in books]}
    except Exception as e:
        return {"error": f"Failed to fetch books: {str(e)}"}
