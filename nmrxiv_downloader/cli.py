"""CLI interface for nmrxiv-downloader."""

import json
import sys
from typing import Optional

import typer

app = typer.Typer(
    help="nmrXiv dataset search and download tool for Claude Code",
    no_args_is_help=True,
)


def _output_json(data: dict, file=sys.stdout) -> None:
    """Output data as JSON."""
    print(json.dumps(data, indent=2), file=file)


@app.command()
def search(
    query: Optional[str] = typer.Argument(None, help="Search query"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """Search nmrXiv datasets by criteria."""
    result = {"status": "not implemented", "command": "search"}
    _output_json(result)
    raise typer.Exit(code=0)


@app.command()
def show(
    item_id: Optional[str] = typer.Argument(None, help="Item identifier to show"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """Show detailed metadata for a dataset."""
    result = {"status": "not implemented", "command": "show"}
    _output_json(result)
    raise typer.Exit(code=0)


@app.command()
def download(
    item_id: Optional[str] = typer.Argument(None, help="Item identifier to download"),
    output_dir: str = typer.Option(".", "--output", "-o", help="Output directory"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """Download dataset files to local directory."""
    result = {"status": "not implemented", "command": "download"}
    _output_json(result)
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
