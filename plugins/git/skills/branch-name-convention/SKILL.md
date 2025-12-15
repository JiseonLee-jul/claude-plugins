---
name: branch-name-convention
description: Use when creating or naming git branches. Provides consistent branch naming conventions.
---

# Format
`<folder>/<category>/<description-in-kebab-case>`

# foler
| 작업 폴더 | 설명 |
|----------|------|
| infra | 인프라 작업 폴더 |
| server | 백엔드 작업 폴더 |
| web | 프론트 작업 폴더 |

# category
| 카테고리 | 설명 |
|----------|------|
| feature | 새로운 기능 추가 |
| refactor | 기존 코드의 수정사항 |
| test | 기능에 대한 테스트 수행 |
| bug | 오류 사항 수정 |
| docs | 문서 작성 작업 |
| chore | 코드 수정사항 이외 작업 (주로 빌드 관련) |

# Examples
- `web/feature/email-verification-workflow`
- `web/bugfix/fix-login-error`
- `server/feature/add-user-profile`
- `server/feature/2fa-auth`
- `server/refactor/board-query-performance`
- `infra/test/build-performance`
- `infra/chore/ci-cd`