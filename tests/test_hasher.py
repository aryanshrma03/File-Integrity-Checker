import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from integrity.hasher import calculate_sha256


class HasherTests(unittest.TestCase):

    def test_sha256(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("hello integrity", encoding="utf-8")

            expected = hashlib.sha256(
                b"hello integrity"
            ).hexdigest()

            self.assertEqual(calculate_sha256(path), expected)


if __name__ == "__main__":
    unittest.main()
