"""
Record file access after Read/Edit/Write/MultiEdit tool use.

Saves file hash and mtime to cache.json for later change detection.
"""

import hashlib
import json
import os
import sys

CACHE_DIR_NAME = ".claude-cache"
CACHE_FILE_NAME = "cache.json"


def get_cache_path(cwd: str) -> str:
    """Get the cache file path for the current project."""
    return os.path.join(cwd, CACHE_DIR_NAME, CACHE_FILE_NAME)


def load_cache(cache_path: str) -> dict:
    """Load existing cache or return empty dict."""
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return {}
    return {}


def save_cache(cache_path: str, cache: dict) -> None:
    """Save cache to file."""
    cache_dir = os.path.dirname(cache_path)
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def calculate_hash(file_path: str) -> str:
    """Calculate MD5 hash of file content."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def normalize_path(file_path: str) -> str:
    """Normalize file path to absolute path."""
    return os.path.normpath(os.path.abspath(file_path))


def main() -> None:
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        return

    cwd = input_data.get("cwd", "")
    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not cwd or not file_path:
        return

    file_path = normalize_path(file_path)

    if not os.path.isfile(file_path):
        return

    try:
        mtime = os.path.getmtime(file_path)
        file_hash = calculate_hash(file_path)
    except (OSError, PermissionError):
        return

    cache_path = get_cache_path(cwd)
    cache = load_cache(cache_path)

    cache[file_path] = {
        "hash": file_hash,
        "mtime": mtime,
    }

    save_cache(cache_path, cache)


if __name__ == "__main__":
    main()
