#!/usr/bin/env python3
from typing import List, Optional

import typer  # type: ignore[import-not-found]
from librero.recommender import CAMUS_BOOKS, Book, recommend_book

app = typer.Typer()


def display_books(books: List[Book], title: str = "Albert Camus' Books") -> None:
    """Display books in a simple text list using typer."""
    typer.echo(title)
    typer.echo("-" * len(title))
    for book in books:
        typer.echo(f"Title: {book.title} | Year: {book.year} | Genre: {book.genre}")


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

        try:
            # Get a recommendation
            result = recommend_book(read_books)

            # Format the recommendation message
            recommendation = (
                f"I recommend reading: '{result.title}' ({result.year}), "
                f"a {result.genre.lower()}. It's one of Camus' most celebrated works!"
            )
            typer.echo(f"{recommendation}\n")

            # Add the book to read books if not already there
            if result.title not in read_books:
                read_books.append(result.title)
            typer.echo(f"Books read so far: {', '.join(read_books) if read_books else 'None'}\n")
        except ValueError as e:
            typer.echo(f"{str(e)}\n")


@app.command()  # type: ignore[misc]
def list_books() -> None:
    """List all available books by Albert Camus."""
    display_books(CAMUS_BOOKS)


if __name__ == "__main__":  # pragma: no cover
    app()  # pragma: no cover
