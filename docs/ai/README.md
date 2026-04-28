# AI Workspace

This directory is the AI-facing source of truth for `material-organize`.

## Read This First

1. `project-overview.md`
2. `shared-context.md`
3. `modules/importer-boundaries.md`
4. one relevant file in `playbooks/`
5. one relevant file in `checklists/` before finalizing changes

## Directory Layout

- `project-overview.md`: repository purpose, runtime model, and doc strategy
- `shared-context.md`: current assumptions, runtime surfaces, and core commands
- `modules/importer-boundaries.md`: ownership boundaries and safe edit zones
- `playbooks/import-workflow.md`: the main workflow for import-related changes
- `checklists/import-change-checklist.md`: final review checklist for importer changes
- `memory/ai-collaboration-decisions.md`: durable repository-level decisions for AI tools
- `reference/project-review-2026-04-12.md`: review findings and refine options

## Usage Notes

- Keep AI-facing docs in English.
- Prefer updating this directory over adding overlapping guidance elsewhere.
- If `.github/copilot-instructions.md` exists, treat it as a thin redirect into this folder.
