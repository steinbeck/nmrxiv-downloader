# Roadmap: nmrxiv-downloader

## Overview

Build a Python CLI tool that enables Claude Code to discover and download NMR spectroscopy datasets from nmrxiv.org. Starting with API discovery and project foundation, we'll implement search capabilities across multiple criteria, add rich metadata browsing, and finish with organized dataset downloads.

## Domain Expertise

None

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Foundation** - Project setup, CLI skeleton, nmrxiv API discovery
- [ ] **Phase 2: Search** - Search commands for experiment type, format, molecular properties, identifiers
- [ ] **Phase 3: Browse** - Results display with rich metadata and JSON output
- [ ] **Phase 4: Download** - Dataset download with organized directory structure

## Phase Details

### Phase 1: Foundation
**Goal**: Establish project structure, CLI framework, and understand nmrxiv API
**Depends on**: Nothing (first phase)
**Research**: Likely (nmrxiv API structure unknown)
**Research topics**: nmrxiv.org API endpoints, authentication requirements, rate limits, data model
**Plans**: TBD

Plans:
- [ ] 01-01: Project setup and CLI skeleton
- [ ] 01-02: nmrxiv API client with basic connectivity

### Phase 2: Search
**Goal**: Implement all search capabilities (experiment type, format, molecular properties, identifiers)
**Depends on**: Phase 1
**Research**: Unlikely (uses API patterns from Phase 1)
**Plans**: TBD

Plans:
- [ ] 02-01: Search by experiment type and format
- [ ] 02-02: Search by molecular properties and identifiers

### Phase 3: Browse
**Goal**: Display search results with rich metadata in human and machine-readable formats
**Depends on**: Phase 2
**Research**: Unlikely (internal output formatting)
**Plans**: TBD

Plans:
- [ ] 03-01: Rich metadata display and JSON output

### Phase 4: Download
**Goal**: Download datasets to local disk with organized directory structure
**Depends on**: Phase 3
**Research**: Unlikely (standard HTTP downloads)
**Plans**: TBD

Plans:
- [ ] 04-01: Dataset download with progress and organization

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 0/2 | Not started | - |
| 2. Search | 0/2 | Not started | - |
| 3. Browse | 0/1 | Not started | - |
| 4. Download | 0/1 | Not started | - |
