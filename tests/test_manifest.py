import tempfile
import unittest
from pathlib import Path

from material_importer.manifest import ManifestStore, compute_sha256  # type: ignore


class ManifestTest(unittest.TestCase):
    def test_loads_existing_hashes_and_appends_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "manifest.jsonl"
            manifest_path.write_text('{"sha256": "abc"}\n', encoding="utf-8")

            store = ManifestStore(manifest_path)

            self.assertTrue(store.has_hash("abc"))
            store.record({"sha256": "def", "target_path": "/tmp/file"})
            reloaded = ManifestStore(manifest_path)
            self.assertTrue(reloaded.has_hash("def"))

    def test_computes_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "sample.bin"
            file_path.write_bytes(b"material-importer")

            digest = compute_sha256(file_path)

            self.assertEqual(
                digest,
                "54d827ee2f9ee3220d7c8a14a5375070d5a0cdfbb3578bb93c9aa460959207bc",
            )
