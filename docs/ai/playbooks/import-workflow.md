# Import Workflow

## When Changing Import Behavior

1. Update or add tests first in `tests/`.
2. Run:

```bash
make test
```

3. Run a smoke check into a temporary destination:

```bash
make smoke-test
```

4. Confirm:
- expected source roots are shown
- trip-day folders are correct
- duplicate handling is correct on a second run
- real library paths were not touched unless requested

## When Changing Setup Or Entry Points

Update all of:

- `README.md`
- `Makefile`
- `scripts/import-here.command`
- `.github/copilot-instructions.md`
- `docs/ai/shared-context.md`

## When Adding New Material Features

- Keep the repository named `material-organize`.
- Add new CLI commands beside `media-import` rather than overloading one entry point.
- Document new workflows in `docs/ai/playbooks/` before expanding `.github/copilot-instructions.md`.
