---
name: commit-message-convention
description: Use when writing git commit messages. Enforces conventional commit format with Korean descriptions. Triggers on commit creation or commit message generation requests.
---

# Format

```
<type>: <title>

<body>

[footer]
```

# Types

| Type | Description |
|------|-------------|
| feat | Add new feature |
| fix | Fix a bug |
| refactor | Improve code structure without changing functionality |
| test | Add or update tests |
| docs | Update documentation (README, comments, etc.) |
| chore | Non-code changes (build, package management, etc.) |
| style | Code formatting, style changes (no logic changes) |
| remove | Remove unused code or files |
| perf | Performance improvements (query optimization, etc.) |

# Title Rules

- Maximum 50 characters
- End with action verb (추가, 수정, 변경, 제거, etc.)
- Describe WHAT was changed
- No period at the end

# Body Rules

- Separate from title with a blank line
- First paragraph: WHY (explain the problem or motivation)
- Second paragraph: HOW (describe the solution approach)
- Optional: bullet points for detailed changes
- Wrap at 72 characters per line

# Footer Rules (Optional)

- Reference related issues: `Resolves: #123` or `Fixes: #123`

# Examples

```
feat: 장바구니 담기 시 애니메이션 효과 추가

사용자가 버튼을 눌렀을 때 상품이 담겼는지 직관적으로 알기 어려움.
시각적 피드백을 주기 위해 상품이 장바구니 아이콘으로 날아가는 효과 구현.

- FlyToCart 컴포넌트 구현
- 기존 Toast 알림은 유지하되 노출 시간 1초로 단축

Resolves: #105
```

```
fix: 윤년 생일자 회원가입 시 앱 크래시 수정

DateUtil 라이브러리가 2월 29일을 유효하지 않은 날짜로 처리하여
생일 입력 단계에서 예외(Exception)가 발생하고 앱이 강제 종료됨.

라이브러리 버전을 v2.1.0으로 업그레이드하여 윤년 처리 로직 반영함.

Fixes: #204
```

```
refactor: 중복되는 결제 검증 로직 함수화

CreditCard, NaverPay, KakaoPay 클래스 내부에
동일하게 존재하는 '잔액 확인' 및 '유효성 검사' 로직이 중복되어 있음.

PaymentValidator 클래스로 공통 로직을 추출하여 유지보수성을 높임.
(기능 변경 사항 없음)
```

```
docs: README 설치 명령어 오타 수정

npm intsall -> npm install 로 수정.
초기 설정 시 복사-붙여넣기 하는 개발자들의 혼란 방지.
```