def demo_baseline():
    return {
        "app/config.ini": {
            "sha256": "aaa111",
            "size": 100,
            "mtime_ns": 1,
        },
        "app/main.py": {
            "sha256": "bbb222",
            "size": 500,
            "mtime_ns": 2,
        },
        "docs/readme.txt": {
            "sha256": "ccc333",
            "size": 200,
            "mtime_ns": 3,
        },
    }

def demo_current():
    # Synthetic snapshots only; no files are created or changed.
    return {
        "app/config.ini": {
            "sha256": "CHANGED_HASH",
            "size": 120,
            "mtime_ns": 4,
        },
        "app/main.py": {
            "sha256": "bbb222",
            "size": 500,
            "mtime_ns": 2,
        },
        "app/new_module.py": {
            "sha256": "NEW_HASH",
            "size": 300,
            "mtime_ns": 5,
        },
    }
