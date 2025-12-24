"""
Manage cache lifecycle based on session events.

- SessionStart (source: startup, clear, compact): Delete cache
- SessionStart (source: resume): Keep cache
- SessionEnd: Delete cache
"""

import json
import os
import shutil
import sys

CACHE_DIR_NAME = ".claude-cache"


def get_cache_dir(cwd: str) -> str:
    """Get the cache directory path for the current project."""
    return os.path.join(cwd, CACHE_DIR_NAME)


def delete_cache(cwd: str) -> None:
    """Delete the cache directory if it exists."""
    cache_dir = get_cache_dir(cwd)
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)


def main() -> None:
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        return

    hook_event_name = input_data.get("hook_event_name", "")
    cwd = input_data.get("cwd", "")

    if not cwd:
        return

    if hook_event_name == "SessionStart":
        source = input_data.get("source", "")
        if source in ("startup", "clear", "compact"):
            delete_cache(cwd)
        # source == "resume": keep cache

    elif hook_event_name == "SessionEnd":
        delete_cache(cwd)


if __name__ == "__main__":
    main()
