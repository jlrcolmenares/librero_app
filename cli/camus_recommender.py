#!/usr/bin/env python3
from typing import List, Optional

import typer  # type: ignore[import-not-found]
from rich.console import Console  # type: ignore[import-not-found]
from rich.table import Table  # type: ignore[import-not-found]

from librero.recommender import CAMUS_BOOKS, Book, recommend_book

app = typer.Typer()
console = Console()


def display_books(books: List[Book], title: str = "Albert Camus' Books") -> None:
    """Display books in a formatted table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Title", style="cyan")
    table.add_column("Year", justify="right")
    table.add_column("Genre")
    for book in books:
        table.add_row(book["title"], str(book["year"]), book["genre"])
    console.print(table)


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
    console.print("\n[bold blue]Welcome to the Camus Book Recommender![/bold blue]")
    console.print("Press Enter to get a recommendation or 'q' to quit\n")

    # Normalize the read list up-front
    read_books: List[str] = read or []

    while True:
        user_input = input("Press Enter for a recommendation (or 'q' to quit): ")
        if user_input.lower() == "q":
            break

        recommendation = recommend_book(read_books)
        if recommendation.startswith("You've read all"):
            console.print(f"\n[bold red]{recommendation}[/bold red]\n")
            break

        console.print("\n[bold green]I recommend:[/bold green]")
        console.print(f"[bold yellow]{recommendation}[/bold yellow]\n")

        read_books.append(recommendation)
        console.print(f"Books read so far: {', '.join(read_books) if read_books else 'None'}\n")


@app.command()  # type: ignore[misc]
def list_books() -> None:
    """List all available books by Albert Camus."""
    display_books(CAMUS_BOOKS)


if __name__ == "__main__":
    app()
