# Plan 04-01 Summary: Dataset Download

**Completed:** 2026-01-13
**Duration:** ~10 minutes

## What Was Done

### Task 1: Add download methods to API client
- Added `get_download_url(item_id)` method to fetch download URL from item
- Added `download_file(url, dest, progress_callback)` method with streaming
- Uses httpx streaming with 8KB chunks for large files
- 300s timeout for download operations
- Returns Path to downloaded file

### Task 2: Implement download command with progress
- Arguments: item_id (required), --output/-o, --extract/-x, --json/--no-json
- Rich progress bar with: filename, percentage, size, speed, ETA
- JSON output: status, id, file path, size
- Error handling for invalid IDs and missing download URLs
- Suggests parent project for datasets without download URL

### Task 3: Add extraction and organization
- Uses zipfile module for extraction
- Creates subdirectory with project ID (e.g., P5/)
- JSON includes: extracted_to, files (top-level), total_files count
- Human-readable output shows extraction path and file count

## Verification Results

All checks passed:
- [x] `nmrxiv download P5 --output /tmp` downloads ZIP file
- [x] `nmrxiv download P5 --output /tmp --no-json` shows progress bar
- [x] `nmrxiv download P5 --output /tmp --extract` extracts ZIP
- [x] JSON output includes status, file path, and size
- [x] Error handling for invalid IDs (HTTP 500 error)
- [x] Error handling for datasets suggests parent project (e.g., D410 → P11)

## Files Modified

- `nmrxiv_downloader/client.py` - Added get_download_url() and download_file()
- `nmrxiv_downloader/cli.py` - Implemented download command with progress bar

## Output Examples

**JSON output:**
```json
{
  "status": "success",
  "id": "P5",
  "file": "/tmp/nmr-data-for-sinapigladioside-congener-gladiofungin-a-and-necroxime-a.zip",
  "size": 175628897
}
```

**With extraction:**
```json
{
  "status": "success",
  "id": "P5",
  "file": "/tmp/...",
  "size": 175628897,
  "extracted_to": "/tmp/P5",
  "files": ["64667648-8220-4940-aa08-b9548efb1218"],
  "total_files": 645
}
```

**Human-readable output:**
```
filename.zip 100.0% • 167.5/167.5 MB • 5.2 MB/s • 0:00:00

✓ Downloaded: /tmp/filename.zip
  Size: 175,628,897 bytes
```

## Notes

- ZIP archives are downloaded from S3 (https://s3.uni-jena.de/nmrxiv/)
- Projects have download URLs, datasets must be downloaded via parent project
- Files are large (100+ MB typical), streaming prevents memory issues
- Progress callback updates Rich progress bar in real-time
