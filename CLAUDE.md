# nmrxiv-downloader - Claude Code Instructions

CLI tool for searching and downloading NMR datasets from nmrxiv.org. All commands output JSON by default for easy parsing.

## Commands

### List projects/datasets
```bash
nmrxiv list --type project          # List all projects
nmrxiv list --type dataset          # List all datasets
nmrxiv list --type project --page 2 # Pagination
```
**JSON path:** `.items[]` (each has `.identifier`, `.name`, `.doi`)

### Search molecules
```bash
nmrxiv search --query "caffeine"    # By name/synonym
nmrxiv search --smiles "c1ccccc1"   # By SMILES substructure
```
**JSON path:** `.results[]` (each has `.id`, `.iupac_name`, `.molecular_formula`, `.canonical_smiles`)

### Filter datasets by experiment type
```bash
nmrxiv search --type hsqc           # HSQC experiments
nmrxiv search --type "1d-13c"       # 1D 13C experiments
nmrxiv search --type cosy           # COSY experiments
nmrxiv search --type hmbc           # HMBC experiments
nmrxiv search --type dept           # DEPT experiments
```
**JSON path:** `.results[]` (each has `.identifier`, `.name`, `.type`)

### Show item details
```bash
nmrxiv show P5                      # Project details
nmrxiv show D410                    # Dataset details
```
**JSON path:** `.item` (has `.download_url` for projects, `.type` for datasets)

### Download project
```bash
nmrxiv download P5 --output /tmp              # Download ZIP
nmrxiv download P5 --output /tmp --extract    # Download and extract
```
**JSON path:** `.file` (path), `.size` (bytes), `.extracted_to` (if --extract)

## Key Facts

- **Projects have download URLs, datasets don't** - Download via parent project
- **If dataset has no download_url:** Error message includes parent project ID
- **Data hierarchy:** Project → Study → Dataset → Files (Bruker, JCAMP-DX)
- **Human output:** Add `--no-json` for tables/progress bars

## Common Workflows

### Find and download HSQC data
```bash
# 1. Find HSQC datasets
nmrxiv search --type hsqc | jq '.results[0]'

# 2. Get dataset details (find parent project)
nmrxiv show D410 | jq '.item.project'

# 3. Download parent project
nmrxiv download P11 --output ./data --extract
```

### Search compound and get NMR data
```bash
# 1. Search for compound
nmrxiv search --query "quercetin" | jq '.results[0].canonical_smiles'

# 2. List projects to find relevant data
nmrxiv list --type project | jq '.items[] | select(.name | test("quercetin"; "i"))'
```

## Error Handling

Errors return JSON: `{"error": true, "message": "...", "code": N}`

Common errors:
- Invalid ID: HTTP 500 error
- Dataset without download URL: Suggests parent project ID
