# AI Workspace

This directory is the AI-facing source of truth for `material-manager`.

## Read This First

1. `shared-context.md`
2. `architecture/module-boundaries.md`
3. one relevant file in `playbooks/`
4. one relevant file in `checklists/` before finalizing changes

## Directory Layout

- `shared-context.md`: repository purpose, runtime assumptions, and core commands
- `architecture/module-boundaries.md`: ownership boundaries and safe edit zones
- `playbooks/import-workflow.md`: the main workflow for import-related changes
- `checklists/import-change-checklist.md`: final review checklist for importer changes
- `memory/ai-collaboration-decisions.md`: durable repository-level decisions for AI tools
- `reference/project-review-2026-04-12.md`: current project review findings and refine options

## Usage Notes

- Keep AI-facing docs in English.
- Prefer updating this directory over adding overlapping guidance elsewhere.
- If `.github/copilot-instructions.md` exists, treat it as a thin redirect into this folder.
