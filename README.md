# Material Manager

Material Manager is a Python tool for organizing and extracting RAW photos and MP4 videos from a source directory, sorting them by creation time, and moving them to target folders with standardized filenames.

## Features
- Extract RAW files (e.g., .raw, .arw) and sort by EXIF creation time
- Extract MP4 files and sort by filename date
- Automatically renames files to a consistent format
- Ignores duplicate and unwanted files

## Requirements
- Python 3.8+
- exifread >= 3.0.0

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Edit `main.py` to set your target date and source directory. Example:
```python
from utils.file_helper import FileHelper

target = "20250920"
source = FileHelper("/Users/lancer/import")
source.extract_raw(f"/Users/lancer/materials/{target}/photo")
source.extract_mp4(f"/Users/lancer/materials/{target}/video")
```
Run the script:
```bash
python main.py
```

## For AI Agents
- The main entry point is `main.py`.
- Core logic is in `utils/file_helper.py` (`FileHelper` class).
- `extract_raw(target_path)` and `extract_mp4(target_path)` are the main methods for file extraction and sorting.
- All file operations use Python's standard libraries and `exifread` for EXIF data.

## License
MIT