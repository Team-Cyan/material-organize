import logging
from collections import defaultdict
from datetime import datetime
from os import walk, makedirs
from pathlib import Path
from shutil import move
from typing import Dict, List, Optional

from exifread import process_file

logger = logging.getLogger(__name__)


class FileHelper:

    def __init__(self, root_path: str):
        self._root_path: str = root_path
        self.files_paths: List[Path] = []
        for dir_path, dir_names, file_names in walk(self._root_path):
            for file_name in file_names:
                self.files_paths.append(Path(dir_path, file_name))

    def _filter_by_suffixes(self, *suffixes: str) -> List[Path]:
        return [path for path in self.files_paths 
                if path.suffix.lstrip(".").lower() in suffixes]

    @staticmethod
    def _filter_by_keyword(paths: List[Path], keyword: str) -> List[Path]:
        return [path for path in paths 
                if keyword.lower() in path.name.lower()]

    @staticmethod
    def _check_target_path(target_path: str) -> Path:
        target_path = Path(target_path)
        if not target_path.is_dir():
            makedirs(target_path)
        return target_path

    def extract_raw(self, target_path: str) -> None:
        """Extract and organize RAW files by EXIF creation time.
        
        Args:
            target_path: Directory to move organized RAW files
            
        Raises:
            ValueError: If target_path cannot be created or is invalid
        """
        target_path = self._check_target_path(target_path)
        file_paths = self._filter_by_suffixes("raw", "arw")
        file_paths_by_create_time: Dict[datetime, List[Path]] = defaultdict(list)
        
        for file_path in file_paths:
            # Skip duplicate/test shots marked with " 2.ARW"
            if file_path.name.endswith(" 2.ARW"):
                logger.debug(f"Skipping duplicate: {file_path.name}")
                continue
            
            try:
                with open(file_path, "rb") as file:
                    file_info = process_file(file)
                    exif_datetime = file_info.get("EXIF DateTimeOriginal")
                    
                    if exif_datetime is None:
                        logger.warning(f"No EXIF DateTimeOriginal found: {file_path.name}")
                        continue
                    
                    create_time = datetime.strptime(
                        exif_datetime.values, "%Y:%m:%d %H:%M:%S"
                    )
                    file_paths_by_create_time[create_time].append(file_path)
                    
            except (OSError, IOError) as e:
                logger.error(f"Failed to read file {file_path.name}: {e}")
                continue
            except ValueError as e:
                logger.error(f"Failed to parse EXIF date from {file_path.name}: {e}")
                continue
        
        # Rename and move files
        for create_time, paths in file_paths_by_create_time.items():
            paths.sort(key=lambda p: p.name)
            for index, file_path in enumerate(paths, start=1):
                new_name = f"{create_time.strftime('%Y%m%d_%H%M%S')}_{index:02d}{file_path.suffix.lower()}"
                try:
                    move(str(file_path), str(target_path / new_name))
                    logger.info(f"Moved: {file_path.name} → {new_name}")
                except (OSError, IOError) as e:
                    logger.error(f"Failed to move {file_path.name} to {new_name}: {e}")

    def extract_mp4(self, target_path: str) -> None:
        """Extract and organize MP4 files by filename date prefix.
        
        Args:
            target_path: Directory to move organized MP4 files
            
        Raises:
            ValueError: If target_path cannot be created or is invalid
        """
        target_path = self._check_target_path(target_path)
        file_paths = self._filter_by_suffixes("mp4")
        file_paths_by_create_time: Dict[datetime, List[Path]] = defaultdict(list)
        
        for file_path in file_paths:
            # Skip SUB directory files (low-quality variants)
            if len(file_path.parts) >= 2 and file_path.parts[-2] == "SUB":
                logger.debug(f"Skipping SUB directory file: {file_path.name}")
                continue
            
            try:
                # Extract date from filename prefix (YYYYMMDD_...)
                date_str = file_path.name.split("_")[0]
                if len(date_str) != 8 or not date_str.isdigit():
                    logger.warning(f"Invalid date prefix in filename: {file_path.name}")
                    continue
                
                create_time = datetime.strptime(date_str, "%Y%m%d")
                file_paths_by_create_time[create_time].append(file_path)
                
            except ValueError as e:
                logger.error(f"Failed to parse date from {file_path.name}: {e}")
                continue
        
        # Rename and move files
        for create_time, paths in file_paths_by_create_time.items():
            paths.sort(key=lambda p: p.name)
            for index, file_path in enumerate(paths):
                new_name = f"{create_time.strftime('%Y%m%d')}_{index:03d}{file_path.suffix.lower()}"
                try:
                    move(str(file_path), str(target_path / new_name))
                    logger.info(f"Moved: {file_path.name} → {new_name}")
                except (OSError, IOError) as e:
                    logger.error(f"Failed to move {file_path.name} to {new_name}: {e}")
