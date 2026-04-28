# Material Organize - AI Workflow

Read `docs/ai/README.md` first.

## Current Architecture

- Repository root: `~/projects/material-organize`
- Python package: `src/material_importer`
- CLI command: `uv run media-import`
- Double-click launcher: `/Users/lancer/materials/Import Here.command`

## Required Read Order

1. `docs/ai/shared-context.md`
2. `docs/ai/modules/importer-boundaries.md`
3. one relevant file in `docs/ai/playbooks/`
4. `docs/ai/checklists/import-change-checklist.md` before finalizing

## Working Rules

- Keep AI-facing documentation in English.
- Verify behavior in `/tmp/...` unless the user explicitly asks to write into the real materials library.
- Keep README, launcher, and `docs/ai` docs aligned whenever changing setup or workflow.
