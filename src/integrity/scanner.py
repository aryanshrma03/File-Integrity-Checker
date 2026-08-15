from pathlib import Path

from integrity.hasher import calculate_sha256

DEFAULT_EXCLUDED = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
}

def scan_directory(root: str | Path, excluded: set[str] | None = None) -> dict:
    """Return a JSON-serializable snapshot of files under root."""
    root = Path(root).resolve()
    excluded = excluded or DEFAULT_EXCLUDED
    snapshot = {}

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in excluded for part in path.parts):
            continue

        relative = path.relative_to(root).as_posix()

        try:
            stat = path.stat()
            snapshot[relative] = {
                "sha256": calculate_sha256(path),
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        except (PermissionError, OSError):
            snapshot[relative] = {
                "error": "unreadable",
            }

    return snapshot
