"""Detect which raw files need compilation by comparing file hashes.

Input (stdin JSON):
    {"kb_root": "..."}

Output (stdout JSON):
    {"new_files": [...], "modified_files": [...], "total_pending": N,
     "batch": [...], "remaining": N, "all_sources": [...]}

Batch size cap: 10 files per run.
"""

import hashlib
import json
import sys
from pathlib import Path

BATCH_SIZE = 10
STATE_FILE = ".kb_state.json"
SUPPORTED_EXTENSIONS = {
    ".md", ".txt", ".html", ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg",
}


def file_hash(path: Path) -> str:
    """Compute MD5 hash of a file."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state(kb_root: Path) -> dict:
    """Load the compile state file."""
    state_path = kb_root / STATE_FILE
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return {"compiled": {}}


def save_state(kb_root: Path, state: dict):
    """Save the compile state file."""
    state_path = kb_root / STATE_FILE
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def scan_raw_files(raw_dir: Path) -> list[Path]:
    """Scan raw/ for supported files, excluding images/ subdirectory."""
    if not raw_dir.exists():
        return []
    files = []
    for f in raw_dir.iterdir():
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(f)
    return sorted(files, key=lambda p: p.stat().st_mtime)


def main():
    data = json.loads(sys.stdin.read())
    kb_root = Path(data["kb_root"])
    raw_dir = kb_root / "raw"

    state = load_state(kb_root)
    compiled = state.get("compiled", {})

    raw_files = scan_raw_files(raw_dir)
    all_sources = [f.name for f in raw_files]

    new_files = []
    modified_files = []

    for f in raw_files:
        fname = f.name
        current_hash = file_hash(f)

        if fname not in compiled:
            new_files.append({"name": fname, "path": str(f), "hash": current_hash})
        elif compiled[fname] != current_hash:
            modified_files.append({"name": fname, "path": str(f), "hash": current_hash})

    pending = new_files + modified_files
    total_pending = len(pending)
    batch = pending[:BATCH_SIZE]
    remaining = max(0, total_pending - BATCH_SIZE)

    output = {
        "new_files": [f["name"] for f in new_files],
        "modified_files": [f["name"] for f in modified_files],
        "total_pending": total_pending,
        "batch": batch,
        "remaining": remaining,
        "all_sources": all_sources,
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
