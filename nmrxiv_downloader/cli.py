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
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """List items from nmrXiv (projects or datasets)."""
    try:
        with NmrXivClient() as client:
            if type == "project":
                response = client.list_projects(page=page)
            elif type == "dataset":
                response = client.list_datasets(page=page)
            else:
                output_error(f"Unknown type: {type}. Use 'project' or 'dataset'.")
                return

            result = {
                "items": [item.model_dump() for item in response.items],
                "count": len(response.items),
                "total": response.total,
                "page": response.page,
                "last_page": response.last_page,
                "type": type,
            }
            output_json(result)
    except NmrXivError as e:
        output_error(e.message, code=e.status_code or 1)


@app.command()
def search(
    query: Optional[str] = typer.Option(
        None, "--query", "-q", help="Search molecules by name or synonym"
    ),
    smiles: Optional[str] = typer.Option(
        None, "--smiles", "-s", help="Search molecules by SMILES substructure"
    ),
    experiment_type: Optional[str] = typer.Option(
        None, "--type", "-t", help="Filter datasets by experiment type (e.g., hsqc, 1d-13c, cosy)"
    ),
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """Search nmrXiv for molecules or datasets.

    Examples:
        nmrxiv search --query kaempferol       # Search by compound name
        nmrxiv search --smiles CCO             # Search by SMILES substructure
        nmrxiv search --type hsqc              # Filter datasets by experiment type
        nmrxiv search --type "1d-13c"          # Filter datasets by 1D 13C experiments
    """
    if not any([query, smiles, experiment_type]):
        output_error(
            "Please provide at least one search criterion: --query, --smiles, or --type"
        )
        return

    try:
        with NmrXivClient() as client:
            if experiment_type:
                # Dataset filtering by experiment type
                response = client.filter_datasets(experiment_type, page=page)
                result = {
                    "results": [item.model_dump() for item in response.items],
                    "count": len(response.items),
                    "search_type": "dataset",
                    "query": {"experiment_type": experiment_type},
                    "page": response.page,
                    "total": response.total,
                    "note": "Total reflects all datasets, not filtered count",
                }
            else:
                # Molecular search
                response = client.search_molecules(query=query, smiles=smiles, page=page)
                result = {
                    "results": [item.model_dump() for item in response.items],
                    "count": len(response.items),
                    "search_type": "molecule",
                    "query": {
                        k: v for k, v in {"query": query, "smiles": smiles}.items() if v
                    },
                    "page": response.page,
                    "total": response.total,
                }
            output_json(result)
    except NmrXivError as e:
        output_error(e.message, code=e.status_code or 1)


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
