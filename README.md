# Wedatalab Plugins

Wedatalab AI Lab에서 개발한 사내 공용 Claude Code 플러그인 모음입니다. 반복적인 개발 작업을 자동화하고 팀 전체의 생산성을 향상시키기 위해 제작되었습니다.

## Quick Start

Claude Code에 마켓플레이스 등록
```
/plugin marketplace add WeDataLab-AI-Lab/claude-plugins
```

플러그인 관리 인터페이스 열기
```
/plugin
```

특정 플러그인 설치
```
/plugin install {plugin_name}@wedatalab-plugins
```

## Plugin 목록

| 플러그인 | 버전 | 설명 |
|---------|-----|------|
| auto-test-generator | 0.1.0 | 시나리오 기반 테스트 코드 자동 생성 플러그인 |

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