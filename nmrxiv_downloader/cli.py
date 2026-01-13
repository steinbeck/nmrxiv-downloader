"""CLI interface for nmrxiv-downloader."""

from typing import Optional

import typer

from .client import NmrXivClient, NmrXivError
from .output import output_error, output_json

app = typer.Typer(
    help="nmrXiv dataset search and download tool for Claude Code",
    no_args_is_help=True,
)


@app.command()
def list(
    type: str = typer.Option(
        "project",
        "--type",
        "-t",
        help="Type to list: project, dataset",
    ),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """List items from nmrXiv (projects or datasets)."""
    try:
        with NmrXivClient() as client:
            if type == "project":
                items = client.list_projects()
            elif type == "dataset":
                items = client.list_datasets()
            else:
                output_error(f"Unknown type: {type}. Use 'project' or 'dataset'.")

            result = {
                "items": [item.model_dump() for item in items],
                "count": len(items),
                "type": type,
            }
            output_json(result)
    except NmrXivError as e:
        output_error(e.message, code=e.status_code or 1)


@app.command()
def search(
    query: Optional[str] = typer.Argument(None, help="Search query"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """Search nmrXiv datasets by criteria."""
    result = {"status": "not implemented", "command": "search"}
    output_json(result)


@app.command()
def show(
    item_id: str = typer.Argument(..., help="Item identifier (e.g., P5, D123)"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """Show detailed metadata for an item."""
    try:
        with NmrXivClient() as client:
            item = client.get_item(item_id)
            result = {"item": item, "id": item_id}
            output_json(result)
    except NmrXivError as e:
        output_error(e.message, code=e.status_code or 1)


@app.command()
def download(
    item_id: Optional[str] = typer.Argument(None, help="Item identifier to download"),
    output_dir: str = typer.Option(".", "--output", "-o", help="Output directory"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """Download dataset files to local directory."""
    result = {"status": "not implemented", "command": "download"}
    output_json(result)


if __name__ == "__main__":
    app()
