"""
Detect external file changes on user prompt submit.

Compares current file state with cached state and warns about changes.
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


def get_relative_path(file_path: str, cwd: str) -> str:
    """Get relative path from cwd if possible."""
    try:
        return os.path.relpath(file_path, cwd)
    except ValueError:
        return file_path


def main() -> None:
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        return

    cwd = input_data.get("cwd", "")

    if not cwd:
        return

    cache_path = get_cache_path(cwd)
    cache = load_cache(cache_path)

    if not cache:
        return

    changed_files = []
    deleted_files = []
    updated_cache = {}

    for file_path, file_info in cache.items():
        stored_hash = file_info.get("hash", "")
        stored_mtime = file_info.get("mtime", 0)

        if not os.path.isfile(file_path):
            deleted_files.append(file_path)
            continue

        try:
            current_mtime = os.path.getmtime(file_path)

            if current_mtime == stored_mtime:
                updated_cache[file_path] = file_info
                continue

            current_hash = calculate_hash(file_path)

            if current_hash != stored_hash:
                changed_files.append(file_path)

            updated_cache[file_path] = {
                "hash": current_hash,
                "mtime": current_mtime,
            }

        except (OSError, PermissionError):
            updated_cache[file_path] = file_info

    save_cache(cache_path, updated_cache)

    if changed_files or deleted_files:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": format_message(changed_files, deleted_files, cwd),
            }
        }
        print(json.dumps(output))


def format_message(changed_files: list, deleted_files: list, cwd: str) -> str:
    """Format the warning message for changed/deleted files."""
    lines = ["The following files have been modified externally:"]

    for file_path in changed_files:
        rel_path = get_relative_path(file_path, cwd)
        lines.append(f"- {rel_path}")

    for file_path in deleted_files:
        rel_path = get_relative_path(file_path, cwd)
        lines.append(f"- {rel_path} (deleted)")

    lines.append("")
    lines.append("Please check the current state of these files.")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
