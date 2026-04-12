from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

MEDIA_DIRECTORIES = {
    "photo": "photos",
    "video": "videos",
}

FILE_PREFIXES = {
    "photo": "raw",
    "video": "video",
}


def trip_day_for(capture_time: datetime, cutoff_hour: int = 4) -> str:
    local_capture_time = _localize(capture_time)
    trip_day = local_capture_time.date()
    if local_capture_time.hour < cutoff_hour:
        trip_day -= timedelta(days=1)
    return trip_day.strftime("%Y%m%d")


class DestinationPlanner:
    def __init__(self, materials_root: Path, cutoff_hour: int = 4) -> None:
        self.materials_root = materials_root
        self.cutoff_hour = cutoff_hour
        self._counters: dict[tuple[Path, str], int] = {}

    def allocate(self, media_kind: str, capture_time: datetime, extension: str) -> Path:
        localized_capture_time = _localize(capture_time)
        trip_day = trip_day_for(localized_capture_time, self.cutoff_hour)
        directory = self.materials_root / MEDIA_DIRECTORIES[media_kind] / trip_day
        timestamp_token = localized_capture_time.strftime("%Y%m%d_%H%M%S")
        prefix = FILE_PREFIXES[media_kind]
        counter_key = (directory, timestamp_token)
        next_counter = self._counters.get(counter_key, 0) + 1
        candidate = directory / f"{prefix}_{timestamp_token}_{next_counter:02d}{extension.lower()}"
        while candidate.exists():
            next_counter += 1
            candidate = directory / f"{prefix}_{timestamp_token}_{next_counter:02d}{extension.lower()}"
        self._counters[counter_key] = next_counter
        return candidate


def _localize(capture_time: datetime) -> datetime:
    if capture_time.tzinfo is None:
        return capture_time
    return capture_time.astimezone()
