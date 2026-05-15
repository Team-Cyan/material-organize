# Project Overview

## What This Project Is

- A local macOS-focused media organization project.
- The current shipped slice is the Sony camera importer implemented as the Python package `material_importer`.
- A docs-first repo where importer behavior, launcher assumptions, and safe verification paths should stay easy to recover.

## What It Is Not

- Not a general photo-management platform.
- Not a place to verify by writing into the real `/Users/lancer/materials` library unless explicitly requested.
- Not a repo where setup, launcher, and workflow docs should drift apart.

## Core Runtime Surfaces

- repository root: `~/projects/material-organize`
- CLI entrypoint: `uv run media-import`
- launcher entrypoint: `/Users/lancer/materials/Import Here.command`
- default library root: `/Users/lancer/materials`
- safe verification target: `/tmp/material-organize-smoke`

## Current Architecture

- `sources.py` discovers source roots and enumerates candidate media files.
- `metadata.py` resolves timestamps from EXIF, media metadata, and Sony clip XML.
- `planner.py` maps capture times into trip-day destinations and filenames.
- `manifest.py` tracks hashes and duplicate imports.
- `importer.py` orchestrates the import flow.
- `reporting.py` owns terminal presentation.
- `cli.py` handles argument parsing and top-level wiring.

## Documentation Strategy

- root `AGENTS.md` for entry routing
- `.agents/` for repo-local agent assets
- `docs/ai/` for reusable knowledge
- `docs/roadmap.md` for current state
- `docs/operations/` for handoff notes
