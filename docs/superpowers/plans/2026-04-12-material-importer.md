# Material Importer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the repository as a uv-managed `material_importer` project that imports Sony RAW photos and videos into `/Users/lancer/materials` by trip day.

**Architecture:** A small CLI package discovers source roots, extracts capture timestamps with `exiftool` plus Sony XML fallback, groups media by trip day, deduplicates by SHA-256 manifest, and copies files into stable destination folders. A separate `.command` launcher in `/Users/lancer/materials` invokes the CLI through uv for double-click use and accepts a dropped source folder when needed.

**Tech Stack:** Python 3.13+, uv, standard library `unittest`, external `exiftool`

---

### Task 1: Project Skeleton

**Files:**
- Create: `pyproject.toml`
- Create: `src/material_importer/__init__.py`
- Create: `src/material_importer/__main__.py`
- Create: `tests/test_smoke.py`

- [ ] **Step 1: Write the failing test**

```python
import unittest


class SmokeTest(unittest.TestCase):
    def test_package_imports(self) -> None:
        import material_importer

        self.assertIsNotNone(material_importer)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_smoke.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'material_importer'`

- [ ] **Step 3: Write minimal implementation**

Create a uv project using `src/` layout and add an empty package with `__main__.py`.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python3 -m unittest tests/test_smoke.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/material_importer/__init__.py src/material_importer/__main__.py tests/test_smoke.py
git commit -m "build: create material importer package skeleton"
```

### Task 2: Source Discovery

**Files:**
- Create: `src/material_importer/sources.py`
- Create: `tests/test_sources.py`

- [ ] **Step 1: Write the failing test**

Add tests that:
- detect two mounted card roots under a fake `/Volumes`
- return no sources when no card is mounted and no explicit source is provided

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python3 -m unittest tests/test_sources.py -v`
Expected: FAIL because `material_importer.sources` does not exist

- [ ] **Step 3: Write minimal implementation**

Implement helpers that:
- identify camera roots by `DCIM` or `PRIVATE/M4ROOT`
- return all mounted card roots
- return no sources when no cards exist and no explicit fallback is provided

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python3 -m unittest tests/test_sources.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/material_importer/sources.py tests/test_sources.py
git commit -m "feat: add import source discovery"
```

### Task 3: Metadata Extraction

**Files:**
- Create: `src/material_importer/metadata.py`
- Create: `tests/test_metadata.py`

- [ ] **Step 1: Write the failing test**

Add tests that:
- parse `exiftool` JSON-style capture timestamps
- fall back from missing video metadata to Sony clip XML

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python3 -m unittest tests/test_metadata.py -v`
Expected: FAIL because `material_importer.metadata` does not exist

- [ ] **Step 3: Write minimal implementation**

Implement:
- `CaptureTimestampResolver`
- `SonyClipIndex`
- parsing helpers for photo and video timestamps

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python3 -m unittest tests/test_metadata.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/material_importer/metadata.py tests/test_metadata.py
git commit -m "feat: resolve capture timestamps"
```

### Task 4: Planning and Deduplication

**Files:**
- Create: `src/material_importer/planner.py`
- Create: `src/material_importer/manifest.py`
- Create: `tests/test_planner.py`
- Create: `tests/test_manifest.py`

- [ ] **Step 1: Write the failing tests**

Add tests that:
- assign `03:59` media to the previous trip day
- produce stable destination filenames
- skip hashes already recorded in the manifest

- [ ] **Step 2: Run tests to verify they fail**

Run: `PYTHONPATH=src python3 -m unittest tests/test_planner.py tests/test_manifest.py -v`
Expected: FAIL because the planner and manifest modules do not exist

- [ ] **Step 3: Write minimal implementation**

Implement:
- trip day calculation with a configurable cutoff
- destination path allocation
- JSONL manifest load and append helpers
- SHA-256 hashing for files

- [ ] **Step 4: Run tests to verify they pass**

Run: `PYTHONPATH=src python3 -m unittest tests/test_planner.py tests/test_manifest.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/material_importer/planner.py src/material_importer/manifest.py tests/test_planner.py tests/test_manifest.py
git commit -m "feat: plan destinations and deduplicate imports"
```

### Task 5: Import Runner and CLI

**Files:**
- Create: `src/material_importer/cli.py`
- Create: `src/material_importer/importer.py`
- Create: `tests/test_importer.py`

- [ ] **Step 1: Write the failing test**

Add tests that:
- copy files into `photos/YYYYMMDD` and `videos/YYYYMMDD`
- avoid creating a video folder when there are no imported videos
- report skipped duplicates and skipped missing timestamps

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python3 -m unittest tests/test_importer.py -v`
Expected: FAIL because the importer modules do not exist

- [ ] **Step 3: Write minimal implementation**

Implement:
- end-to-end import orchestration
- CLI summary output
- package entry point `media-import`

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python3 -m unittest tests/test_importer.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/material_importer/cli.py src/material_importer/importer.py tests/test_importer.py
git commit -m "feat: add import runner and cli"
```

### Task 6: Double-Click Launcher and Real Verification

**Files:**
- Create: `/Users/lancer/materials/Import Here.command`
- Modify: `README.md`

- [ ] **Step 1: Write the failing verification command**

Run the launcher manually and confirm it does not yet exist.

- [ ] **Step 2: Run check to verify it fails**

Run: `ls /Users/lancer/materials/Import\ Here.command`
Expected: FAIL with `No such file or directory`

- [ ] **Step 3: Write minimal implementation**

Add a launcher that:
- locates the repository automatically
- runs `uv run media-import`
- pauses for review before closing

Update the README with uv and launcher usage.

- [ ] **Step 4: Run verification**

Run:
- `uv run python -m unittest discover -s tests -v`
- `uv run media-import --materials-root /tmp/materials-test --source-root /path/to/import-folder`
- `open /Users/lancer/materials/Import\ Here.command` for a manual smoke test if needed

Expected:
- all tests PASS
- CLI prints imported counts and duplicate skips

- [ ] **Step 5: Commit**

```bash
git add README.md scripts/import-here.command
git commit -m "feat: add double-click launcher"
```
