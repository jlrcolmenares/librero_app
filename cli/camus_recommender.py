#!/usr/bin/env python3
import click
from rich.console import Console
from rich.table import Table
from librero.recommender import recommend_book, filter_books, CAMUS_BOOKS

console = Console()

@click.group()
def cli():
    """A simple CLI for recommending books by Albert Camus."""
    pass

@cli.command()
@click.option('--current', '-c', required=True, help="Your current book by Camus (required)")
@click.option('--read', '-r', multiple=True, help="Books you've already read by Camus")
def recommend(current, read):
    """Get a book recommendation based on your current book and what you've already read."""
    if not current:
        console.print("[red]Please load your current book before we can suggest the next one.[/red]")
        console.print("[yellow]Use: --current 'Book Title' to specify your current book[/yellow]\n")
        return
    
    # Validate that the current book is a valid Camus book
    valid_titles = [book["title"].lower() for book in CAMUS_BOOKS]
    if current.lower() not in valid_titles:
        console.print(f"[red]'{current}' is not a recognized Camus book.[/red]")
        console.print("[yellow]Available books:[/yellow]")
        display_books(CAMUS_BOOKS, "Albert Camus' Notable Works")
        return
    
    books_read = list(read)
    # Add current book to the list of read books
    if current not in books_read:
        books_read.append(current)
    
    recommendation = recommend_book(books_read)
    console.print(f"\n[bold green]Since you're currently reading '{current}', I recommend:[/bold green]")
    console.print(f"[bold yellow]{recommendation}[/bold yellow]\n")
    display_books(CAMUS_BOOKS, "All of Albert Camus' Notable Works")

@cli.command()
@click.option('--title', '-t', help="Search for a specific book by title")
@click.option('--year', '-y', type=int, help="Filter books by publication year")
@click.option('--genre', '-g', help="Filter books by genre")
def list_books(title, year, genre):
    """List all books by Camus with optional filters."""
    filtered_books = filter_books(title, year, genre)
    if not filtered_books:
        console.print("[red]No books match your criteria.[/red]")
        return
    display_books(filtered_books, "Matching Books by Albert Camus")

def display_books(books, title="Albert Camus' Notable Works"):
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Title", style="cyan")
    table.add_column("Year", justify="right")
    table.add_column("Genre")
    for book in books:
        table.add_row(book["title"], str(book["year"]), book["genre"])
    console.print(table)

if __name__ == "__main__":
    cli()
