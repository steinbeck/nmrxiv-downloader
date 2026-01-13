# nmrxiv-downloader

## What This Is

A Python CLI tool designed for Claude Code to search and download NMR spectroscopy datasets from nmrxiv.org. Enables programmatic discovery of NMR data by experiment type, format, molecular properties, and compound identifiers, with seamless download to local disk.

## Core Value

Claude Code integration — the tool must be easy to use programmatically during NMR analysis tasks, with machine-readable output and predictable, composable commands.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Search by experiment type (1D 13C, 1H, HSQC, HMBC, COSY, DEPT, etc.)
- [ ] Search by dataset format (Bruker, Jeol, JCAMP-DX, etc.)
- [ ] Search by molecular properties (formula, mass range, element composition)
- [ ] Search by compound identifiers (SMILES, InChI, compound names)
- [ ] Browse results with rich metadata (compound name, molecular formula, spectrometer info, file size)
- [ ] Download datasets to local disk with organized directory structure
- [ ] Machine-readable output (JSON) optimized for Claude Code consumption
- [ ] Search → Browse → Download workflow with composable commands

### Out of Scope

- Data processing/spectral analysis — tool only searches and downloads, no NMR interpretation
- GUI — CLI only, no web interface or desktop application
- Upload/submission to nmrxiv — read-only access to the repository

## Context

nmrxiv.org is an open repository for NMR spectroscopy data. This tool will query their API to discover datasets matching specified criteria. The primary user is Claude Code itself, using this tool as part of structure elucidation or NMR analysis workflows (e.g., with the lucy-ng skill).

Key considerations:
- Output format should be JSON for easy parsing
- Commands should be composable (search IDs can feed into download commands)
- Error messages should be clear and actionable
- Progress indication for downloads

## Constraints

- **Language**: Python — good ecosystem for scientific tools and chemistry libraries
- **Integration**: Must be optimized for programmatic use by Claude Code, not just human users
- **API**: Dependent on nmrxiv.org API availability and structure

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python implementation | Scientific ecosystem, chemistry libraries, user preference | — Pending |
| JSON output format | Machine-readable for Claude Code integration | — Pending |
| CLI-only interface | Focused scope, optimized for programmatic use | — Pending |

---
*Last updated: 2026-01-13 after initialization*
