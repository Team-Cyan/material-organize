#!/bin/zsh
set -euo pipefail

REPO_ROOT="${HOME}/projects/material-manager"

if [[ ! -f "${REPO_ROOT}/pyproject.toml" ]]; then
  echo "Could not find the material-manager repository."
  echo "Expected: ${HOME}/projects/material-manager"
  echo
  read -k 1 "?Press any key to close..."
  exit 1
fi

cd "${REPO_ROOT}"

if ! command -v poetry >/dev/null 2>&1; then
  echo "poetry is not installed."
  echo "Run: make setup"
  echo
  read -k 1 "?Press any key to close..."
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  echo "Python environment is not ready."
  echo "Run: make setup"
  echo
  read -k 1 "?Press any key to close..."
  exit 1
fi

poetry run media-import "$@"
echo
read -k 1 "?Press any key to close..."
