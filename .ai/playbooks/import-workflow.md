# Import Workflow

## When Changing Import Behavior

1. Update or add tests first in `tests/`.
2. Run:

```bash
poetry run python -m unittest discover -s tests -t . -v
```

3. Run one smoke check into a temporary destination:

```bash
poetry run media-import --materials-root /tmp/material-manager-smoke
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
- `scripts/media-import.command`
- `.github/copilot-instructions.md`
- `.ai/shared-context.md`

## When Adding New Material Features

- Keep the repository named `material-manager`.
- Add new CLI commands beside `media-import` rather than overloading one entry point.
- Document new workflows in `.ai/playbooks/` before expanding `.github/copilot-instructions.md`.
