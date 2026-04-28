# Import Change Checklist

- Tests cover the changed behavior.
- `make test` passes.
- `make smoke-test` passes.
- Smoke verification writes to `/tmp/...`, not the real materials library.
- README matches current repository root, launcher path, and CLI command.
- `.github/copilot-instructions.md` matches the current architecture.
- `docs/ai/shared-context.md` and `docs/ai/modules/importer-boundaries.md` still reflect reality.
- `scripts/import-here.command` points at `~/projects/material-organize`.
