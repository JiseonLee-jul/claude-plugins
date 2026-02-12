#!/usr/bin/env python3
"""
Stop hook: Ruff 린트 검증

Claude의 모든 편집이 완료된 시점(Stop)에 프로젝트 전체를 대상으로
ruff check --fix를 실행한다. 자동 수정 불가능한 문제가 남아 있으면
block을 반환하여 Claude에게 수정을 요청한다.
"""

import json
import os
import subprocess
import sys

LOCK_ENV_VAR = "RUFF_STOP_HOOK_ACTIVE"


def main():
    if os.environ.get(LOCK_ENV_VAR):
        return

    os.environ[LOCK_ENV_VAR] = "1"
    try:
        _run_check()
    finally:
        os.environ.pop(LOCK_ENV_VAR, None)


def _run_check():
    try:
        fix_result = subprocess.run(
            ["ruff", "check", "--fix", "."],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except FileNotFoundError:
        print(
            "[Ruff] Error: ruff not installed. Run: pip install ruff", file=sys.stderr
        )
        return
    except subprocess.TimeoutExpired:
        print("[Ruff Check] Timeout", file=sys.stderr)
        return

    if fix_result.returncode == 0:
        print("[Ruff Check] All clean", file=sys.stderr)
        return

    # 자동 수정 후에도 문제가 남아 있는지 재확인
    try:
        recheck_result = subprocess.run(
            ["ruff", "check", "."],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        print("[Ruff Check] Timeout on recheck", file=sys.stderr)
        return

    if recheck_result.returncode == 0:
        print("[Ruff Check] All issues auto-fixed", file=sys.stderr)
        return

    remaining = recheck_result.stdout.strip()
    decision = {
        "decision": "block",
        "reason": f"Ruff check found issues that require manual fix:\n{remaining}",
    }
    print(json.dumps(decision))


if __name__ == "__main__":
    main()
