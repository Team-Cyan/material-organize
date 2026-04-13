import tempfile
import unittest
from pathlib import Path

from material_importer.sources import discover_source_roots  # type: ignore


class SourceDiscoveryTest(unittest.TestCase):
    def test_discovers_all_camera_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            volumes_root = Path(tmp_dir) / "Volumes"
            fallback_root = Path(tmp_dir) / "import"
            card_a = volumes_root / "CardA"
            card_b = volumes_root / "CardB"
            (card_a / "DCIM").mkdir(parents=True)
            (card_b / "PRIVATE" / "M4ROOT").mkdir(parents=True)
            fallback_root.mkdir()

            roots = discover_source_roots(
                volumes_root=volumes_root,
                fallback_root=fallback_root,
            )

            self.assertEqual(roots, [card_a, card_b])

    def test_falls_back_to_import_folder_when_no_cards_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            volumes_root = Path(tmp_dir) / "Volumes"
            fallback_root = Path(tmp_dir) / "import"
            volumes_root.mkdir()
            fallback_root.mkdir()

            roots = discover_source_roots(
                volumes_root=volumes_root,
                fallback_root=fallback_root,
            )

            self.assertEqual(roots, [fallback_root])

    def test_returns_empty_when_no_cards_exist_and_no_fallback_is_given(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            volumes_root = Path(tmp_dir) / "Volumes"
            volumes_root.mkdir()

            roots = discover_source_roots(
                volumes_root=volumes_root,
                fallback_root=None,
            )

            self.assertEqual(roots, [])

    def test_default_behavior_does_not_invent_legacy_import_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            volumes_root = Path(tmp_dir) / "Volumes"
            volumes_root.mkdir()

            roots = discover_source_roots(volumes_root=volumes_root)

            self.assertEqual(roots, [])
