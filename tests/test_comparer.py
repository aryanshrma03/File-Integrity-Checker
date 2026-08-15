import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from integrity.comparer import compare_snapshots


class ComparerTests(unittest.TestCase):

    def test_added_modified_deleted(self):
        baseline = {
            "same.txt": {"sha256": "a"},
            "changed.txt": {"sha256": "old"},
            "deleted.txt": {"sha256": "gone"},
        }

        current = {
            "same.txt": {"sha256": "a"},
            "changed.txt": {"sha256": "new"},
            "added.txt": {"sha256": "new-file"},
        }

        report = compare_snapshots(baseline, current)

        self.assertEqual(report.added, ["added.txt"])
        self.assertEqual(report.modified, ["changed.txt"])
        self.assertEqual(report.deleted, ["deleted.txt"])
        self.assertEqual(report.score, 100)
        self.assertEqual(report.severity, "CRITICAL")

    def test_unchanged(self):
        snapshot = {
            "a.txt": {"sha256": "123"},
            "b.txt": {"sha256": "456"},
        }

        report = compare_snapshots(snapshot, snapshot)

        self.assertEqual(report.total_changes, 0)
        self.assertEqual(report.score, 0)
        self.assertEqual(report.severity, "NORMAL")

    def test_unreadable(self):
        baseline = {"secret.txt": {"sha256": "abc"}}
        current = {"secret.txt": {"error": "unreadable"}}

        report = compare_snapshots(baseline, current)

        self.assertEqual(report.unreadable, ["secret.txt"])
        self.assertEqual(report.score, 10)


if __name__ == "__main__":
    unittest.main()
