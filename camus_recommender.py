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
@click.option('--read', '-r', multiple=True, help="Books you've already read by Camus")
def recommend(read):
    """Get a book recommendation based on what you've already read."""
    books_read = list(read)
    recommendation = recommend_book(books_read)
    console.print("\n[bold green]Based on what you've read, I recommend:[/bold green]")
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
