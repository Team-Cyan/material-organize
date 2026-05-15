# AGENTS.md

This file is the repository entrypoint for coding agents.

Keep this file short. Treat it as a table of contents, not the full knowledge base.

## Read Order

For most tasks, read in this order:

1. `docs/ai/project-overview.md`
2. `docs/roadmap.md`
3. `docs/ai/modules/importer-boundaries.md`
4. one relevant file in `docs/ai/playbooks/`
5. `docs/operations/session-handoff.md` only if the task depends on recent unfinished work
6. `docs/ai/checklists/import-change-checklist.md` before finalizing import-related changes

Do not start by reading every historical note.

## Repository Model

- `AGENTS.md`: thin agent entrypoint
- `.agents/`: repo-local agent assets and reusable prompts
- `docs/ai/`: reusable AI knowledge base
- `docs/roadmap.md`: current repository state and next work
- `docs/operations/`: operator workflows and handoff notes
- `docs/`: durable documentation for humans and agents

## Working Rules

- Keep AI-facing docs in English.
- Reply to the human user in their preferred language.
- Prefer small, well-bounded sessions.
- Keep `.agents/` thin; keep durable knowledge in `docs/`.
- Verify behavior in `/tmp/...` unless the user explicitly asks to write into the real materials library.
- Keep README, launcher, and `docs/ai/` docs aligned whenever changing setup or workflow.

## Safety

- Keep secrets in gitignored local files.
- Do not commit credentials, tokens, or cookies.
- Prefer temporary destinations for verification instead of writing into the real materials library.

## Useful Docs

- `docs/README.md`
- `.agents/README.md`
- `docs/ai/README.md`
- `docs/ai/project-overview.md`
- `docs/ai/shared-context.md`
- `docs/ai/modules/importer-boundaries.md`
- `docs/ai/playbooks/import-workflow.md`
- `docs/ai/checklists/import-change-checklist.md`
- `docs/roadmap.md`
- `docs/operations/session-handoff.md`
