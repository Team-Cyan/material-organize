# Material Importer Design

## Goal

Build a double-clickable importer for Sony camera media that copies RAW photos and videos into `/Users/lancer/materials`, grouped by trip day instead of natural day.

## Source Selection

- Prefer mounted SD cards under `/Volumes`.
- Treat any volume containing `DCIM` or `PRIVATE/M4ROOT` as a camera source.
- Import from every matching card when multiple cards are mounted.
- If no matching card is mounted, fall back to `/Users/lancer/import`.

## Media Rules

- Import photos from `.arw` and `.raw` only.
- Import videos from `.mp4`, `.mov`, and `.mxf`.
- Ignore hidden folders and Sony `SUB` variants.
- Copy media; never delete or move source files.

## Capture Time Rules

- Photos use `DateTimeOriginal`.
- Videos prefer embedded metadata from the media file.
- If video metadata is missing, fall back to Sony clip XML in `PRIVATE/M4ROOT/CLIP/*.XML`.
- If no capture time can be resolved, skip the file and report it.

## Trip Day Rules

- Trip day cutoff is `04:00`.
- Media captured between `00:00:00` and `03:59:59` belongs to the previous day.
- Output layout:
  - `/Users/lancer/materials/photos/YYYYMMDD`
  - `/Users/lancer/materials/videos/YYYYMMDD`
- Create `videos/YYYYMMDD` only when at least one video is imported for that day.

## Naming

- Photos: `raw_YYYYMMDD_HHMMSS_01.ext`
- Videos: `video_YYYYMMDD_HHMMSS_01.ext`
- Preserve the original extension in lowercase.
- When multiple files share the same second, increment the trailing counter.

## Duplicate Prevention

- Compute a SHA-256 hash for each source file before import.
- Store imported hashes in `/Users/lancer/materials/.material-import-manifest.jsonl`.
- Skip files whose hash already exists in the manifest.
- Also skip duplicates that appear twice in the same run.

## Runtime UX

- Provide a Poetry-managed CLI named `media-import`.
- Provide a double-click launcher at `/Users/lancer/import/media-import.command`.
- The launcher should:
  - Locate the repository automatically.
  - Run the CLI through Poetry.
  - Keep the Terminal window open so the summary is visible.

## Validation

- Unit-test source discovery, trip-day assignment, Sony XML fallback, manifest duplicate detection, and naming.
- Run the CLI against the mounted SD card for a real end-to-end verification.
