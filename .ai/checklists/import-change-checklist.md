# Import Change Checklist

- Tests cover the changed behavior.
- `make test` passes.
- Smoke verification writes to `/tmp/...`, not the real materials library.
- README matches current repository root, launcher path, and CLI command.
- `.github/copilot-instructions.md` matches the current architecture.
- `.ai/shared-context.md` and `.ai/architecture/module-boundaries.md` still reflect reality.
- `scripts/media-import.command` points at `~/projects/material-manager`.
