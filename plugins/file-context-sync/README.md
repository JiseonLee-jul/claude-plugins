# file-context-sync

Claude가 읽거나 수정한 파일이 외부에서 변경되면 자동으로 감지하여 알려주는 플러그인입니다.

## 기능

- **파일 추적**: Claude가 Read/Edit/Write/MultiEdit 도구로 접근한 파일의 상태(해시, mtime)를 저장
- **변경 감지**: 사용자가 메시지를 보낼 때 추적 중인 파일의 외부 변경을 감지
- **세션 관리**: 세션 시작/종료 시 캐시를 자동으로 관리

## 작동 방식

1. Claude가 파일을 읽거나 수정하면 해당 파일의 MD5 해시와 mtime을 `.claude-cache/cache.json`에 저장
2. 사용자가 메시지를 보내면 저장된 파일들의 현재 상태를 확인
3. 외부에서 변경된 파일이 있으면 Claude에게 알림

## 세션 생명주기

| 이벤트 | source/reason | 캐시 처리 |
|--------|---------------|----------|
| SessionStart | startup | 삭제 |
| SessionStart | clear | 삭제 |
| SessionStart | compact | 삭제 |
| SessionStart | resume | 유지 |
| SessionEnd | * | 삭제 |

## 파일 구조

```
plugins/file-context-sync/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   └── hooks.json
├── scripts/
│   ├── manage_cache.py
│   ├── record_file_access.py
│   └── detect_changes.py
└── README.md
```

## 캐시 구조

```json
// .claude-cache/cache.json
{
  "/absolute/path/to/file.py": {
    "hash": "d41d8cd98f00b204e9800998ecf8427e",
    "mtime": 1705312200.0
  }
}
```

## 성능

- mtime 우선 비교로 불필요한 해시 계산 최소화
- MD5 해시 계산: 50KB 파일 기준 약 0.05ms

## 스크립트 로직

### manage_cache.py (SessionStart/SessionEnd)

세션 생명주기에 따라 캐시를 관리합니다.

```
[세션 시작/종료]
       │
       ▼
┌──────────────────────┐
│ stdin에서 JSON 읽기  │
│ - hook_event_name    │
│ - cwd                │
│ - source (optional)  │
└──────────────────────┘
       │
       ▼
┌──────────────────────┐
│ hook_event_name 분기 │
└──────────────────────┘
       │
  ┌────┴────┐
  │         │
SessionStart SessionEnd
  │         │
  ▼         │
source?     │
  │         │
  ▼         ▼
startup,  ──────────────→ .claude-cache 폴더 삭제
clear,
compact

resume ──────────────────→ 캐시 유지 (아무것도 안 함)
```

### record_file_access.py (PostToolUse)

Claude가 Read/Edit/Write/MultiEdit 도구를 사용한 후 파일 상태를 저장합니다.

```
[Claude가 파일 도구 사용]
           │
           ▼
┌────────────────────────┐
│ stdin에서 JSON 읽기    │
│ - cwd                  │
│ - tool_input.file_path │
└────────────────────────┘
           │
           ▼
┌────────────────────────┐
│ file_path 절대경로화   │
└────────────────────────┘
           │
           ▼
┌────────────────────────┐
│ 파일 존재 확인         │
└────────────────────────┘
           │
           ▼
┌────────────────────────┐
│ mtime + MD5 해시 계산  │
└────────────────────────┘
           │
           ▼
┌────────────────────────┐
│ cache.json에 저장      │
│ {                      │
│   "/path/file.py": {   │
│     "hash": "abc...",  │
│     "mtime": 170531... │
│   }                    │
│ }                      │
└────────────────────────┘
```

### detect_changes.py (UserPromptSubmit)

사용자가 메시지를 보낼 때 캐시된 파일들의 외부 변경을 감지합니다.

```
[사용자가 메시지 전송]
           │
           ▼
┌────────────────────────┐
│ cache.json 로드        │
│ (없으면 종료)          │
└────────────────────────┘
           │
           ▼
┌────────────────────────┐
│ 각 캐시된 파일 순회    │
└────────────────────────┘
           │
           ▼
      파일 존재?
      ┌────┴────┐
      │         │
     No        Yes
      │         │
      ▼         ▼
 deleted     mtime 비교
 목록에         │
 추가           ▼
           mtime 같음?
           ┌────┴────┐
           │         │
          Yes       No
           │         │
           ▼         ▼
         스킵     해시 계산
        (최적화)    │
                    ▼
               해시 다름?
               ┌────┴────┐
               │         │
              Yes       No
               │         │
               ▼         ▼
          changed     캐시만
          목록에      업데이트
          추가
           │
           ▼
┌────────────────────────┐
│ updated_cache 저장     │
└────────────────────────┘
           │
           ▼
    변경된 파일 있음?
      ┌────┴────┐
      │         │
     Yes       No
      │         │
      ▼         ▼
  JSON 출력   종료
  (Claude에
   경고 전달)
```

**출력 예시:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "The following files have been modified externally:\n- src/main.py\n- src/utils.py (deleted)\n\nPlease check the current state of these files."
  }
}
```
