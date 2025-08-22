#!/usr/bin/env python3
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional, List
from librero.recommender import recommend_book, CAMUS_BOOKS

app = typer.Typer()
console = Console()

def display_books(books: List[dict], title: str = "Albert Camus' Books") -> None:
    """Display books in a formatted table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Title", style="cyan")
    table.add_column("Year", justify="right")
    table.add_column("Genre")
    for book in books:
        table.add_row(book["title"], str(book["year"]), book["genre"])
    console.print(table)

@app.command()
def recommend(
    read: List[str] = typer.Option(
        None, "--read", "-r", 
        help="Books you've already read by Camus (can be used multiple times)"
    )
) -> None:
    """Get a random book recommendation from Albert Camus' works."""
    console.print("\n[bold blue]Welcome to the Camus Book Recommender![/bold blue]")
    console.print("Press Enter to get a recommendation or 'q' to quit\n")
    
    while True:
        user_input = input("Press Enter for a recommendation (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
            
        recommendation = recommend_book(read)
        if recommendation.startswith("You've read all"):
            console.print(f"\n[bold red]{recommendation}[/bold red]\n")
            break
            
        console.print(f"\n[bold green]I recommend:[/bold green]")
        console.print(f"[bold yellow]{recommendation}[/bold yellow]\n")
        
        if read is None:
            read = []
        read.append(recommendation)
        console.print(f"Books read so far: {', '.join(read) if read else 'None'}\n")

@app.command()
def list_books() -> None:
    """List all available books by Albert Camus."""
    display_books(CAMUS_BOOKS)

if __name__ == "__main__":
    app()
