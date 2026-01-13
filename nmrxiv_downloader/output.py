"""Output formatting for nmrxiv-downloader."""

import json
import sys
from typing import Any

import typer


def output_json(data: Any, pretty: bool = True) -> None:
    """Output data as JSON to stdout."""
    indent = 2 if pretty else None
    print(json.dumps(data, indent=indent, default=str))


def output_error(message: str, code: int = 1) -> None:
    """Output error as JSON to stderr and exit."""
    error = {"error": True, "message": message, "code": code}
    print(json.dumps(error), file=sys.stderr)
    raise typer.Exit(code=code)
