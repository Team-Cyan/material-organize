SHELL := /bin/zsh
BREW := /opt/homebrew/bin/brew
MATERIALS_DIR := /Users/lancer/materials
LAUNCHER_SOURCE := scripts/import-here.command
LAUNCHER_TARGET := $(MATERIALS_DIR)/Import\ Here.command

.PHONY: setup deps-refresh deps-refresh-commit test smoke-test run install-launcher

setup:
	@command -v $(BREW) >/dev/null 2>&1 || { echo "Homebrew is required. Install Homebrew first."; exit 1; }
	$(BREW) bundle --file Brewfile
	uv sync --all-groups
	$(MAKE) install-launcher

deps-refresh:
	uv lock --upgrade
	uv sync --all-groups --reinstall
	$(MAKE) test

deps-refresh-commit:
	$(MAKE) deps-refresh
	@if git diff --quiet -- uv.lock; then \
		echo "uv.lock unchanged; nothing to commit."; \
	else \
		git add uv.lock; \
		git commit -m "chore(deps): refresh uv lock"; \
	fi

test:
	uv run python -m unittest discover -s tests -t . -v

smoke-test:
	rm -rf /tmp/material-organize-smoke
	@first_log=$$(mktemp /tmp/material-organize-smoke-first.XXXXXX); \
	second_log=$$(mktemp /tmp/material-organize-smoke-second.XXXXXX); \
	echo "First pass: import into /tmp/material-organize-smoke"; \
	uv run media-import --materials-root /tmp/material-organize-smoke --volumes-root /Volumes | tee "$$first_log"; \
	echo "Second pass: verify duplicate detection"; \
	uv run media-import --materials-root /tmp/material-organize-smoke --volumes-root /Volumes | tee "$$second_log"; \
	python3 scripts/verify-smoke-duplicates.py "$$second_log" || { echo "smoke-test failed: second pass did not report duplicates"; exit 1; }; \
	echo "smoke-test passed: duplicate detection confirmed on second run"

run:
	uv run media-import

install-launcher:
	mkdir -p "$(MATERIALS_DIR)"
	cp "$(LAUNCHER_SOURCE)" "$(LAUNCHER_TARGET)"
	chmod +x "$(LAUNCHER_TARGET)"
