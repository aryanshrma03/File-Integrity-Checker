from hashlib import sha256
from pathlib import Path

CHUNK_SIZE = 1024 * 1024

def calculate_sha256(path: str | Path) -> str:
    """Return SHA-256 without loading the entire file into memory."""
    digest = sha256()

    with Path(path).open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            digest.update(chunk)

    return digest.hexdigest()
