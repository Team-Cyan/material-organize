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
        "--fallback-root",
        type=Path,
        default=Path("/Users/lancer/import"),
        help="Fallback source root when no SD card is mounted.",
    )
    parser.add_argument(
        "--volumes-root",
        type=Path,
        default=Path("/Volumes"),
        help="Directory used to scan for mounted SD cards.",
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
    source_roots = discover_source_roots(
        volumes_root=args.volumes_root,
        fallback_root=args.fallback_root,
    )
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
