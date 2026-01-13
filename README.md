# nmrxiv-downloader

[![PyPI version](https://badge.fury.io/py/nmrxiv-downloader.svg)](https://badge.fury.io/py/nmrxiv-downloader)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool for searching and downloading NMR spectroscopy datasets from [nmrxiv.org](https://nmrxiv.org). Designed for integration with Claude Code and other AI assistants, with JSON output by default for easy programmatic use. Includes a `/nmrxiv` skill for Claude Code. You can then ask things like: 
`I need 20 nmr datasets from nmrxiv from molecules with less than 20 heavy atoms. The nmr data itself should be Bruker data. Every dataset should at least have 1D proton and carbon spectra, DEPT or APT, HSQC and HMBC. More is ok. Place all of them here in this
  folder. One subfolder for each nmr dataset of one and only one molecule.`

## Installation

### From PyPI (recommended)

```bash
pip install nmrxiv-downloader
```

### From GitHub

```bash
pip install git+https://github.com/steinbeck/nmrxiv-downloader.git
```

### From source (for development)

```bash
git clone https://github.com/steinbeck/nmrxiv-downloader.git
cd nmrxiv-downloader
pip install -e .
```

## Quick Start

```bash
# List available projects
nmrxiv list --type project

# Search for molecules by name
nmrxiv search --query kaempferol

# Show details for a specific project
nmrxiv show P5

# Download a project archive
nmrxiv download P5 --output ./data --extract
```

## Commands

### `nmrxiv list`

List projects or datasets from nmrXiv.

```bash
# List projects (default)
nmrxiv list --type project

# List datasets
nmrxiv list --type dataset

# Paginate through results
nmrxiv list --type project --page 2

# Human-readable table output
nmrxiv list --type project --no-json
```

**Options:**
- `--type`, `-t`: Type to list (`project` or `dataset`). Default: `project`
- `--page`, `-p`: Page number for pagination. Default: `1`
- `--json/--no-json`: Output format. Default: `--json`

**Example JSON output:**
```json
{
  "items": [
    {
      "name": "NMR data for Sinapigladioside...",
      "identifier": "NMRXIV:P5",
      "doi": "10.57992/nmrxiv.p5",
      "description": "..."
    }
  ],
  "count": 100,
  "total": 234,
  "page": 1,
  "last_page": 3,
  "type": "project"
}
```

### `nmrxiv search`

Search for molecules or filter datasets by experiment type.

#### Search molecules by name

```bash
# Search by compound name or synonym
nmrxiv search --query kaempferol

# Search by SMILES substructure
nmrxiv search --smiles "c1ccccc1"

# Human-readable output
nmrxiv search --query caffeine --no-json
```

#### Filter datasets by experiment type

```bash
# Find HSQC experiments
nmrxiv search --type hsqc

# Find 1D 13C experiments
nmrxiv search --type "1d-13c"

# Find COSY experiments
nmrxiv search --type cosy

# Find DEPT experiments
nmrxiv search --type dept

# Find HMBC experiments
nmrxiv search --type hmbc
```

**Options:**
- `--query`, `-q`: Search molecules by name or synonym
- `--smiles`, `-s`: Search molecules by SMILES substructure
- `--type`, `-t`: Filter datasets by experiment type (e.g., `hsqc`, `1d-13c`, `cosy`, `dept`, `hmbc`, `noesy`, `tocsy`)
- `--page`, `-p`: Page number. Default: `1`
- `--json/--no-json`: Output format. Default: `--json`

**Example molecule search output:**
```json
{
  "results": [
    {
      "id": 12345,
      "iupac_name": "Kaempferol",
      "molecular_formula": "C15H10O6",
      "molecular_weight": 286.24,
      "canonical_smiles": "OC1=CC=C(C=C1)C1=C(O)C(=O)C2=C(O)C=C(O)C=C2O1",
      "inchi": "InChI=1S/C15H10O6/c16-8-3-1-7..."
    }
  ],
  "count": 5,
  "search_type": "molecule",
  "query": {"query": "kaempferol"},
  "page": 1,
  "total": 5
}
```

**Example dataset filter output:**
```json
{
  "results": [
    {
      "name": "1H-13C HSQC spectrum",
      "identifier": "NMRXIV:D410",
      "type": "1H-13C HSQC",
      "doi": "10.57992/nmrxiv.d410"
    }
  ],
  "count": 15,
  "search_type": "dataset",
  "query": {"experiment_type": "hsqc"},
  "page": 1,
  "total": 5000,
  "note": "Total reflects all datasets, not filtered count"
}
```

### `nmrxiv show`

Display detailed metadata for a specific item (project or dataset).

```bash
# Show project details
nmrxiv show P5

# Show dataset details
nmrxiv show D410

# Human-readable panel output
nmrxiv show P5 --no-json
```

**Options:**
- `item_id`: Item identifier (e.g., `P5`, `D410`, `S123`)
- `--json/--no-json`: Output format. Default: `--json`

**Example output:**
```json
{
  "item": {
    "name": "NMR data for Sinapigladioside...",
    "identifier": "NMRXIV:P5",
    "doi": "10.57992/nmrxiv.p5",
    "description": "NMR data for the structure elucidation...",
    "license": "CC-BY-4.0",
    "download_url": "https://s3.uni-jena.de/nmrxiv/...",
    "created_at": "2023-01-15T10:30:00Z",
    "updated_at": "2023-06-20T14:45:00Z"
  },
  "id": "P5"
}
```

### `nmrxiv download`

Download project archives to local disk.

```bash
# Download to current directory
nmrxiv download P5

# Download to specific directory
nmrxiv download P5 --output ./nmr-data

# Download and extract ZIP
nmrxiv download P5 --output ./nmr-data --extract

# Show progress bar during download
nmrxiv download P5 --output ./nmr-data --no-json

# Download with extraction and progress bar
nmrxiv download P5 --output ./nmr-data --extract --no-json
```

**Options:**
- `item_id`: Item identifier to download (e.g., `P5`)
- `--output`, `-o`: Output directory. Default: current directory
- `--extract`, `-x`: Extract ZIP archive after download
- `--json/--no-json`: Output format. Default: `--json`

**Example output:**
```json
{
  "status": "success",
  "id": "P5",
  "file": "/path/to/nmr-data-for-project.zip",
  "size": 175628897
}
```

**Example output with extraction:**
```json
{
  "status": "success",
  "id": "P5",
  "file": "/path/to/nmr-data-for-project.zip",
  "size": 175628897,
  "extracted_to": "/path/to/P5",
  "files": ["64667648-8220-4940-aa08-b9548efb1218"],
  "total_files": 645
}
```

**Note:** Only projects have download URLs. If you try to download a dataset, the tool will suggest the parent project:
```json
{"error": true, "message": "No download URL for D410. Try downloading parent project: P11", "code": 1}
```

## Output Formats

### JSON (default)

JSON output is the default, designed for programmatic use with Claude Code and other tools:

```bash
nmrxiv list --type project | jq '.items[0].name'
```

### Human-readable

Use `--no-json` for formatted terminal output with Rich tables and panels:

```bash
nmrxiv list --type project --no-json
```

```
                          nmrXiv Projects
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Name                              ┃ ID          ┃ DOI               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ NMR data for Sinapigladioside...  │ NMRXIV:P5   │ 10.57992/nmrxiv.p5│
│ Sherlock Validation Datasets      │ NMRXIV:P11  │ 10.57992/nmrxiv...│
└───────────────────────────────────┴─────────────┴───────────────────┘
Showing 100 of 234 projects (page 1 of 3)
```

## Use Cases

### Structure Elucidation Workflow

Find and download NMR data for structure elucidation:

```bash
# 1. Search for HSQC datasets
nmrxiv search --type hsqc

# 2. Get details about a specific dataset
nmrxiv show D410

# 3. Download the parent project
nmrxiv download P11 --output ./elucidation --extract
```

### Compound Lookup

Find NMR data for a known compound:

```bash
# Search by compound name
nmrxiv search --query "caffeine"

# Or search by SMILES
nmrxiv search --smiles "Cn1cnc2c1c(=O)n(c(=O)n2C)C"
```

### Batch Processing with Claude Code

The JSON output makes it easy for AI assistants to process results:

```bash
# Get all HSQC datasets and extract identifiers
nmrxiv search --type hsqc | jq -r '.results[].identifier'

# Download multiple projects
for id in P5 P11 P15; do
  nmrxiv download $id --output ./batch --extract
done
```

## Data Structure

nmrXiv organizes data hierarchically:

- **Project**: Top-level container with download URL (ZIP archive)
  - **Study**: Grouping within a project
    - **Dataset**: Individual NMR experiment (HSQC, COSY, etc.)
      - **Files**: Bruker folders, JCAMP-DX files, etc.

Downloads are available at the project level. The ZIP archive contains all studies and datasets within the project.

## API Information

This tool uses the [nmrXiv REST API](https://nmrxiv.org/api/v1) which is publicly accessible without authentication for read operations.

**Endpoints used:**
- `GET /list/projects` - List projects
- `GET /list/datasets` - List datasets
- `GET /{id}` - Get item by identifier
- `POST /search` - Search molecules by name
- `POST /search/{smiles}` - Search by SMILES substructure

## Claude Code Integration

This tool is designed for use with [Claude Code](https://claude.ai/code) and other AI assistants.

### Automatic Context (CLAUDE.md)

When working in a directory containing this project, Claude Code automatically reads `CLAUDE.md` which provides:
- Command reference with JSON output paths
- Common workflows
- Key facts about the data model

### Install Skill (Global Access)

For global access to nmrxiv instructions from any directory:

```bash
# Clone the repo (if not already done)
git clone https://github.com/steinbeck/nmrxiv-downloader.git
cd nmrxiv-downloader

# Install the skill
./scripts/install-skill.sh
```

This installs the `/nmrxiv` skill to `~/.claude/skills/nmrxiv/`. Claude Code will automatically use this skill when you ask about NMR data or nmrxiv.

### JSON Output for AI

All commands output JSON by default, making it easy for AI assistants to parse results:

```bash
# Get download URL programmatically
nmrxiv show P5 | jq -r '.item.download_url'

# List all HSQC dataset identifiers
nmrxiv search --type hsqc | jq -r '.results[].identifier'
```

## Requirements

- Python 3.10+
- httpx
- typer
- pydantic
- rich

## License

MIT
