from __future__ import annotations

from pathlib import Path
from typing import Iterable

PHOTO_EXTENSIONS = {".arw", ".raw"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mxf"}


def discover_source_roots(
    volumes_root: Path = Path("/Volumes"),
    fallback_root: Path = Path("/Users/lancer/import"),
) -> list[Path]:
    if volumes_root.exists():
        camera_roots = sorted(
            path
            for path in volumes_root.iterdir()
            if path.is_dir() and not path.name.startswith(".") and is_camera_root(path)
        )
        if camera_roots:
            return camera_roots

    return [fallback_root]


def is_camera_root(root_path: Path) -> bool:
    return (root_path / "DCIM").exists() or (root_path / "PRIVATE" / "M4ROOT").exists()


def iter_media_files(source_roots: Iterable[Path]) -> Iterable[Path]:
    for source_root in source_roots:
        if not source_root.exists():
            continue
        for file_path in sorted(source_root.rglob("*")):
            if not file_path.is_file():
                continue
            if _is_hidden(file_path, source_root):
                continue
            if any(part.upper() == "SUB" for part in file_path.parts):
                continue
            if file_path.suffix.lower() in PHOTO_EXTENSIONS | VIDEO_EXTENSIONS:
                yield file_path


def media_kind_for(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix in PHOTO_EXTENSIONS:
        return "photo"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    raise ValueError(f"Unsupported media type: {file_path}")


def _is_hidden(file_path: Path, source_root: Path) -> bool:
    try:
        parts = file_path.relative_to(source_root).parts
    except ValueError:
        parts = file_path.parts
    return any(part.startswith(".") for part in parts)
