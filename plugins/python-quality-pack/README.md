# Python Quality Pack Plugin

Python 개발 품질 향상을 위한 Claude Code 플러그인입니다. 코드 편집 시 자동으로 Ruff 린터/포맷터를 실행합니다.

## 요구사항

이 플러그인은 **Ruff**가 필요합니다.

### 설치

```bash
pip install ruff
```

또는 프로젝트에 이미 ruff가 의존성으로 포함되어 있다면 별도 설치 불필요합니다.

---

## 기능 요약

| 구분 | 이름 | 설명 |
|------|------|------|
| Hook | `PostToolUse` | Python 파일 편집 후 Ruff 자동 실행 |

## 설치

```bash
/plugin install python-quality-pack@jiseonlee-plugins
```

---

## Hooks

### PostToolUse (Edit/Write)

Python 파일을 편집하거나 생성할 때 자동으로 실행됩니다.

**동작:**
1. `Edit` 또는 `Write` 도구로 `.py` 파일 수정 감지
2. `ruff check --fix` 실행 (린트 검사 + 자동 수정)
3. `ruff format` 실행 (코드 포맷팅)

**지원 파일:**
- `.py` 확장자 파일만 처리
- 존재하지 않는 파일은 스킵
