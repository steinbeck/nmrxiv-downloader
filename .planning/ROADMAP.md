# Roadmap: nmrxiv-downloader

## Overview

Build a Python CLI tool that enables Claude Code to discover and download NMR spectroscopy datasets from nmrxiv.org. Starting with API discovery and project foundation, we'll implement search capabilities across multiple criteria, add rich metadata browsing, and finish with organized dataset downloads.

## Domain Expertise

None

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Foundation** - Project setup, CLI skeleton, nmrxiv API discovery
- [x] **Phase 2: Search** - Search commands for experiment type, format, molecular properties, identifiers
- [x] **Phase 3: Browse** - Results display with rich metadata and JSON output
- [x] **Phase 4: Download** - Dataset download with organized directory structure

## Phase Details

### Phase 1: Foundation
**Goal**: Establish project structure, CLI framework, and understand nmrxiv API
**Depends on**: Nothing (first phase)
**Research**: Likely (nmrxiv API structure unknown)
**Research topics**: nmrxiv.org API endpoints, authentication requirements, rate limits, data model
**Plans**: TBD

Plans:
- [x] 01-01: Project setup and CLI skeleton
- [x] 01-02: nmrxiv API client with basic connectivity

### Phase 2: Search
**Goal**: Implement all search capabilities (experiment type, format, molecular properties, identifiers)
**Depends on**: Phase 1
**Research**: Done (API search capabilities explored)
**Plans**: Combined into single plan (API simpler than expected)

Plans:
- [x] 02-01: Search by experiment type, molecular properties, and identifiers (combined)

### Phase 3: Browse
**Goal**: Display search results with rich metadata in human and machine-readable formats
**Depends on**: Phase 2
**Research**: None needed
**Plans**: Complete

Plans:
- [x] 03-01: Rich metadata display with table and panel output

### Phase 4: Download
**Goal**: Download datasets to local disk with organized directory structure
**Depends on**: Phase 3
**Research**: Unlikely (standard HTTP downloads)
**Plans**: TBD

Plans:
- [x] 04-01: Dataset download with progress and organization

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 2/2 | Complete | 2026-01-13 |
| 2. Search | 1/1 | Complete | 2026-01-13 |
| 3. Browse | 1/1 | Complete | 2026-01-13 |
| 4. Download | 1/1 | Complete | 2026-01-13 |
