#!/usr/bin/env python3
"""
PostToolUse hook: Python 파일 편집 후 Ruff format 실행

Edit/Write 도구 사용 후 .py 파일에 대해 ruff format만 수행한다.
코드 스타일(들여쓰기, 줄바꿈, 따옴표 등)만 정리하며,
코드를 삭제하거나 의미를 변경하지 않는다.
"""

import json
import os
import subprocess
import sys


def main():
    hook_input = json.loads(sys.stdin.read())
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path.endswith(".py"):
        return

    if not os.path.isfile(file_path):
        return

    try:
        result = subprocess.run(
            ["ruff", "format", file_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            if "1 file reformatted" in result.stderr:
                print(f"[Ruff Format] {file_path} - Reformatted", file=sys.stderr)
            else:
                print(f"[Ruff Format] {file_path} - OK", file=sys.stderr)
        else:
            print(f"[Ruff Format] Error: {result.stderr}", file=sys.stderr)

    except FileNotFoundError:
        print(
            "[Ruff] Error: ruff not installed. Run: pip install ruff", file=sys.stderr
        )
    except subprocess.TimeoutExpired:
        print(f"[Ruff Format] Timeout: {file_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
