from __future__ import annotations

from collections import defaultdict
from dataclasses import field
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table

if TYPE_CHECKING:
    from material_importer.importer import ImportSummary


class ProgressReporter(Protocol):
    def start(self, total_files: int, source_roots: list[Path]) -> None: ...
    def processing(self, file_path: Path) -> None: ...
    def advance(self) -> None: ...
    def finish(self, summary: "ImportSummary") -> None: ...


class NullProgressReporter:
    def start(self, total_files: int, source_roots: list[Path]) -> None:
        return None

    def processing(self, file_path: Path) -> None:
        return None

    def advance(self) -> None:
        return None

    def finish(self, summary: "ImportSummary") -> None:
        return None


class RichProgressReporter:
    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.console,
            transient=False,
        )
        self.task_id: TaskID | None = None

    def start(self, total_files: int, source_roots: list[Path]) -> None:
        source_table = Table(title="Sources")
        source_table.add_column("Path")
        for source_root in source_roots:
            source_table.add_row(str(source_root))
        self.console.print(source_table)

        self.progress.start()
        self.task_id = self.progress.add_task(
            description="Preparing import",
            total=max(total_files, 1),
        )

    def processing(self, file_path: Path) -> None:
        if self.task_id is None:
            return
        self.progress.update(
            self.task_id,
            description=f"Processing {file_path.name}",
        )

    def advance(self) -> None:
        if self.task_id is None:
            return
        self.progress.advance(self.task_id)

    def finish(self, summary: "ImportSummary") -> None:
        if self.task_id is not None:
            self.progress.update(self.task_id, description="Import complete")
            self.progress.stop()
            self.task_id = None

        summary_table = Table(title="Import Summary")
        summary_table.add_column("Metric")
        summary_table.add_column("Value", justify="right")
        summary_table.add_row("Imported photos", str(summary.imported_photos))
        summary_table.add_row("Imported videos", str(summary.imported_videos))
        summary_table.add_row("Skipped duplicates", str(summary.skipped_duplicates))
        summary_table.add_row(
            "Skipped missing timestamps",
            str(summary.skipped_missing_timestamps),
        )
        self.console.print(summary_table)

        if summary.imported_trip_days:
            trip_day_table = Table(title="Imported By Trip Day")
            trip_day_table.add_column("Trip Day")
            trip_day_table.add_column("Photos", justify="right")
            trip_day_table.add_column("Videos", justify="right")
            for trip_day in sorted(summary.imported_trip_days):
                counts = summary.imported_trip_days[trip_day]
                trip_day_table.add_row(
                    trip_day,
                    str(counts["photo"]),
                    str(counts["video"]),
                )
            self.console.print(trip_day_table)

        if not summary.has_media:
            self.console.print("No new RAW photos or videos were imported.")
