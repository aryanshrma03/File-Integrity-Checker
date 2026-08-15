import json
from pathlib import Path

import customtkinter as ctk
from tkinter import filedialog, messagebox

from components.controls import create_controls
from components.event_log import EventLog
from components.header import create_header
from components.risk_meter import RiskMeter
from config.theme import load_theme
from integrity.comparer import compare_snapshots
from integrity.scanner import scan_directory
from simulator.scenarios import demo_baseline, demo_current

load_theme()

class FileIntegrityApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("File Integrity Checker")
        self.root.geometry("1050x800")
        self.root.minsize(900, 700)

        self.selected_directory = None
        self.baseline = None

        create_header(self.root)

        self.path_label = ctk.CTkLabel(
            self.root,
            text="No directory selected",
            anchor="w",
            height=42,
            corner_radius=10,
            fg_color="#20242b",
            text_color="#b8c0cc",
        )
        self.path_label.pack(fill="x", padx=30, pady=(4, 4))

        create_controls(
            self.root,
            self.select_directory,
            self.create_baseline,
            self.verify_integrity,
            self.demo_changes,
            self.reset,
        )

        self.risk = RiskMeter(self.root)
        self.log = EventLog(self.root)

        self.stats = ctk.CTkLabel(
            self.root,
            text="Files: 0 | Added: 0 | Modified: 0 | Deleted: 0",
            text_color="#9aa4b2",
            font=("Segoe UI", 11),
        )
        self.stats.pack(anchor="w", padx=30, pady=(2, 5))

        ctk.CTkLabel(
            self.root,
            text="⚠ Integrity alerts indicate changes relative to the trusted baseline; investigate before treating them as malicious.",
            text_color="#9aa4b2",
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=30, pady=(0, 18))

        self.reset()

    def select_directory(self):
        path = filedialog.askdirectory(title="Select Directory to Monitor")
        if path:
            self.selected_directory = Path(path)
            self.path_label.configure(text=str(self.selected_directory))
            self.log.add(f"[INFO] Selected: {self.selected_directory}")

    def create_baseline(self):
        if not self.selected_directory:
            messagebox.showwarning("Directory Required", "Select a directory first.")
            return

        try:
            self.baseline = scan_directory(self.selected_directory)
        except Exception as exc:
            messagebox.showerror("Baseline Error", str(exc))
            return

        output = filedialog.asksaveasfilename(
            title="Save Integrity Baseline",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile="integrity-baseline.json",
        )

        if output:
            payload = {
                "version": 1,
                "algorithm": "sha256",
                "root": str(self.selected_directory),
                "files": self.baseline,
            }

            try:
                with open(output, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle, indent=2)
            except OSError as exc:
                messagebox.showerror("Save Error", str(exc))
                return

            self.log.add(f"[BASELINE] Saved {len(self.baseline)} file records.")
            self.log.add(f"[BASELINE] {output}")

        self._show_report(
            compare_snapshots(self.baseline, self.baseline),
            len(self.baseline),
            "BASELINE CREATED",
        )

    def verify_integrity(self):
        if not self.selected_directory:
            messagebox.showwarning("Directory Required", "Select a directory first.")
            return

        if self.baseline is None:
            path = filedialog.askopenfilename(
                title="Load Integrity Baseline",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            )
            if not path:
                return

            try:
                with open(path, "r", encoding="utf-8") as handle:
                    payload = json.load(handle)
                self.baseline = payload["files"]
            except Exception as exc:
                messagebox.showerror("Baseline Error", str(exc))
                return

        try:
            current = scan_directory(self.selected_directory)
            report = compare_snapshots(self.baseline, current)
        except Exception as exc:
            messagebox.showerror("Verification Error", str(exc))
            return

        self._show_report(report, len(current), "INTEGRITY VERIFICATION")

    def demo_changes(self):
        baseline = demo_baseline()
        current = demo_current()
        report = compare_snapshots(baseline, current)

        self._show_report(report, len(current), "SAFE DEMO")
        self.log.add("[INFO] Demo used synthetic snapshots only.")
        self.log.add("[INFO] No monitored files were created or modified.")

    def _show_report(self, report, file_count, source):
        self.risk.update(report)

        self.stats.configure(
            text=(
                f"Files: {file_count} | "
                f"Added: {len(report.added)} | "
                f"Modified: {len(report.modified)} | "
                f"Deleted: {len(report.deleted)} | "
                f"Unreadable: {len(report.unreadable)}"
            )
        )

        self.log.clear()
        self.log.add(f"[{source}] Severity: {report.severity}")
        self.log.add(f"[{source}] Risk score: {report.score}/100")
        self.log.add("")

        if not report.total_changes:
            self.log.add("[OK] No integrity changes detected.")
            return

        for path in report.added:
            self.log.add(f"[ADDED] {path}")

        for path in report.modified:
            self.log.add(f"[MODIFIED] {path}")

        for path in report.deleted:
            self.log.add(f"[DELETED] {path}")

        for path in report.unreadable:
            self.log.add(f"[UNREADABLE] {path}")

    def reset(self):
        self.selected_directory = None
        self.baseline = None
        self.path_label.configure(text="No directory selected")
        self.risk.update(compare_snapshots({}, {}))
        self.stats.configure(
            text="Files: 0 | Added: 0 | Modified: 0 | Deleted: 0 | Unreadable: 0"
        )
        self.log.clear()
        self.log.add("[INFO] File Integrity Checker reset and ready.")

    def run(self):
        self.root.mainloop()
