# Pixel Judge Extraction Notes

## Recommendation

Do not copy `/Users/lancer/projects/pixel-judge` into this repository as a module.

## Why

- `pixel-judge` is a full product repository, not a narrow reusable library.
- Pulling it in wholesale would import unrelated domain concepts, workflows, and maintenance burden.
- The main useful thing to borrow is its documentation pattern, not its business code.

## What To Reuse Instead

- `docs/ai/` documentation structure
- checklist and playbook style
- module-boundary documentation style
- handoff and workflow writing conventions

## What To Extract Only If Needed

- truly standalone media utilities
- isolated metadata helpers
- export/report helpers that have clear interfaces

## Expansion Strategy For `material-manager`

When the repository grows, prefer adding new commands beside `media-import`, for example:

- `media-audit`
- `media-report`
- `media-index`

If a future `pixel-judge` capability is needed, extract only the specific unit with tests and docs, not the whole repository.
