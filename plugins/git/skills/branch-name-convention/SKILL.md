---
name: branch-name-convention
description: Use when creating or naming git branches. Provides consistent branch naming conventions.
---

# Format
`<folder>/<category>/[issue-number-]<description-in-kebab-case>`
- issue-number: Optional, include only when related issue exists

# Folder
| Folder | Description |
|--------|-------------|
| infra | Infrastructure work |
| server | Backend work |
| web | Frontend work |

# Category
| Category | Description |
|----------|-------------|
| feature | Add new feature |
| refactor | Modify existing code |
| fix | Fix bugs |
| test | Add or modify tests |
| docs | Documentation work |
| chore | Non-code changes (build, config, etc.) |

# Examples
- `web/feature/email-verification`
- `web/fix/42-login-error` (with issue)
- `server/refactor/board-query-performance`
- `infra/chore/ci-cd`