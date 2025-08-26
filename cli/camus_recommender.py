#!/usr/bin/env python3
import re
from typing import List, Optional

import typer  # type: ignore[import-not-found]

from librero.recommender import CAMUS_BOOKS, Book, recommend_book

app = typer.Typer()


def display_books(books: List[Book], title: str = "Albert Camus' Books") -> None:
    """Display books in a simple text list using typer."""
    typer.echo(title)
    typer.echo("-" * len(title))
    for book in books:
        typer.echo(f"Title: {book['title']} | Year: {book['year']} | Genre: {book['genre']}")


@app.command()  # type: ignore[misc]
def recommend(
    read: Optional[List[str]] = typer.Option(
        None,
        "--read",
        "-r",
        help="Books you've already read by Camus (can be used multiple times)",
    )
) -> None:
    """Get a random book recommendation from Albert Camus' works."""
    typer.echo("\nWelcome to the Camus Book Recommender!")
    typer.echo("Press Enter to get a recommendation or 'q' to quit\n")

    # Normalize the read list up-front
    read_books: List[str] = read or []

    while True:
        user_input = input("Press Enter for a recommendation (or 'q' to quit): ")
        if user_input.lower() == "q":
            break

        recommendation = recommend_book(read_books)
        if recommendation.startswith("You've read all"):
            typer.echo(f"\n{recommendation}\n")
            break

        typer.echo("\nI recommend:")
        typer.echo(f"{recommendation}\n")

        # Extract the title from the recommendation sentence and track only titles
        match = re.search(r"I recommend reading '([^']+)'", recommendation)
        if match:
            title = match.group(1)
            if title not in read_books:
                read_books.append(title)
        typer.echo(f"Books read so far: {', '.join(read_books) if read_books else 'None'}\n")


@app.command()  # type: ignore[misc]
def list_books() -> None:
    """List all available books by Albert Camus."""
    display_books(CAMUS_BOOKS)


if __name__ == "__main__":  # pragma: no cover
    app()  # pragma: no cover
