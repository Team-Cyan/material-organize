# Shared Context

## Repository Purpose

`material-organize` is a local macOS-focused media organization project. The current shipped slice is a Sony camera importer implemented as the Python package `material_importer`.

## Current Runtime Model

- The repository root is expected at `~/projects/material-organize`.
- The double-click entry point is `/Users/lancer/materials/Import Here.command`.
- The CLI entry point is `uv run media-import`.
- Destination library root defaults to `/Users/lancer/materials`.
- Source priority is:
  1. an explicit dropped source directory
  2. mounted SD cards under `/Volumes`

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
uv run media-import --materials-root /tmp/materials-check
```

## Guardrails

- Do not import into the real `/Users/lancer/materials` during verification unless explicitly requested.
- Prefer `/tmp/...` destinations for test and smoke-check runs.
- Keep `scripts/import-here.command` aligned with the repository root expectation and launcher location semantics.
