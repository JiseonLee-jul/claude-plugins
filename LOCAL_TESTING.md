# Local Testing Guide

로컬 환경에서 플러그인을 테스트하는 방법입니다.

## 방법 1: `--plugin-dir` 플래그 사용

개별 플러그인을 직접 로드하여 테스트합니다.

```bash
# 특정 플러그인만 로드

claude --plugin-dir ./plugins/git

# 여러 플러그인 동시 로드
claude --plugin-dir ./plugins/git --plugin-dir ./plugins/file-context-sync
```

## 방법 2: 로컬 마켓플레이스 등록

전체 마켓플레이스를 로컬 경로로 등록합니다.

```bash
# Claude Code 내에서 실행
/plugin marketplace add F:\PROJECT\99_Claude_Plugins\00_git_pv

# 또는 해당 폴더에서 Claude 실행 시 상대 경로 사용
/plugin marketplace add .

# 플러그인 설치
/plugin install git@jiseonlee-plugins
```

## 방법 3: 플러그인 검증

배포 전 플러그인 구조를 검증합니다.

```bash
# 커맨드라인에서
claude plugin validate ./plugins/git

# Claude Code 내에서
/plugin validate ./plugins/git
```

## 권장 워크플로우

1. 코드 수정
2. `claude --plugin-dir ./plugins/{plugin-name}` 으로 새 세션 시작
3. 기능 테스트
4. 테스트 완료 후 GitHub에 push

> 변경사항 반영을 위해서는 Claude Code 세션을 재시작해야 합니다.
