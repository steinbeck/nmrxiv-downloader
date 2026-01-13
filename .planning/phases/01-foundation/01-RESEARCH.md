# Phase 1: Foundation - Research

**Researched:** 2026-01-13
**Domain:** nmrxiv API client + Python CLI for Claude Code integration
**Confidence:** HIGH

<research_summary>
## Summary

Researched the nmrxiv.org REST API and Python ecosystem for building a CLI tool optimized for Claude Code consumption. nmrxiv provides a Laravel-based REST API with Swagger documentation, supporting search via SMILES, listing by model type, and dataset retrieval by identifier.

The standard Python approach for a modern CLI tool targeting programmatic use is Typer (for clean type-hinted CLI) + httpx (for sync/async HTTP with HTTP/2 support). The combination provides machine-readable JSON output capability, minimal boilerplate, and excellent developer experience.

**Primary recommendation:** Use Typer + httpx stack. Implement JSON output as default (machine-readable), with optional human-readable formatting. Structure commands as `nmrxiv search`, `nmrxiv show`, `nmrxiv download` for composability.
</research_summary>

<standard_stack>
## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| typer | 0.12+ | CLI framework | Type-hint driven, minimal boilerplate, auto-help, shell completion |
| httpx | 0.27+ | HTTP client | Sync + async, HTTP/2, requests-compatible API, streaming downloads |
| rich | 13+ | Terminal formatting | Beautiful output, progress bars, tables (bundled with typer) |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pydantic | 2.5+ | Data validation | Parsing API responses, config files |
| python-dotenv | 1.0+ | Environment config | API keys, custom endpoints |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Typer | Click | Click is more verbose; Typer builds on Click with type hints |
| Typer | argparse | argparse is stdlib but very verbose; Typer is much simpler |
| httpx | requests | requests lacks async and HTTP/2; httpx is modern choice |
| httpx | aiohttp | aiohttp is async-only; httpx does both sync and async |

**Installation:**
```bash
pip install typer httpx rich pydantic python-dotenv
```
</standard_stack>

<nmrxiv_api>
## nmrXiv API Details

### Base URL
```
https://nmrxiv.org/api/v1
```

### Key Endpoints

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/v1/search/{smiles?}` | POST | Search datasets, optional SMILES filter | No |
| `/v1/list/{model}` | GET | List all items by model type (project, study, dataset) | No |
| `/v1/{id}` | GET | Get item by identifier | No |
| `/v1/files/children/{file}` | GET | List files in a directory | No |
| `/v1/schemas/bioschemas/{id}` | GET | Get Bioschemas metadata | No |
| `/v1/schemas/datacite/{id}` | GET | Get DataCite metadata | No |

### Data Model Hierarchy
```
Project
  └── Study (Sample)
        └── Dataset (Spectrum)
              └── Files (raw NMR data)
```

### Metadata Standards
- **Bioschemas**: Structured data for search engines
- **DataCite**: DOI metadata standard
- **ISA-Tab**: Investigation-Study-Assay format
- **NMR CV**: Nuclear magnetic resonance controlled vocabulary

### Ontologies Used (for search filtering)
- **NMR CV**: Experiment types, file formats, instruments
- **CHMO**: Chemical methods ontology
- **UO**: Units of measurement
- **CHEMINF**: Chemical informatics terms

### Authentication
- Public endpoints: No auth required for read operations
- Protected endpoints: Laravel Sanctum (API tokens)
- Most read operations are public
</nmrxiv_api>

<architecture_patterns>
## Architecture Patterns

### Recommended Project Structure
```
nmrxiv_downloader/
├── __init__.py
├── __main__.py          # Entry point
├── cli.py               # Typer app definition
├── client.py            # nmrxiv API client
├── models.py            # Pydantic response models
├── output.py            # JSON/human formatting
└── config.py            # Settings, defaults
```

### Pattern 1: Typer App with Subcommands
**What:** Group related commands under a single CLI app
**When to use:** Multiple commands that share context
**Example:**
```python
# cli.py
import typer
from typing import Optional
import json

app = typer.Typer(help="nmrXiv dataset search and download tool")

@app.command()
def search(
    experiment_type: Optional[str] = typer.Option(None, "--type", "-t"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
    json_output: bool = typer.Option(True, "--json/--no-json"),
):
    """Search nmrXiv datasets by criteria."""
    results = client.search(experiment_type=experiment_type, format=format)
    if json_output:
        print(json.dumps(results, indent=2))
    else:
        display_table(results)

@app.command()
def show(dataset_id: str):
    """Show detailed metadata for a dataset."""
    ...

@app.command()
def download(dataset_id: str, output_dir: str = "."):
    """Download dataset files to local directory."""
    ...

if __name__ == "__main__":
    app()
```

### Pattern 2: API Client with httpx
**What:** Encapsulate all API calls in a client class
**When to use:** Any API integration
**Example:**
```python
# client.py
import httpx
from typing import Optional, List
from .models import Dataset, SearchResult

class NmrXivClient:
    BASE_URL = "https://nmrxiv.org/api/v1"

    def __init__(self, timeout: float = 30.0):
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=timeout,
            headers={"Accept": "application/json"}
        )

    def search(self, smiles: Optional[str] = None) -> List[SearchResult]:
        response = self.client.post(f"/search/{smiles or ''}")
        response.raise_for_status()
        return [SearchResult(**r) for r in response.json()]

    def get_dataset(self, dataset_id: str) -> Dataset:
        response = self.client.get(f"/{dataset_id}")
        response.raise_for_status()
        return Dataset(**response.json())

    def list_models(self, model: str) -> List[dict]:
        response = self.client.get(f"/list/{model}")
        response.raise_for_status()
        return response.json()
```

### Pattern 3: Machine-Readable Output for Claude Code
**What:** Default to JSON output for programmatic consumption
**When to use:** Tools meant for AI/script consumption
**Example:**
```python
# output.py
import json
import sys
from typing import Any
from rich.console import Console
from rich.table import Table

def output_json(data: Any, pretty: bool = True):
    """Output data as JSON to stdout."""
    indent = 2 if pretty else None
    print(json.dumps(data, indent=indent, default=str))

def output_table(data: list[dict], columns: list[str]):
    """Output data as a rich table for humans."""
    console = Console()
    table = Table()
    for col in columns:
        table.add_column(col)
    for row in data:
        table.add_row(*[str(row.get(col, "")) for col in columns])
    console.print(table)
```

### Anti-Patterns to Avoid
- **Mixing output to stdout/stderr**: JSON output to stdout, errors to stderr only
- **Interactive prompts**: Breaks programmatic use; use options instead
- **Hardcoded URLs**: Use config/env vars for base URL flexibility
- **No timeout handling**: Always set explicit timeouts on HTTP calls
</architecture_patterns>

<dont_hand_roll>
## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Argument parsing | Custom sys.argv parsing | Typer | Type hints, help generation, validation |
| HTTP requests | urllib/socket | httpx | Connection pooling, retries, streaming |
| JSON formatting | print(dict) | json.dumps() | Proper escaping, serialization |
| Progress bars | Custom print loops | rich.progress | Handles terminal width, ETA, rates |
| Config management | Custom file parsing | pydantic-settings | Validation, env vars, defaults |
| Shell completion | Custom scripts | Typer built-in | Works with bash/zsh/fish/pwsh |

**Key insight:** For a CLI tool meant for Claude Code integration, the primary interface is JSON output. Don't invent a custom format — standard JSON is universally parseable and what Claude Code expects.
</dont_hand_roll>

<common_pitfalls>
## Common Pitfalls

### Pitfall 1: Blocking on Large Downloads
**What goes wrong:** CLI hangs with no feedback during large file downloads
**Why it happens:** Synchronous download without progress indication
**How to avoid:** Use httpx streaming with rich progress bar
**Warning signs:** User/Claude cancels thinking it's stuck

### Pitfall 2: Non-Machine-Readable Output
**What goes wrong:** Claude Code can't parse the output reliably
**Why it happens:** Mixing human-readable formatting with data
**How to avoid:** JSON by default, human formatting opt-in via `--no-json`
**Warning signs:** Parsing errors in Claude Code workflows

### Pitfall 3: No Error Handling for API Failures
**What goes wrong:** Cryptic Python tracebacks on network errors
**Why it happens:** No try/except around HTTP calls
**How to avoid:** Catch httpx exceptions, output structured error JSON
**Warning signs:** Stack traces in output instead of error messages

### Pitfall 4: Hardcoded API Assumptions
**What goes wrong:** Tool breaks when nmrxiv API changes
**Why it happens:** Assuming fixed response structure
**How to avoid:** Use Pydantic models with Optional fields, graceful degradation
**Warning signs:** KeyError on new/missing fields

### Pitfall 5: No Exit Codes
**What goes wrong:** Scripts can't detect if command succeeded
**Why it happens:** Forgetting to raise SystemExit with appropriate code
**How to avoid:** Use `raise typer.Exit(code=1)` for errors
**Warning signs:** `echo $?` always returns 0
</common_pitfalls>

<code_examples>
## Code Examples

### Entry Point Setup (__main__.py)
```python
# Source: Typer best practices
from .cli import app

if __name__ == "__main__":
    app()
```

### Pydantic Models for API Responses
```python
# Source: Pydantic docs pattern
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Dataset(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    experiment_type: Optional[str] = None
    format: Optional[str] = None
    molecular_formula: Optional[str] = None
    compound_name: Optional[str] = None
    created_at: Optional[datetime] = None
    download_url: Optional[str] = None

class SearchResult(BaseModel):
    total: int
    datasets: List[Dataset]
```

### Streaming Download with Progress
```python
# Source: httpx + rich pattern
import httpx
from pathlib import Path
from rich.progress import Progress, DownloadColumn, TransferSpeedColumn

def download_file(url: str, dest: Path):
    with httpx.stream("GET", url) as response:
        total = int(response.headers.get("content-length", 0))
        with Progress(
            *Progress.get_default_columns(),
            DownloadColumn(),
            TransferSpeedColumn(),
        ) as progress:
            task = progress.add_task("Downloading", total=total)
            with open(dest, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
                    progress.update(task, advance=len(chunk))
```

### Structured Error Output
```python
# Pattern for Claude Code consumption
import json
import sys
import typer

def error_exit(message: str, code: int = 1):
    """Output error as JSON and exit with code."""
    error = {"error": True, "message": message, "code": code}
    print(json.dumps(error), file=sys.stderr)
    raise typer.Exit(code=code)
```
</code_examples>

<sota_updates>
## State of the Art (2025-2026)

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| requests | httpx | 2023+ | httpx supports async, HTTP/2; requests does not |
| argparse/click | Typer | 2022+ | Typer uses type hints, less boilerplate |
| Custom arg parsing | Typer with Annotated | 2023+ | Better IDE support, cleaner syntax |

**New tools/patterns to consider:**
- **uv**: Fast Python package installer, can replace pip for faster installs
- **Ruff**: Fast Python linter, can replace flake8/black in CI
- **pyproject.toml**: Modern Python packaging, replaces setup.py

**Deprecated/outdated:**
- **requests for async**: Use httpx instead
- **setup.py**: Use pyproject.toml for packaging
- **Click for new projects**: Typer is simpler for most cases
</sota_updates>

<open_questions>
## Open Questions

1. **Exact search query parameters for nmrxiv**
   - What we know: POST to `/v1/search/{smiles?}` exists
   - What's unclear: Full list of query parameters for filtering by experiment type, format, etc.
   - Recommendation: Test the Swagger UI at nmrxiv.org/api/documentation, implement based on actual responses

2. **File download mechanism**
   - What we know: Datasets have associated files, `/files/children/{file}` lists them
   - What's unclear: Exact URL structure for raw file downloads
   - Recommendation: Explore a few datasets to discover download URL patterns

3. **Rate limiting**
   - What we know: API is public, no explicit rate limit documented
   - What's unclear: Whether rate limits exist in practice
   - Recommendation: Implement respectful delays, handle 429 responses gracefully
</open_questions>

<sources>
## Sources

### Primary (HIGH confidence)
- [nmrxiv API documentation](https://docs.nmrxiv.org/developer-guides/api.html) - API overview
- [nmrxiv GitHub routes/api.php](https://github.com/NFDI4Chem/nmrxiv/blob/main/routes/api.php) - Actual endpoint definitions
- [Typer documentation](https://typer.tiangolo.com/) - CLI framework
- [httpx documentation](https://www.python-httpx.org/) - HTTP client

### Secondary (MEDIUM confidence)
- [nmrxiv ontologies](https://docs.nmrxiv.org/introduction/data/ontologies.html) - Metadata standards
- CLI framework comparisons verified against official docs

### Tertiary (LOW confidence - needs validation)
- Rate limit behavior - needs testing
- Full search parameter list - needs API exploration
</sources>

<metadata>
## Metadata

**Research scope:**
- Core technology: nmrxiv REST API, Python CLI
- Ecosystem: Typer, httpx, rich, pydantic
- Patterns: CLI architecture, API client, JSON output
- Pitfalls: Downloads, output format, error handling

**Confidence breakdown:**
- Standard stack: HIGH - verified with official docs
- Architecture: HIGH - standard Python patterns
- nmrxiv API: MEDIUM - routes verified, parameters need exploration
- Pitfalls: HIGH - common CLI/API integration issues

**Research date:** 2026-01-13
**Valid until:** 2026-02-13 (30 days - stable ecosystem)
</metadata>

---

*Phase: 01-foundation*
*Research completed: 2026-01-13*
*Ready for planning: yes*
