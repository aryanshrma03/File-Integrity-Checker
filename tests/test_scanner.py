import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from integrity.scanner import scan_directory


class ScannerTests(unittest.TestCase):

    def test_scan_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "hello.txt").write_text("hello", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "world.txt").write_text("world", encoding="utf-8")

            snapshot = scan_directory(root)

        self.assertEqual(set(snapshot), {"hello.txt", "nested/world.txt"})
        self.assertEqual(len(snapshot["hello.txt"]["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
