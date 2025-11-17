from datetime import datetime
from os import walk, makedirs
from pathlib import Path
from shutil import move
from typing import Dict, List

from exifread import process_file


class FileHelper:

    def __init__(self, root_path: str):
        self._root_path: str = root_path
        self.files_paths: List[Path] = []
        for (dir_path, dir_names, file_names) in walk(self._root_path):
            for file_name in file_names:
                self.files_paths.append(Path(dir_path, file_name))

    def _filter_by_suffixes(self, *suffixes: str) -> List[Path]:
        return list(filter(lambda path: path.suffix.lstrip(".").lower() in suffixes, self.files_paths))

    @staticmethod
    def _filter_by_keyword(paths: List[Path], keyword: str) -> List[Path]:
        return list(filter(lambda path: keyword.lower() in path.name.lower(), paths))

    @staticmethod
    def _check_target_path(target_path: str) -> Path:
        target_path = Path(target_path)
        if not target_path.is_dir():
            makedirs(target_path)
        return target_path

    def extract_raw(self, target_path: str):
        target_path = self._check_target_path(target_path)
        file_paths = self._filter_by_suffixes("raw", "arw")
        file_paths_by_create_times: Dict[datetime: List[Path]] = {}
        for file_path in file_paths:
            if file_path.name.endswith(" 2.ARW"):
                continue
            with open(file_path, "rb") as file:
                file_info = process_file(file)
                create_time = datetime.strptime(file_info.get("EXIF DateTimeOriginal").values, "%Y:%m:%d %H:%M:%S")
                if file_paths_by_create_time := file_paths_by_create_times.get(create_time):
                    file_paths_by_create_time.append(file_path)
                else:
                    file_paths_by_create_times[create_time] = [file_path]
        for key, values in file_paths_by_create_times.items():
            values.sort(key=lambda path: path.name)
            for index, file_path in enumerate(values):
                converted_file_name = f"{key.strftime("%Y%m%d_%H%M%S")}_{index + 1:02d}{file_path.suffix.lower()}"
                move(file_path, Path(target_path, converted_file_name))

    def extract_mp4(self, target_path: str):
        target_path = self._check_target_path(target_path)
        file_paths = self._filter_by_suffixes("mp4")
        file_paths_by_create_times: Dict[datetime: List[Path]] = {}
        for file_path in file_paths:
            if file_path.parts[-2] == "SUB":
                continue
            create_time = datetime.strptime(file_path.name.split("_")[0], "%Y%m%d")
            if file_paths_by_create_time := file_paths_by_create_times.get(create_time):
                file_paths_by_create_time.append(file_path)
            else:
                file_paths_by_create_times[create_time] = [file_path]
        for key, values in file_paths_by_create_times.items():
            values.sort(key=lambda path: path.name)
            for index, file_path in enumerate(values):
                converted_file_name = f"{key.strftime("%Y%m%d")}_{index:03d}{file_path.suffix.lower()}"
                move(file_path, Path(target_path, converted_file_name))
