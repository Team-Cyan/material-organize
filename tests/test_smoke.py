import unittest


class SmokeTest(unittest.TestCase):
    def test_package_imports(self) -> None:
        import material_importer  # type: ignore

        self.assertIsNotNone(material_importer)
