#!/usr/bin/env python3
import click
from rich.console import Console
from rich.table import Table
from typing import List, Dict

# Collection of Albert Camus' notable works
CAMUS_BOOKS = [
    {"title": "The Stranger", "year": 1942, "genre": "Philosophical fiction"},
    {"title": "The Plague", "year": 1947, "genre": "Philosophical novel"},
    {"title": "The Fall", "year": 1956, "genre": "Philosophical fiction"},
    {"title": "The Myth of Sisyphus", "year": 1942, "genre": "Philosophical essay"},
    {"title": "The Rebel", "year": 1951, "genre": "Philosophical essay"},
    {"title": "A Happy Death", "year": 1971, "genre": "Philosophical fiction"},
    {"title": "The First Man", "year": 1994, "genre": "Autobiographical novel"},
]

# Default recommendation (The Stranger is often considered Camus' most famous work)
DEFAULT_RECOMMENDATION = "The Stranger"

console = Console()

def recommend_book(books_read: List[str] = None) -> str:
    """
    Recommends a book by Albert Camus based on what the user has already read.
    
    Args:
        books_read: List of book titles the user has already read
        
    Returns:
        str: Recommended book title
    """
    if not books_read:
        return DEFAULT_RECOMMENDATION
    
    # Convert to lowercase for case-insensitive comparison
    books_read_lower = [book.lower() for book in books_read]
    
    # Find unread books
    unread_books = [
        book for book in CAMUS_BOOKS 
        if book["title"].lower() not in books_read_lower
    ]
    
    if not unread_books:
        return "You've read all of Camus' major works! Consider re-reading your favorites."
    
    # Recommend the most famous unread book (prioritizing The Stranger, then The Plague, etc.)
    famous_order = ["The Stranger", "The Plague", "The Fall", "The Myth of Sisyphus"]
    
    for title in famous_order:
        if title.lower() not in books_read_lower:
            return title
    
    # If none of the most famous are unread, return the first unread book
    return unread_books[0]["title"]

def display_books(books: List[Dict[str, str]], title: str = "Albert Camus' Notable Works"):
    """Display books in a formatted table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Title", style="cyan")
    table.add_column("Year", justify="right")
    table.add_column("Genre")
    
    for book in books:
        table.add_row(book["title"], str(book["year"]), book["genre"])
    
    console.print(table)

@click.group()
def cli():
    """A simple CLI for recommending books by Albert Camus."""
    pass

@cli.command()
@click.option('--read', '-r', multiple=True, help="Books you've already read by Camus")
def recommend(read):
    """Get a book recommendation based on what you've already read."""
    books_read = list(read)
    recommendation = recommend_book(books_read)
    
    console.print("\n[bold green]Based on what you've read, I recommend:[/bold green]")
    console.print(f"[bold yellow]{recommendation}[/bold yellow]\n")
    
    # Show all books for reference
    display_books(CAMUS_BOOKS, "All of Albert Camus' Notable Works")

@cli.command()
@click.option('--title', '-t', help="Search for a specific book by title")
@click.option('--year', '-y', type=int, help="Filter books by publication year")
@click.option('--genre', '-g', help="Filter books by genre")
def list_books(title, year, genre):
    """List all books by Camus with optional filters."""
    filtered_books = CAMUS_BOOKS
    
    if title:
        filtered_books = [b for b in filtered_books if title.lower() in b["title"].lower()]
    if year:
        filtered_books = [b for b in filtered_books if b["year"] == year]
    if genre:
        filtered_books = [b for b in filtered_books if genre.lower() in b["genre"].lower()]
    
    if not filtered_books:
        console.print("[red]No books match your criteria.[/red]")
        return
    
    display_books(filtered_books, "Matching Books by Albert Camus")

if __name__ == "__main__":
    cli()
