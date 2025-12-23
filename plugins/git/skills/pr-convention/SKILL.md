---
name: pr-convention
description: Use when creating GitHub pull requests. Provides PR title, body format, and labeling conventions.
---

## Format

### Title
`<category>: <description>`
- category: Same as branch category
- description: Summarize in Korean

Examples:
- `feat: 소셜 로그인(구글/카카오) 기능 구현`
- `fix: 결제 페이지 할인 쿠폰 미적용 버그 수정`
- `refactor: 주문 처리 로직 서비스 레이어로 분리`
- `perf: 상품 목록 조회 쿼리 N+1 문제 해결`

### Body

```markdown
## 1. 개요

**변경 내용**
(WHAT: Describe what was changed)

**배경**
(WHY: Explain why this change was necessary)

## 2. 주요 변경 사항
(HOW: Describe how you solved the problem)
- Change 1
- Change 2

## 3. 테스트
(Test command, verification method, or "없음")
```

### Labels
**At least 1 position label + at least 1 category label required**

#### Position Labels
| Label | Description |
|-------|-------------|
| @web | Web-related work |
| @server | Server feature addition or modification |
| @infra | Infrastructure-related work |
| @database | Database-related work |

#### Category Labels
| Label | Description |
|-------|-------------|
| feature | Add new feature |
| bug | Fix functional errors |
| remove | Remove unnecessary code or files |
| performance | Performance improvement (e.g., query optimization, memory reduction) |
| refactoring | Code refactoring (improve structure without changing functionality) |
| ci/cd | CI/CD related work |
| testing | Add or modify test code |
| dependencies | Dependency management (add, update libraries) |
| security | Security fixes (vulnerability improvements, authentication hardening) |
| development | Development environment setup |
| documentation | Add or modify documentation (including comments) |
| ignore-for-release | Exclude from release changelog (mainly internal config changes) |


## Constraints
- MUST EXCLUDE phrases like `Generated with Claude Code` or `Co-Authored-By: Claude` in PR messages
