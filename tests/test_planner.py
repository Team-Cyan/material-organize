import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from material_importer.planner import DestinationPlanner, trip_day_for  # type: ignore


class PlannerTest(unittest.TestCase):
    def test_trip_day_rolls_back_before_cutoff(self) -> None:
        capture_time = datetime(2026, 4, 12, 3, 59, 59)

        self.assertEqual(trip_day_for(capture_time), "20260411")

    def test_allocates_sequential_names_per_second(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            planner = DestinationPlanner(Path(tmp_dir))
            capture_time = datetime(2026, 4, 12, 3, 59, 59)

            first_path = planner.allocate("photo", capture_time, ".ARW")
            second_path = planner.allocate("photo", capture_time, ".RAW")

            self.assertEqual(
                first_path,
                Path(tmp_dir) / "photos" / "20260411" / "raw_20260412_035959_01.arw",
            )
            self.assertEqual(
                second_path,
                Path(tmp_dir) / "photos" / "20260411" / "raw_20260412_035959_02.raw",
            )
