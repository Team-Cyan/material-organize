# Shared Context

## Repository Purpose

`material-manager` is a local macOS-focused media management project. The current shipped slice is a Sony camera importer implemented as the Python package `material_importer`.

## Current Runtime Model

- The repository root is expected at `~/projects/material-manager`.
- The double-click entry point is `/Users/lancer/import/media-import.command`.
- The CLI entry point is `poetry run media-import`.
- Destination library root defaults to `/Users/lancer/materials`.
- Source priority is:
  1. mounted SD cards under `/Volumes`
  2. fallback directory `/Users/lancer/import`

## Current Functional Scope

- Import `.arw` and `.raw` photos.
- Import `.mp4`, `.mov`, and `.mxf` videos.
- Use EXIF and media metadata to resolve capture time.
- Fall back to Sony clip XML for video timestamps.
- Group media by trip day with a `04:00` cutoff.
- Deduplicate imports via SHA-256 manifest tracking.

## Core Commands

```bash
make setup
make test
make run
poetry run media-import --materials-root /tmp/materials-check
```

## Guardrails

- Do not import into the real `/Users/lancer/materials` during verification unless explicitly requested.
- Prefer `/tmp/...` destinations for test and smoke-check runs.
- Keep `scripts/media-import.command` aligned with the repository root expectation.
