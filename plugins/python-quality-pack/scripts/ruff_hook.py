#!/usr/bin/env python3
"""
PostToolUse hook: Python 파일 편집 후 Ruff 린터/포맷터 실행
"""

import json
import os
import subprocess
import sys


def main():
    # Claude Code가 stdin으로 전달하는 hook input 파싱
    hook_input = json.loads(sys.stdin.read())

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Edit/Write 도구에서 파일 경로 추출
    file_path = tool_input.get("file_path", "")

    # Python 파일이 아니면 스킵
    if not file_path.endswith(".py"):
        return

    # 파일 존재 확인
    if not os.path.isfile(file_path):
        return

    # 1. Ruff check --fix (린트 검사 + 자동 수정)
    try:
        check_result = subprocess.run(
            ["ruff", "check", "--fix", file_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if check_result.returncode != 0:
            print(f"[Ruff Check] Issues in {file_path}:", file=sys.stderr)
            print(check_result.stdout, file=sys.stderr)
            if check_result.stderr:
                print(check_result.stderr, file=sys.stderr)
        else:
            print(f"[Ruff Check] {file_path} - OK", file=sys.stderr)

    except FileNotFoundError:
        print(
            "[Ruff] Error: ruff not installed. Run: pip install ruff", file=sys.stderr
        )
        sys.exit(2)
    except subprocess.TimeoutExpired:
        print(f"[Ruff Check] Timeout: {file_path}", file=sys.stderr)
        sys.exit(2)

    # 2. Ruff format (코드 포맷팅)
    try:
        format_result = subprocess.run(
            ["ruff", "format", file_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if format_result.returncode == 0:
            # 포맷팅 변경이 있었는지 확인
            if "1 file reformatted" in format_result.stderr:
                print(f"[Ruff Format] {file_path} - Reformatted", file=sys.stderr)
            else:
                print(f"[Ruff Format] {file_path} - OK", file=sys.stderr)
        else:
            print(f"[Ruff Format] Error: {format_result.stderr}", file=sys.stderr)

    except subprocess.TimeoutExpired:
        print(f"[Ruff Format] Timeout: {file_path}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"[Ruff] Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
