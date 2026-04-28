# Module Boundaries

## `src/material_importer/sources.py`

- Owns source-root discovery and file enumeration.
- Safe changes:
  - adding new media suffixes
  - changing source selection rules
- Avoid mixing timestamp or copy logic into this module.

## `src/material_importer/metadata.py`

- Owns timestamp extraction from EXIF, media metadata, and Sony clip XML.
- Safe changes:
  - adding timestamp fallbacks
  - hardening parsing
- Avoid mixing destination planning or UI output here.

## `src/material_importer/planner.py`

- Owns trip-day mapping and destination filename allocation.
- Safe changes:
  - cutoff-hour behavior
  - naming scheme changes
- Avoid file-copy or manifest I/O here.

## `src/material_importer/manifest.py`

- Owns duplicate tracking and file hashing.
- Safe changes:
  - manifest schema extensions
  - hash strategy changes
- Avoid timestamp or copy behavior here.

## `src/material_importer/importer.py`

- Owns orchestration across discovery results, metadata resolution, deduplication, and copy operations.
- Safe changes:
  - import summary shape
  - sequencing and failure handling
- Avoid rich-terminal formatting details here.

## `src/material_importer/reporting.py`

- Owns terminal presentation only.
- Safe changes:
  - progress bar format
  - summary tables
- Avoid import-side behavior changes here.

## `src/material_importer/cli.py`

- Owns argument parsing and top-level wiring.
- Keep CLI defaults aligned with README and the `.command` launcher.
