SHELL := /bin/zsh
BREW := /opt/homebrew/bin/brew
POETRY := /opt/homebrew/bin/poetry
IMPORT_DIR := /Users/lancer/import
LAUNCHER_SOURCE := scripts/media-import.command
LAUNCHER_TARGET := $(IMPORT_DIR)/media-import.command

.PHONY: setup test smoke-test run install-launcher

setup:
	@command -v $(BREW) >/dev/null 2>&1 || { echo "Homebrew is required. Install Homebrew first."; exit 1; }
	$(BREW) bundle --file Brewfile
	$(POETRY) install
	$(MAKE) install-launcher

test:
	$(POETRY) run python -m unittest discover -s tests -t . -v

smoke-test:
	rm -rf /tmp/material-manager-smoke
	@first_log=$$(mktemp /tmp/material-manager-smoke-first.XXXXXX); \
	second_log=$$(mktemp /tmp/material-manager-smoke-second.XXXXXX); \
	echo "First pass: import into /tmp/material-manager-smoke"; \
	$(POETRY) run media-import --materials-root /tmp/material-manager-smoke --volumes-root /Volumes --fallback-root /Users/lancer/import | tee "$$first_log"; \
	echo "Second pass: verify duplicate detection"; \
	$(POETRY) run media-import --materials-root /tmp/material-manager-smoke --volumes-root /Volumes --fallback-root /Users/lancer/import | tee "$$second_log"; \
	python3 scripts/verify-smoke-duplicates.py "$$second_log" || { echo "smoke-test failed: second pass did not report duplicates"; exit 1; }; \
	echo "smoke-test passed: duplicate detection confirmed on second run"

run:
	$(POETRY) run media-import

install-launcher:
	mkdir -p "$(IMPORT_DIR)"
	cp "$(LAUNCHER_SOURCE)" "$(LAUNCHER_TARGET)"
	chmod +x "$(LAUNCHER_TARGET)"
