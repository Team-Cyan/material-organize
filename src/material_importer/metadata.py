from __future__ import annotations

import json
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Iterable

PHOTO_TIMESTAMP_KEYS = (
    "DateTimeOriginal",
    "CreateDate",
    "ModifyDate",
)
VIDEO_TIMESTAMP_KEYS = (
    "DateTimeOriginal",
    "MediaCreateDate",
    "TrackCreateDate",
    "CreateDate",
    "ModifyDate",
)


class ExifToolClient:
    def __init__(self, executable: str = "exiftool") -> None:
        self.executable = executable

    def read_tags(self, file_path: Path) -> dict[str, str]:
        command = [
            self.executable,
            "-json",
            "-DateTimeOriginal",
            "-CreateDate",
            "-MediaCreateDate",
            "-TrackCreateDate",
            "-ModifyDate",
            str(file_path),
        ]
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                check=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("exiftool is not installed. Run `make setup`.") from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(exc.stderr.strip() or f"exiftool failed for {file_path}") from exc

        payload = json.loads(completed.stdout)
        return payload[0] if payload else {}


class SonyClipIndex:
    def __init__(self, clip_timestamps: dict[str, datetime]) -> None:
        self.clip_timestamps = clip_timestamps

    @classmethod
    def from_source_roots(cls, source_roots: Iterable[Path]) -> "SonyClipIndex":
        clip_timestamps: dict[str, datetime] = {}
        for source_root in source_roots:
            clip_dir = source_root / "PRIVATE" / "M4ROOT" / "CLIP"
            if not clip_dir.exists():
                continue
            for xml_path in sorted(clip_dir.glob("*.XML")):
                capture_time = _parse_sony_creation_date(xml_path)
                if capture_time is None:
                    continue
                clip_timestamps[_clip_lookup_key(xml_path)] = capture_time
        return cls(clip_timestamps)

    def lookup(self, video_path: Path) -> datetime | None:
        return self.clip_timestamps.get(_clip_lookup_key(video_path))


class CaptureTimestampResolver:
    def __init__(
        self,
        exiftool: ExifToolClient | None = None,
        clip_index: SonyClipIndex | None = None,
    ) -> None:
        self.exiftool = exiftool or ExifToolClient()
        self.clip_index = clip_index or SonyClipIndex({})

    def resolve(self, file_path: Path, media_kind: str) -> datetime | None:
        tags = self.exiftool.read_tags(file_path)
        keys = PHOTO_TIMESTAMP_KEYS if media_kind == "photo" else VIDEO_TIMESTAMP_KEYS
        for key in keys:
            capture_time = parse_timestamp(tags.get(key))
            if capture_time is not None:
                return capture_time
        if media_kind == "video":
            return self.clip_index.lookup(file_path)
        return None


def parse_timestamp(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None

    value = raw_value.strip()
    if not value or value.startswith("0000:00:00"):
        return None

    value = re.sub(r"([+-]\d{2}):(\d{2})$", r"\1\2", value)
    if "." in value and "T" in value:
        head, _, tail = value.partition(".")
        tail = tail[tail.find("+") :] if "+" in tail else tail[tail.find("-") :] if "-" in tail else ""
        value = f"{head}{tail}"

    parsers = (
        "%Y:%m:%d %H:%M:%S%z",
        "%Y:%m:%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S %z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
    )
    for parser in parsers:
        try:
            return datetime.strptime(value, parser)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(raw_value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _parse_sony_creation_date(xml_path: Path) -> datetime | None:
    try:
        root = ET.fromstring(xml_path.read_text(encoding="utf-8"))
    except (ET.ParseError, OSError, UnicodeDecodeError):
        return None

    for element in root.iter():
        if element.tag.endswith("CreationDate"):
            return parse_timestamp(element.attrib.get("value"))
    return None


def _clip_lookup_key(file_path: Path) -> str:
    stem = file_path.stem.upper()
    stem = re.sub(r"M\d\d$", "", stem)
    return stem
