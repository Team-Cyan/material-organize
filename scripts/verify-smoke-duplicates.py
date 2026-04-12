from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify-smoke-duplicates.py <log-file>", file=sys.stderr)
        return 2

    log_path = Path(sys.argv[1])
    text = log_path.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    match = re.search(r"Skipped duplicates\D+([1-9][0-9]*)", text, re.S)
    return 0 if match else 1


if __name__ == "__main__":
    raise SystemExit(main())
