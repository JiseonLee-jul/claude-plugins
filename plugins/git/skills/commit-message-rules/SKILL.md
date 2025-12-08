---
name: commit-message-rules
description: Use when writing git commit messages. Enforces conventional commit format with Korean descriptions. Triggers on commit creation or commit message generation requests.
---

# Format
`<type>: <description>`

# types
| Type | 설명 |
|------|------|
| feat | 새로운 기능 추가 |
| fix | 오류 사항 수정 |
| refactor | 코드 개선 및 구조 변경 (기능 변경 없이 리팩토링) |
| test | 기능에 대한 테스트 코드 추가/수정 |
| docs | 문서 작성 및 수정 (주석, 설명 추가 등) |
| chore | 코드 이외 작업 (빌드, 패키지 관리 등) |
| style | 코드 포맷팅, 스타일 수정 (기능이나 로직 변경 없이) |
| remove | 불필요한 코드나 파일 삭제 |
| perf | 성능 개선 (예: 쿼리 최적화, 로직 개선) |

# Examples
`feat: UserService에 loginUser 메서드 추가하여 사용자 로그인 처리`
`fix: UserController의 registerUser 메서드에서 NullPointerException 수정`
`refactor: AuthService의 generateToken 메서드 리팩토링으로 코드 가독성 개선`
`docs: UserService에 있는 checkPassword 메서드 설명 주석 추가`
`remove: AuthUtils 클래스 내 사용되지 않는 validateCredentials 메서드 제거`