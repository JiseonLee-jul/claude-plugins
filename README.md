# JiseonLee Plugins

JiseonLee 개인용 Claude Code 플러그인 모음입니다. 반복적인 개발 작업을 자동화하고 생산성을 향상시키기 위해 제작되었습니다.

## Quick Start

Claude Code에 마켓플레이스 등록
```
/plugin marketplace add JiseonLee-jul/claude-plugins
```

플러그인 관리 인터페이스 열기
```
/plugin
```

특정 플러그인 설치
```
/plugin install {plugin_name}@jiseonlee-plugins
```

## Troubleshooting

### SSH 인증 실패 오류

마켓플레이스 추가 시 다음과 같은 오류가 발생하는 경우:

```
Error: Failed to clone marketplace repository: SSH authentication failed.
git@github.com: Permission denied (publickey).
```

**해결 방법:**

1. SSH 키 생성
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. 키 파일 확인 (자동으로 `~/.ssh/`에 저장됨)
   - `id_ed25519` (비밀키)
   - `id_ed25519.pub` (공개키)

3. 공개키 복사
   ```bash
   cat ~/.ssh/id_ed25519.pub | clip
   ```

4. GitHub에 공개키 등록
   - [github.com](https://github.com) 접속
   - 프로필 > Settings > SSH and GPG keys > New SSH key
   - 복사한 공개키 붙여넣기

5. SSH Agent에 키 등록
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

6. 연결 테스트
   ```bash
   ssh -T git@github.com
   ```
   성공 시: `Hi {username}! You've successfully authenticated...` 메시지 출력

## Plugin 목록

| 플러그인 | 버전 | 설명 |
|---------|-----|------|
| auto-test-generator | 0.1.0 | 시나리오 기반 테스트 코드 자동 생성 플러그인 |
| file-context-sync | 0.1.1 | 파일 외부 변경 감지 플러그인 |
| git | 1.0.2 | Git 작업 편의 기능을 제공하는 플러그인 |
| playbook | 0.1.0 | 코딩 전 사고를 돕는 요청 템플릿 모음 |
| python-quality-pack | 0.1.0 | Python 개발 품질 향상을 위한 도구 모음 |

## Plugin Schema

```
plugin-name/
├── .claude-plugin/           # 필수: 메타데이터 디렉토리
│   └── plugin.json          # 필수: 플러그인 매니페스트
├── commands/                 # 선택: 커맨드 정의
│   └── command.md
├── agents/                   # 선택: 에이전트 정의
│   └── agent.md
├── skills/                   # 선택: 에이전트 스킬
│   └── skill-name/
│       └── SKILL.md
├── hooks/                    # 선택: 훅 설정
│   └── hooks.json
├── .mcp.json                # 선택: MCP 서버 정의
├── scripts/                 # 선택: 훅 및 유틸리티 스크립트
│   └── script.sh
└── README.md                # 선택: 문서
```