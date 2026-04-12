import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from material_importer.importer import MaterialImporter  # type: ignore


class StubResolver:
    def __init__(self, timestamps: dict[Path, datetime | None]) -> None:
        self.timestamps = timestamps

    def resolve(self, file_path: Path, media_kind: str) -> datetime | None:
        return self.timestamps.get(file_path)


class ImporterTest(unittest.TestCase):
    def test_imports_photos_and_skips_duplicates_and_missing_video_timestamps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source_root = root / "card"
            materials_root = root / "materials"
            photo_dir = source_root / "DCIM" / "100MEDIA"
            video_dir = source_root / "PRIVATE" / "M4ROOT" / "CLIP"
            photo_dir.mkdir(parents=True)
            video_dir.mkdir(parents=True)

            first_photo = photo_dir / "A7C05140.ARW"
            duplicate_photo = photo_dir / "A7C05141.ARW"
            missing_video = video_dir / "20260411_A7C2_0064.MP4"
            first_photo.write_bytes(b"same-photo")
            duplicate_photo.write_bytes(b"same-photo")
            missing_video.write_bytes(b"video-without-time")

            resolver = StubResolver(
                {
                    first_photo: datetime(2026, 4, 11, 9, 19, 12),
                    duplicate_photo: datetime(2026, 4, 11, 9, 19, 13),
                    missing_video: None,
                }
            )
            importer = MaterialImporter(
                materials_root=materials_root,
                timestamp_resolver=resolver,
            )

            summary = importer.run([source_root])

            imported_photo = (
                materials_root / "photos" / "20260411" / "raw_20260411_091912_01.arw"
            )
            self.assertTrue(imported_photo.exists())
            self.assertEqual(summary.imported_photos, 1)
            self.assertEqual(summary.imported_videos, 0)
            self.assertEqual(summary.skipped_duplicates, 1)
            self.assertEqual(summary.skipped_missing_timestamps, 1)
            self.assertFalse((materials_root / "videos").exists())

    def test_creates_video_folder_only_when_video_is_imported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source_root = root / "card"
            materials_root = root / "materials"
            video_dir = source_root / "PRIVATE" / "M4ROOT" / "CLIP"
            video_dir.mkdir(parents=True)
            video_path = video_dir / "20260411_A7C2_0064.MP4"
            video_path.write_bytes(b"video")

            importer = MaterialImporter(
                materials_root=materials_root,
                timestamp_resolver=StubResolver(
                    {video_path: datetime(2026, 4, 11, 10, 18, 58)}
                ),
            )

            summary = importer.run([source_root])

            imported_video = (
                materials_root / "videos" / "20260411" / "video_20260411_101858_01.mp4"
            )
            self.assertTrue(imported_video.exists())
            self.assertEqual(summary.imported_videos, 1)
