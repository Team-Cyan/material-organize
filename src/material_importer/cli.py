from __future__ import annotations

import argparse
from pathlib import Path

from material_importer.importer import build_default_importer
from material_importer.reporting import RichProgressReporter
from material_importer.sources import discover_source_roots


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import Sony media into materials folders.")
    parser.add_argument(
        "--materials-root",
        type=Path,
        default=Path("/Users/lancer/materials"),
        help="Destination root for imported materials.",
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        help="Explicit source directory to import from. When provided, SD card discovery is skipped.",
    )
    parser.add_argument(
        "--volumes-root",
        type=Path,
        default=Path("/Volumes"),
        help="Directory used to scan for mounted SD cards when --source-root is not provided.",
    )
    parser.add_argument(
        "--cutoff-hour",
        type=int,
        default=4,
        help="Hour before which media is assigned to the previous trip day.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.source_root is not None:
        source_root = args.source_root.expanduser().resolve()
        if not source_root.is_dir():
            print(f"Error: source root does not exist or is not a directory: {source_root}")
            return 1
        source_roots = [source_root]
    else:
        source_roots = discover_source_roots(
            volumes_root=args.volumes_root,
            fallback_root=None,
        )
        if not source_roots:
            print("Error: no SD card was detected. Drag an import folder onto the launcher or use --source-root.")
            return 1
    importer = build_default_importer(
        materials_root=args.materials_root,
        source_roots=source_roots,
        cutoff_hour=args.cutoff_hour,
    )
    try:
        importer.run(source_roots, reporter=RichProgressReporter())
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1
    return 0
