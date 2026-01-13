"""Output formatting for nmrxiv-downloader."""

import json
import sys
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def output_json(data: Any, pretty: bool = True) -> None:
    """Output data as JSON to stdout."""
    indent = 2 if pretty else None
    print(json.dumps(data, indent=indent, default=str))


def output_error(message: str, code: int = 1) -> None:
    """Output error as JSON to stderr and exit."""
    error = {"error": True, "message": message, "code": code}
    print(json.dumps(error), file=sys.stderr)
    raise typer.Exit(code=code)


def truncate(value: Any, max_len: int = 50) -> str:
    """Truncate string to max length."""
    s = str(value) if value is not None else ""
    return s[:max_len] + "..." if len(s) > max_len else s


def output_table(
    data: list[dict],
    columns: list[tuple[str, str]],
    title: str | None = None,
    footer: str | None = None,
) -> None:
    """Output data as a rich table.

    Args:
        data: List of dictionaries to display
        columns: List of (key, header) tuples
        title: Optional table title
        footer: Optional footer text
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")

    for key, header in columns:
        table.add_column(header)

    for row in data:
        values = []
        for key, _ in columns:
            value = row.get(key)
            if isinstance(value, dict):
                # Handle nested dicts (e.g., project: {name: ...})
                value = value.get("name") or value.get("title") or str(value)
            values.append(truncate(value))
        table.add_row(*values)

    console.print(table)
    if footer:
        console.print(f"[dim]{footer}[/dim]")


def output_item(data: dict, title: str | None = None) -> None:
    """Output a single item with rich formatting.

    Args:
        data: Dictionary of item data
        title: Optional panel title
    """
    lines = []

    # Group fields for better display
    main_fields = ["name", "description", "type", "identifier", "doi"]
    link_fields = ["public_url", "download_url", "external_url"]
    date_fields = ["created_at", "updated_at", "release_date"]
    skip_fields = ["slug", "id", "schema_version", "is_public", "is_published"]

    # Main fields
    for field in main_fields:
        if field in data and data[field]:
            label = field.replace("_", " ").title()
            value = data[field]
            if field == "description":
                value = truncate(value, 100)
            lines.append(f"[bold]{label}:[/bold] {value}")

    # Tags
    if "tags" in data and data["tags"]:
        tags = data["tags"]
        if isinstance(tags, list):
            tag_names = []
            for t in tags:
                if isinstance(t, dict):
                    name = t.get("name", {})
                    if isinstance(name, dict):
                        tag_names.append(name.get("en", str(t)))
                    else:
                        tag_names.append(str(name))
                else:
                    tag_names.append(str(t))
            lines.append(f"[bold]Tags:[/bold] {', '.join(tag_names)}")

    # License
    if "license" in data and data["license"]:
        license_info = data["license"]
        if isinstance(license_info, dict):
            lines.append(f"[bold]License:[/bold] {license_info.get('title', 'Unknown')}")

    # Project/Study (for datasets)
    if "project" in data and data["project"]:
        project = data["project"]
        if isinstance(project, dict):
            lines.append(f"[bold]Project:[/bold] {project.get('name', 'Unknown')}")

    if "study" in data and data["study"]:
        study = data["study"]
        if isinstance(study, dict):
            lines.append(f"[bold]Study:[/bold] {study.get('name', 'Unknown')}")

    # Owner
    if "owner" in data and data["owner"]:
        owner = data["owner"]
        if isinstance(owner, dict):
            name = f"{owner.get('first_name', '')} {owner.get('last_name', '')}".strip()
            lines.append(f"[bold]Owner:[/bold] {name or owner.get('username', 'Unknown')}")

    # Links
    lines.append("")
    for field in link_fields:
        if field in data and data[field]:
            label = field.replace("_", " ").title()
            lines.append(f"[bold]{label}:[/bold] [link]{data[field]}[/link]")

    # Dates
    lines.append("")
    for field in date_fields:
        if field in data and data[field]:
            label = field.replace("_", " ").title()
            lines.append(f"[bold]{label}:[/bold] {data[field]}")

    # Stats
    if "stats" in data and data["stats"]:
        stats = data["stats"]
        if isinstance(stats, dict) and stats.get("likes"):
            lines.append(f"[bold]Likes:[/bold] {stats['likes']}")

    # NMRium
    if "has_nmrium" in data:
        lines.append(f"[bold]NMRium Available:[/bold] {'Yes' if data['has_nmrium'] else 'No'}")

    content = "\n".join(line for line in lines if line or lines.index(line) > 0)
    panel = Panel(content, title=title or data.get("name", "Item"), border_style="cyan")
    console.print(panel)
