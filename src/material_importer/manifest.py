from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class ManifestStore:
    def __init__(self, manifest_path: Path) -> None:
        self.manifest_path = manifest_path
        self._hashes = self._load_hashes()

    def has_hash(self, digest: str) -> bool:
        return digest in self._hashes

    def record(self, entry: dict[str, Any]) -> None:
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with self.manifest_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
        digest = entry.get("sha256")
        if isinstance(digest, str):
            self._hashes.add(digest)

    def _load_hashes(self) -> set[str]:
        if not self.manifest_path.exists():
            return set()

        hashes: set[str] = set()
        with self.manifest_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                digest = payload.get("sha256")
                if isinstance(digest, str):
                    hashes.add(digest)
        return hashes


def compute_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
