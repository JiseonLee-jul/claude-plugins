# Git Plugin

Git 작업 편의 기능을 제공하는 Claude Code 플러그인입니다. 커밋, PR 생성, 브랜치 관리 등 반복적인 Git 작업을 자동화합니다.

## 기능 요약

| 구분 | 이름 | 설명 |
|------|------|------|
| Command | `/git:setup` | GitHub MCP 서버 설정 가이드 |
| Command | `/git:commit` | 변경사항을 자동 분석하여 커밋 생성 |
| Command | `/git:pr` | PR 생성 (push + gh pr create) |
| Command | `/git:issue` | GitHub Issue와 연동된 브랜치 생성 |
| Command | `/git:cleanup` | 삭제된 원격 브랜치의 로컬 정리 |
| Skill | `commit-message-rules` | Conventional Commit 형식 가이드 |
| Skill | `branch-name` | 브랜치 네이밍 컨벤션 |
| Skill | `pr-rules` | PR 작성 규칙 |

## 설치

```bash
/plugin install git@wedatalab-plugins
```

## Commands

### `/git:setup`

GitHub MCP 서버 설정 가이드를 제공합니다.

**사용법:**
```bash
/git:setup
```

**동작:**
1. GitHub Personal Access Token (PAT) 생성 방법 안내
2. GitHub MCP 서버 추가 명령어 제공
3. 설정 확인 방법 안내

---

### `/git:commit [message]`

현재 변경사항을 분석하여 커밋을 생성합니다.

**사용법:**
```bash
/git:commit                         # 자동 메시지 생성
/git:commit feat: 로그인 기능 추가    # 직접 메시지 지정
```

**동작:**
1. `git status`와 `git diff`로 변경사항 분석
2. 메시지가 없으면 `commit-message-rules`에 따라 자동 생성
3. 변경사항 스테이징 후 커밋

---

### `/git:pr`

현재 브랜치의 변경사항을 기반으로 Pull Request를 생성합니다.

**사용법:**
```bash
/git:pr
```

**동작:**
1. `origin/HEAD..HEAD` 범위의 커밋 분석
2. 원격에 브랜치 push
3. `pr-rules`에 따라 PR 제목/본문 자동 생성
4. `gh pr create`로 PR 생성

---

### `/git:issue <issue-number>`

GitHub Issue와 연동된 브랜치를 생성합니다.

**사용법:**
```bash
/git:issue 42
```

**동작:**
1. Issue 정보 조회 (`gh issue view`)
2. `branch-name` 규칙에 따라 브랜치명 생성
3. `gh issue develop`으로 Issue와 연결된 브랜치 생성

---

### `/git:cleanup`

원격에서 삭제된 브랜치(`[gone]`)를 로컬에서 정리합니다.

**사용법:**
```bash
/git:cleanup
```

**동작:**
1. `[gone]` 상태인 로컬 브랜치 탐색
2. 연결된 worktree가 있으면 함께 제거
3. 브랜치 삭제

## Skills

플러그인 설치 시 자동으로 적용되는 규칙입니다.

### commit-message-rules

Conventional Commit 형식을 따르는 커밋 메시지 규칙입니다.

**형식:** `<type>: <description>`

**예시:**
```
feat: UserService에 loginUser 메서드 추가
fix: UserController의 NullPointerException 수정
refactor: AuthService의 generateToken 메서드 가독성 개선
```

---

### branch-name

브랜치 네이밍 컨벤션입니다.

**형식:** `<folder>/<category>/<description-in-kebab-case>`

**예시:**
```
web/feature/email-verification-workflow
server/bug/fix-login-error
infra/chore/ci-cd
```

---

### pr-rules

Pull Request 작성 규칙입니다.

**제목:** `<category>: <한글 설명>`

**본문:**
```markdown
## 1. 개요
(배경 및 목적 요약)

## 2. 주요 변경 사항
- 변경사항 1
- 변경사항 2

## 3. 테스트 방법
(테스트 방법이 없으면 "없음")
```
