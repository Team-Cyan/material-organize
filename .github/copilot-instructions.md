# Material Manager - AI Coding Instructions

## Project Overview
Material Manager is a Python CLI tool for batch organizing media files (RAW photos and MP4 videos) from a source directory into target folders with standardized naming. The tool extracts metadata (EXIF for RAW, filename parsing for MP4), groups by creation time, and renames files with a consistent format.

## Architecture & Data Flow

### Core Component: `FileHelper` Class (`utils/file_helper.py`)
The `FileHelper` class is the single service layer handling all file operations:

1. **Initialization**: Recursively scans the root path and builds a flat list of all file paths
2. **Filtering**: Generic `_filter_by_suffixes()` and static `_filter_by_keyword()` methods for file selection
3. **Processing**:
   - `extract_raw(target_path)`: Extracts RAW/ARW files, reads EXIF DateTimeOriginal, groups by creation time, renames to `YYYYMMDD_HHMMSS_NN.ext`
   - `extract_mp4(target_path)`: Extracts MP4 files, parses date from filename prefix, groups by date only, renames to `YYYYMMDD_NNN.ext`

### File Naming Conventions
- **RAW files**: Format `YYYYMMDD_HHMMSS_NN.ext` where NN increments from 01 for files with identical EXIF timestamps
- **MP4 files**: Format `YYYYMMDD_NNN.ext` where NNN is zero-padded index within the same-day group
- Both use lowercase extensions

### Key Design Patterns
- **Dictionary grouping**: Uses `datetime` objects as keys to group files by creation time (see `extract_raw()` line 38-44)
- **Walrus operator**: Leverages `:=` for dict lookups with fallback list creation (lines 40, 62)
- **Type hints**: Consistent use of `List[Path]`, `Dict[datetime, List[Path]]` throughout
- **Static methods**: Utility filters are static since they don't depend on instance state

## Special Cases & Edge Conditions
- **RAW files**: Skip files ending in ` 2.ARW` (assumed duplicates/test shots) in `extract_raw()`
- **MP4 files**: Skip files in `SUB` directories (line 61) to exclude low-quality variants
- **Directory creation**: Automatically creates target directories if they don't exist via `_check_target_path()`

## Development Setup & Workflows

### Installation
```bash
pip install -r requirements.txt  # Installs exifread >= 3.0.0
```

### Running the Tool
Edit `import_to_materials.py` to set:
- `target`: Date string in `YYYYMMDD` format (e.g., `"20251012"`)
- `source`: Path to directory containing import files (e.g., `/Users/lancer/import`)

Then run:
```bash
python import_to_materials.py
```

### Testing Workflow
- No automated test suite exists; test manually by running the script on sample files
- For RAW testing: Files must have valid EXIF DateTimeOriginal metadata
- For MP4 testing: Filenames must start with date in `YYYYMMDD` format

## Dependencies & External Integrations

### Key Dependency: `exifread`
- Used solely in `extract_raw()` to parse EXIF metadata
- Accessed via `process_file(file_handle)` → returns IFD dictionary with optional `"EXIF DateTimeOriginal"` key
- Always check for `None` before accessing EXIF values (see error handling pattern)

### Python Standard Library Usage
- `pathlib.Path`: All file path operations (filtering, sorting, moving)
- `os.walk()`: Recursive directory traversal in `__init__()`
- `shutil.move()`: File relocation after renaming with error handling
- `datetime.strptime()`: EXIF timestamp and MP4 filename parsing
- `logging`: Structured logging for visibility into file operations (see `extract_raw()` and `extract_mp4()`)
- `collections.defaultdict()`: Simplifies date-based grouping logic

## Error Handling Patterns

The refactored code includes comprehensive error handling:

1. **Missing EXIF Data**: Check if `get("EXIF DateTimeOriginal")` is `None` before accessing `.values` (line 70)
2. **File Read Failures**: Wrap file operations in try/except for `OSError`/`IOError` (lines 74-76)
3. **Date Parsing Failures**: Catch `ValueError` on invalid date formats (lines 81-82)
4. **Invalid MP4 Filenames**: Validate date prefix format and length before parsing (lines 118-120)
5. **Safe Directory Access**: Check `len(file_path.parts) >= 2` before accessing `parts[-2]` (line 115)
6. **File Move Failures**: Wrap move operations with try/except and log errors (lines 89-91, 130-132)

All errors are logged with context, allowing operations to continue for other files instead of crashing.

## When Extending This Project

### Adding New Media Types
1. Create a new `extract_<format>()` method following the pattern in `extract_raw()` or `extract_mp4()`
2. Use `_filter_by_suffixes()` for file selection
3. Implement date extraction logic (EXIF, filename parsing, or file metadata)
4. Maintain the naming convention: group → sort → rename → move
5. Add skip conditions for duplicates/unwanted files if needed
6. Implement comprehensive error handling with try/except blocks and logging
7. Use `defaultdict(list)` for grouping to avoid walrus operator complexity

### Modifying File Naming
- RAW sequence: Edit the format string in line 88 (currently `'%Y%m%d_%H%M%S'` + `_{index:02d}`)
- MP4 sequence: Edit the format string in line 129 (currently `'%Y%m%d'` + `_{index:03d}`)

### Code Style Guidelines
- Replace lambda functions with list comprehensions for readability (see `_filter_by_suffixes()`)
- Use f-strings consistently for formatting and logging
- Include docstrings on public methods with Args and Raises documentation
- Log at appropriate levels: DEBUG for skipped files, INFO for successful moves, WARNING/ERROR for issues
- Always validate external data before parsing (date format, EXIF keys, path components)

### Logging Configuration
The main script configures logging in `import_to_materials.py`:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```
Adjust the level to DEBUG for verbose output during development/troubleshooting.
