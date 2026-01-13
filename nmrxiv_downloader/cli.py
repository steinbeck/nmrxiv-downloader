"""CLI interface for nmrxiv-downloader."""

from pathlib import Path
from typing import Optional

import typer
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from .client import NmrXivClient, NmrXivError
from .output import output_error, output_item, output_json, output_table

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

            if json_output:
                result = {
                    "items": [item.model_dump() for item in response.items],
                    "count": len(response.items),
                    "total": response.total,
                    "page": response.page,
                    "last_page": response.last_page,
                    "type": type,
                }
                output_json(result)
            else:
                # Human-readable table output
                if type == "project":
                    columns = [
                        ("name", "Name"),
                        ("identifier", "ID"),
                        ("doi", "DOI"),
                    ]
                else:
                    columns = [
                        ("name", "Name"),
                        ("type", "Type"),
                        ("identifier", "ID"),
                        ("doi", "DOI"),
                    ]
                data = [item.model_dump() for item in response.items]
                footer = f"Showing {len(response.items)} of {response.total} {type}s (page {response.page} of {response.last_page})"
                output_table(data, columns, title=f"nmrXiv {type.title()}s", footer=footer)
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
                if json_output:
                    result = {
                        "results": [item.model_dump() for item in response.items],
                        "count": len(response.items),
                        "search_type": "dataset",
                        "query": {"experiment_type": experiment_type},
                        "page": response.page,
                        "total": response.total,
                        "note": "Total reflects all datasets, not filtered count",
                    }
                    output_json(result)
                else:
                    columns = [
                        ("name", "Name"),
                        ("type", "Type"),
                        ("identifier", "ID"),
                        ("project", "Project"),
                    ]
                    data = [item.model_dump() for item in response.items]
                    footer = f"Found {len(response.items)} {experiment_type} datasets on page {response.page}"
                    output_table(data, columns, title=f"Datasets: {experiment_type}", footer=footer)
            else:
                # Molecular search
                response = client.search_molecules(query=query, smiles=smiles, page=page)
                if json_output:
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
                else:
                    columns = [
                        ("iupac_name", "Name"),
                        ("molecular_formula", "Formula"),
                        ("molecular_weight", "MW"),
                        ("canonical_smiles", "SMILES"),
                    ]
                    data = [item.model_dump() for item in response.items]
                    search_desc = query or smiles
                    footer = f"Found {len(response.items)} of {response.total} molecules (page {response.page})"
                    output_table(data, columns, title=f"Molecules: {search_desc}", footer=footer)
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
            if json_output:
                result = {"item": item, "id": item_id}
                output_json(result)
            else:
                output_item(item, title=item_id)
    except NmrXivError as e:
        output_error(e.message, code=e.status_code or 1)


@app.command()
def download(
    item_id: str = typer.Argument(..., help="Item identifier to download (e.g., P5)"),
    output_dir: str = typer.Option(".", "--output", "-o", help="Output directory"),
    extract: bool = typer.Option(False, "--extract", "-x", help="Extract ZIP after download"),
    json_output: bool = typer.Option(True, "--json/--no-json", help="Output as JSON"),
) -> None:
    """Download dataset files to local directory.

    Examples:
        nmrxiv download P5                        # Download project P5 to current dir
        nmrxiv download P5 --output /data         # Download to /data directory
        nmrxiv download P5 --extract              # Download and extract ZIP
        nmrxiv download P5 --extract --no-json    # Download with progress bar
    """
    import zipfile

    try:
        with NmrXivClient() as client:
            # Get download URL for the item
            download_url = client.get_download_url(item_id)

            if not download_url:
                # Check if it's a dataset and suggest parent project
                item = client.get_item(item_id)
                project_info = item.get("project", {})
                if project_info and isinstance(project_info, dict):
                    # Try to get identifier from different sources
                    project_id = project_info.get("identifier")
                    if not project_id and project_info.get("public_url"):
                        # Extract from URL like https://nmrxiv.org/project/P11
                        project_id = project_info["public_url"].split("/")[-1]
                    if project_id:
                        output_error(
                            f"No download URL for {item_id}. Try downloading parent project: {project_id}"
                        )
                    else:
                        output_error(f"No download URL available for {item_id}")
                else:
                    output_error(f"No download URL available for {item_id}")
                return

            # Prepare output path
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)

            # Extract filename from URL
            filename = download_url.split("/")[-1]
            dest_file = out_path / filename

            # Download with progress
            if json_output:
                # Silent download for JSON output
                client.download_file(download_url, dest_file)
            else:
                # Rich progress bar for human-readable output
                with Progress(
                    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                    BarColumn(bar_width=40),
                    "[progress.percentage]{task.percentage:>3.1f}%",
                    "•",
                    DownloadColumn(),
                    "•",
                    TransferSpeedColumn(),
                    "•",
                    TimeRemainingColumn(),
                ) as progress:
                    task_id = progress.add_task(
                        "download", filename=filename, total=None
                    )

                    def update_progress(downloaded: int, total: int) -> None:
                        if total > 0:
                            progress.update(task_id, total=total, completed=downloaded)

                    client.download_file(download_url, dest_file, progress_callback=update_progress)

            # Get file size
            file_size = dest_file.stat().st_size

            result = {
                "status": "success",
                "id": item_id,
                "file": str(dest_file.absolute()),
                "size": file_size,
            }

            # Extract if requested
            if extract:
                extract_dir = out_path / item_id
                extract_dir.mkdir(parents=True, exist_ok=True)

                with zipfile.ZipFile(dest_file, "r") as zf:
                    zf.extractall(extract_dir)
                    total_files = len(zf.namelist())

                # List top-level contents of extracted directory
                top_level = [p.name for p in extract_dir.iterdir()]
                result["extracted_to"] = str(extract_dir.absolute())
                result["files"] = top_level[:20]  # Limit to first 20 items
                result["total_files"] = total_files

                if not json_output:
                    from rich.console import Console
                    console = Console()
                    console.print(f"\n[green]✓[/green] Extracted to: {extract_dir}")
                    console.print(f"  Files: {total_files} items")

            if json_output:
                output_json(result)
            else:
                from rich.console import Console
                console = Console()
                console.print(f"\n[green]✓[/green] Downloaded: {dest_file}")
                console.print(f"  Size: {file_size:,} bytes")

    except NmrXivError as e:
        output_error(e.message, code=e.status_code or 1)


if __name__ == "__main__":
    app()
