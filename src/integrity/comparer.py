from dataclasses import dataclass, field

@dataclass
class IntegrityReport:
    added: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    unreadable: list[str] = field(default_factory=list)

    @property
    def unchanged(self) -> int:
        return 0

    @property
    def total_changes(self) -> int:
        return (
            len(self.added)
            + len(self.modified)
            + len(self.deleted)
            + len(self.unreadable)
        )

    @property
    def score(self) -> int:
        score = (
            len(self.added) * 20
            + len(self.modified) * 50
            + len(self.deleted) * 60
            + len(self.unreadable) * 10
        )
        return min(100, score)

    @property
    def severity(self) -> str:
        score = self.score

        if score >= 80:
            return "CRITICAL"
        if score >= 60:
            return "HIGH"
        if score >= 40:
            return "MEDIUM"
        if score >= 20:
            return "LOW"
        return "NORMAL"

def compare_snapshots(baseline: dict, current: dict) -> IntegrityReport:
    report = IntegrityReport()

    baseline_paths = set(baseline)
    current_paths = set(current)

    report.added = sorted(current_paths - baseline_paths)
    report.deleted = sorted(baseline_paths - current_paths)

    for relative in sorted(baseline_paths & current_paths):
        old = baseline[relative]
        new = current[relative]

        if new.get("error") == "unreadable":
            report.unreadable.append(relative)
            continue

        if old.get("sha256") != new.get("sha256"):
            report.modified.append(relative)

    return report
