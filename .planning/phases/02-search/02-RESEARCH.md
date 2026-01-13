# Phase 2: Search - Research

**Researched:** 2026-01-13
**Domain:** nmrxiv search API capabilities
**Confidence:** HIGH (verified through API testing)

## API Findings

### Molecular Search: `/v1/search`

The search endpoint searches **molecules**, not datasets directly.

**Endpoint:** `POST /v1/search/{smiles?}`

**Parameters:**
- URL path: SMILES string (optional, for substructure search)
- Body: `{"query": "compound name"}` for name/synonym search

**Response:** Paginated list of molecules with:
- `molecular_formula`, `molecular_weight`
- `canonical_smiles`, `inchi`, `inchi_key`
- `synonyms` (extensive list of names)
- Pagination: `current_page`, `total`, `data[]`

**Examples:**
```bash
# Search by name
curl -X POST -d '{"query": "kaempferol"}' /v1/search
# Returns 2 molecules matching "kaempferol"

# Search by SMILES substructure
curl -X POST /v1/search/CCO
# Returns 1174 molecules containing ethanol substructure
```

### Dataset Listing: `/v1/list/datasets`

**Pagination:**
- 5970 total datasets
- 100 per page (60 pages)
- `?page=N` parameter

**Dataset fields include:**
- `type`: Experiment type (e.g., "hsqc - 1H-13C", "1d - 13C", "cosy - 1H-1H")
- `identifier`: "NMRXIV:D410"
- `project`, `study`: Parent references
- `doi`, `public_url`

**No server-side filtering** - must filter client-side.

### Experiment Types Found

From 100 datasets sampled:
- 1d - 13C, 1d - 1H
- 2d - 1H-13C, 2d - 1H-1H
- cosy - 1H-1H
- dept - 13C
- hmbc - 1H-13C, hmbc - 13C-1H
- hsqc - 1H-13C
- hmqc - 1H-13C
- noesy - 1H-1H
- tocsy - 1H-1H

### Data Format

Datasets don't expose format (Bruker, Jeol, JCAMP) in list endpoint.
Format may be available in individual dataset details or file listing.

## Search Strategy

1. **Compound search** → Use `/v1/search` with SMILES or query
2. **Experiment type filter** → Fetch datasets, filter client-side by `type`
3. **Combined** → Search molecules, then find related datasets

## Limitations

- No direct "find datasets for molecule X" endpoint
- No server-side filtering for datasets
- Format info not in dataset list
- Pagination required for full results
