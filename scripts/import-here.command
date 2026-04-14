#!/bin/zsh
set -euo pipefail

REPO_ROOT="${HOME}/projects/material-organize"
MATERIALS_ROOT="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -f "${REPO_ROOT}/pyproject.toml" ]]; then
  echo "Could not find the material-organize repository."
  echo "Expected: ${HOME}/projects/material-organize"
  echo
  read -k 1 "?Press any key to close..."
  exit 1
fi

cd "${REPO_ROOT}"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed."
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

if [[ $# -ge 1 ]]; then
  SOURCE_ROOT="$1"
  if [[ ! -d "${SOURCE_ROOT}" ]]; then
    echo "The dropped item is not a folder:"
    echo "  ${SOURCE_ROOT}"
    echo
    read -k 1 "?Press any key to close..."
    exit 1
  fi

  uv run media-import --materials-root "${MATERIALS_ROOT}" --source-root "${SOURCE_ROOT}"
else
  uv run media-import --materials-root "${MATERIALS_ROOT}"
fi
echo
read -k 1 "?Press any key to close..."
