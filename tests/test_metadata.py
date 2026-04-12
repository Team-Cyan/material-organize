import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from material_importer.metadata import CaptureTimestampResolver, SonyClipIndex  # type: ignore


class FakeExifTool:
    def __init__(self, payloads: dict[Path, dict[str, str]]) -> None:
        self.payloads = payloads

    def read_tags(self, file_path: Path) -> dict[str, str]:
        return self.payloads[file_path]


class MetadataResolverTest(unittest.TestCase):
    def test_resolves_photo_capture_time_from_exif(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            photo_path = Path(tmp_dir) / "A7C05140.ARW"
            photo_path.write_bytes(b"raw")
            resolver = CaptureTimestampResolver(
                exiftool=FakeExifTool(
                    {
                        photo_path: {
                            "DateTimeOriginal": "2026:04:11 09:19:12",
                        }
                    }
                ),
                clip_index=SonyClipIndex({}),
            )

            capture_time = resolver.resolve(photo_path, "photo")

            self.assertEqual(capture_time, datetime(2026, 4, 11, 9, 19, 12))

    def test_falls_back_to_sony_clip_xml_for_video(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            source_root = Path(tmp_dir)
            clip_dir = source_root / "PRIVATE" / "M4ROOT" / "CLIP"
            clip_dir.mkdir(parents=True)
            video_path = clip_dir / "20260411_A7C2_0064.MP4"
            xml_path = clip_dir / "20260411_A7C2_0064M01.XML"
            video_path.write_bytes(b"video")
            xml_path.write_text(
                (
                    "<?xml version='1.0' encoding='UTF-8'?>"
                    "<NonRealTimeMeta>"
                    "<CreationDate value='2026-04-11T18:18:58+08:00'/>"
                    "</NonRealTimeMeta>"
                ),
                encoding="utf-8",
            )
            resolver = CaptureTimestampResolver(
                exiftool=FakeExifTool({video_path: {}}),
                clip_index=SonyClipIndex.from_source_roots([source_root]),
            )

            capture_time = resolver.resolve(video_path, "video")

            self.assertEqual(
                capture_time,
                datetime.fromisoformat("2026-04-11T18:18:58+08:00"),
            )
