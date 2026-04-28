# Session Handoff

## Repository State

- current branch: check local git state before assuming anything about tracked history
- important recent commit: not recorded in this handoff yet

## Durable Knowledge Already Recorded

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `docs/ai/README.md`
- `docs/ai/project-overview.md`
- `docs/ai/shared-context.md`
- `docs/ai/modules/importer-boundaries.md`
- `docs/ai/playbooks/import-workflow.md`
- `docs/ai/checklists/import-change-checklist.md`
- `docs/roadmap.md`

## Current Focus

This repo should keep the importer workflow cheap to understand: thin root entrypoint, durable docs under `docs/ai/`, and verification guidance that defaults to `/tmp/...` instead of the real materials library.

## What Changed Recently

- Migrated the old top-level `.ai/` guidance into `docs/ai/`
- Added thin root routing via `AGENTS.md`
- Added roadmap and session-handoff docs so future sessions do not need to rediscover the safe verification path

## Recommended Next Task

- Refresh the importer module or playbook docs whenever behavior changes materially
- Keep launcher, README, and docs in sync if setup or entrypoint behavior changes
