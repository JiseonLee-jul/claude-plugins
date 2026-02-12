# Python Quality Pack Plugin

Python 개발 품질 향상을 위한 Claude Code 플러그인입니다. 코드 편집 시 자동으로 Ruff 포맷터/린터를 실행합니다.

## 요구사항

이 플러그인은 **Ruff**가 필요합니다.

### 설치

```bash
pip install ruff
```

또는 프로젝트에 이미 ruff가 의존성으로 포함되어 있다면 별도 설치 불필요합니다.

---

## 기능 요약

| 구분 | 이벤트 | 스크립트 | 설명 |
|------|--------|----------|------|
| Hook | `PostToolUse` (Edit/Write) | `ruff_format.py` | 파일 편집 직후 포맷팅 |
| Hook | `Stop` | `ruff_check.py` | 작업 완료 시 린트 검증 |

## 설치

```bash
/plugin install python-quality-pack@jiseonlee-plugins
```

---

## Hooks

### PostToolUse - ruff format

Edit 또는 Write 도구로 `.py` 파일을 수정할 때마다 자동으로 `ruff format`을 실행한다.

- 코드 스타일(들여쓰기, 줄바꿈, 따옴표 등)만 정리
- 코드를 삭제하거나 의미를 변경하지 않음
- 편집 직후 즉시 실행되므로, 작성 중인 import가 삭제되는 문제 없음

### Stop - ruff check

Claude의 모든 편집이 완료된 시점에 프로젝트 전체를 대상으로 `ruff check --fix`를 실행한다.

- 린트 규칙 위반을 검사하고 자동 수정 가능한 항목은 수정
- 자동 수정 불가능한 문제가 남아 있으면 block을 반환하여 Claude에게 수정 요청
- 환경 변수 `RUFF_STOP_HOOK_ACTIVE`로 무한 루프 방지

### format과 check의 역할 분리 이유

`ruff check --fix`는 unused import 삭제(F401), 미사용 변수 제거(F841) 등 코드를 삭제/변경할 수 있다. 파일 편집 직후(PostToolUse)에 실행하면, Claude가 import를 추가한 뒤 아직 사용 코드를 작성하기 전에 해당 import를 삭제해버리는 문제가 발생한다.

이를 방지하기 위해:
- **PostToolUse**: `ruff format`만 실행 (스타일 정리, 코드 삭제 없음)
- **Stop**: `ruff check --fix` 실행 (모든 편집 완료 후 린트 검증)
