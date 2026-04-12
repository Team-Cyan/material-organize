from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from shutil import copy2

from material_importer.manifest import ManifestStore, compute_sha256
from material_importer.metadata import CaptureTimestampResolver, SonyClipIndex
from material_importer.planner import DestinationPlanner
from material_importer.reporting import NullProgressReporter, ProgressReporter
from material_importer.sources import iter_media_files, media_kind_for


@dataclass
class ImportSummary:
    source_roots: list[Path]
    imported_photos: int = 0
    imported_videos: int = 0
    skipped_duplicates: int = 0
    skipped_missing_timestamps: int = 0
    imported_trip_days: dict[str, dict[str, int]] = field(
        default_factory=lambda: defaultdict(lambda: {"photo": 0, "video": 0})
    )

    @property
    def has_media(self) -> bool:
        return self.imported_photos > 0 or self.imported_videos > 0

    def record_import(self, media_kind: str, trip_day: str) -> None:
        if media_kind == "photo":
            self.imported_photos += 1
        else:
            self.imported_videos += 1
        self.imported_trip_days[trip_day][media_kind] += 1


class MaterialImporter:
    def __init__(
        self,
        materials_root: Path,
        timestamp_resolver: CaptureTimestampResolver | None = None,
        manifest_path: Path | None = None,
        cutoff_hour: int = 4,
    ) -> None:
        self.materials_root = materials_root
        self.timestamp_resolver = timestamp_resolver or CaptureTimestampResolver()
        self.manifest_store = ManifestStore(
            manifest_path or materials_root / ".material-import-manifest.jsonl"
        )
        self.destination_planner = DestinationPlanner(materials_root, cutoff_hour=cutoff_hour)

    def run(
        self,
        source_roots: list[Path],
        reporter: ProgressReporter | None = None,
    ) -> ImportSummary:
        summary = ImportSummary(source_roots=list(source_roots))
        seen_hashes: set[str] = set()
        active_reporter = reporter or NullProgressReporter()
        media_files = list(iter_media_files(source_roots))
        active_reporter.start(len(media_files), source_roots)

        for file_path in media_files:
            active_reporter.processing(file_path)
            media_kind = media_kind_for(file_path)
            capture_time = self.timestamp_resolver.resolve(file_path, media_kind)
            if capture_time is None:
                summary.skipped_missing_timestamps += 1
                active_reporter.advance()
                continue

            digest = compute_sha256(file_path)
            if digest in seen_hashes or self.manifest_store.has_hash(digest):
                summary.skipped_duplicates += 1
                active_reporter.advance()
                continue

            destination = self.destination_planner.allocate(
                media_kind,
                capture_time,
                file_path.suffix,
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            copy2(file_path, destination)
            self.manifest_store.record(
                {
                    "capture_time": capture_time.isoformat(),
                    "media_kind": media_kind,
                    "sha256": digest,
                    "source_path": str(file_path),
                    "target_path": str(destination),
                }
            )
            seen_hashes.add(digest)
            summary.record_import(media_kind, destination.parent.name)
            active_reporter.advance()

        active_reporter.finish(summary)
        return summary


def build_default_importer(
    materials_root: Path,
    source_roots: list[Path],
    cutoff_hour: int = 4,
) -> MaterialImporter:
    return MaterialImporter(
        materials_root=materials_root,
        timestamp_resolver=CaptureTimestampResolver(
            clip_index=SonyClipIndex.from_source_roots(source_roots)
        ),
        cutoff_hour=cutoff_hour,
    )
