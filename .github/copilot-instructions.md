# Material Organize - AI Workflow

Read `.ai/README.md` first.

## Current Architecture

- Repository root: `~/projects/material-organize`
- Python package: `src/material_importer`
- CLI command: `poetry run media-import`
- Double-click launcher: `/Users/lancer/materials/Import Here.command`

## Required Read Order

1. `.ai/shared-context.md`
2. `.ai/architecture/module-boundaries.md`
3. one relevant file in `.ai/playbooks/`
4. `.ai/checklists/import-change-checklist.md` before finalizing

## Working Rules

- Keep AI-facing documentation in English.
- Verify behavior in `/tmp/...` unless the user explicitly asks to write into the real materials library.
- Keep README, launcher, and `.ai` docs aligned whenever changing setup or workflow.
