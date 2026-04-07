# Knowledge Base Plugin

Karpathy 스타일의 LLM 지식 베이스를 Claude Code 플러그인으로 구현. 소스를 수집하고, LLM이 위키를 컴파일하고, 위키 기반으로 질의하고, 품질을 관리한다.

## 설정

플러그인을 처음 사용할 때 `/knowledge-base:setup`을 실행해서 초기화한다.

```
/knowledge-base:setup
```

setup이 하는 일:
- 지식 베이스 루트 경로를 대화형으로 수집 (경로 인자로 직접 지정도 가능)
- `~/.claude/knowledge-base/config`에 경로 저장
- 아래 디렉토리 구조 생성

```
{kb_root}/
  raw/                    # 원본 소스 (여기로 수집)
    images/{source}/      # URL에서 다운로드한 이미지
  wiki/                   # LLM이 컴파일한 위키
    index.md              # 전체 인덱스 (빈 스텁으로 시작)
    summaries/            # 소스별 요약
    concepts/             # 개념 문서
    connections/          # 개념 간 관계
  .kb_state.json          # 컴파일 상태 추적 (파일 해시, 첫 컴파일 시 생성)
```

경로를 바꾸고 싶으면 setup을 다시 실행하면 된다. 기존 데이터는 건드리지 않는다.

## 커맨드

### `/knowledge-base:setup [경로]`

지식 베이스를 초기화한다. 처음 사용할 때 **반드시 먼저 실행**해야 한다. 다른 커맨드들은 구조가 없으면 setup 실행 안내로 막는다.

```
/knowledge-base:setup
/knowledge-base:setup ~/Documents/my-kb
```

### `/knowledge-base:ingest <URL 또는 로컬 경로>`

소스를 지식 베이스에 수집한다. 수집 후 자동으로 증분 컴파일을 실행한다.

```
/knowledge-base:ingest https://example.com/interesting-article
/knowledge-base:ingest ./my-notes/research-paper.md
/knowledge-base:ingest ./papers/
```

- **URL:** 페이지를 다운로드하고, 이미지를 로컬에 저장하고, LLM이 HTML을 마크다운으로 정제
- **로컬 파일/디렉토리:** `raw/`로 복사

### `/knowledge-base:compile`

새로 추가되거나 수정된 raw 소스를 위키로 컴파일한다. 기본 증분 방식 (배치당 최대 10개 파일).

```
/knowledge-base:compile
```

10개 이상 대기 중이면 다시 실행해서 다음 배치를 처리한다.

### `/knowledge-base:ask <질문>`

컴파일된 지식 베이스를 기반으로 질문에 답변한다. RAG 없이 인덱스 기반 직접 읽기 방식.

```
/knowledge-base:ask 트랜스포머와 어텐션 메커니즘의 관계는?
/knowledge-base:ask 최근 수집한 ML 논문의 핵심 내용을 정리해줘
```

### `/knowledge-base:health-check`

지식 베이스 전체 건강 검진을 실행하고 발견된 문제를 자동 수정한다.

```
/knowledge-base:health-check
```

---

## 구현 상세

### 아키텍처: Prompt-Heavy / Script-Thin

모든 LLM 추론 로직은 **커맨드 .md 파일**(프롬프트)에 작성되어 있고, Python 스크립트는 LLM이 직접 수행할 수 없는 **기계적 I/O 작업만** 담당한다.

```
사용자 → 슬래시 커맨드 → 커맨드 .md (LLM 프롬프트)
                              │
                              ├── LLM이 직접: Read, Write, Glob, Grep
                              └── 스크립트 호출: Bash(python ...)
                                    │
                                    ├── kb_ingest_url.py (HTTP 다운로드)
                                    ├── kb_compile_status.py (해시 비교)
                                    └── kb_verify_integrity.py (구조 검증)
```

이 설계의 근거: 기존 플러그인 번들(git, daylog, playbook 등)이 모두 이 패턴을 따르고 있으며, `daylog-review.md`(84줄)가 복잡한 멀티스텝 워크플로우를 순수 프롬프트로 구현할 수 있음을 증명했다.

---

### `/knowledge-base:ingest` 구현 흐름

```
입력: URL 또는 로컬 파일 경로
  │
  ├─ URL인 경우:
  │   1. kb_ingest_url.py 호출 (stdin JSON으로 URL 전달)
  │      - urllib.request로 HTML 다운로드
  │      - HTMLParser로 <img> 태그 파싱, 이미지 URL 추출
  │      - 이미지를 raw/images/{source}/ 에 다운로드
  │      - 결과를 stdout JSON으로 반환
  │   2. LLM이 다운로드된 HTML을 읽고 마크다운으로 정제
  │      - 네비게이션, 광고, 스크립트 제거
  │      - 본문만 추출하여 깔끔한 .md로 변환
  │      - 이미지 참조를 로컬 경로로 교체
  │   3. raw/{source_name}.md 로 저장
  │
  └─ 로컬인 경우:
      1. cp 명령으로 raw/에 복사
      2. 디렉토리면 재귀 복사
  │
  └─ 이후 자동 증분 compile:
      1. kb_compile_status.py 호출 → 새 파일 감지
      2. LLM이 각 파일을 읽고:
         - wiki/summaries/ 에 요약 생성
         - wiki/concepts/ 에 개념 문서 생성/병합
         - wiki/connections/ 에 연결 문서 생성
         - wiki/index.md 재구축
      3. .kb_state.json 에 해시 업데이트
      4. kb_verify_integrity.py 로 무결성 검증
```

**핵심 포인트:**
- `kb_ingest_url.py`는 **stdlib만** 사용 (`urllib.request`, `html.parser`) — 외부 의존성 제로
- HTML → 마크다운 정제는 LLM이 담당 (스크립트는 단순 다운로드만)
- ingest 후 compile이 인라인으로 실행됨 (별도 커맨드 호출 아님, 플러그인 시스템이 cross-command 호출을 미지원하므로)

---

### `/knowledge-base:compile` 구현 흐름

```
1. kb_compile_status.py 호출 (stdin: {"kb_root": "..."})
   │
   ├─ raw/ 디렉토리 스캔
   ├─ .kb_state.json 의 기존 해시와 비교 (MD5)
   ├─ 새 파일 / 수정된 파일 분류
   └─ 최대 10개까지 batch 반환 (나머지는 remaining으로 보고)
   │
2. LLM이 batch의 각 파일을 처리:
   │
   ├─ 파일 읽기 (멀티모달: .md, .txt, .html, 이미지, PDF 지원)
   │
   ├─ 요약 생성 → wiki/summaries/{stem}.md
   │   - YAML 메타데이터 (source, compiled date, topics)
   │   - 3-5 단락 요약
   │   - 관련 concept 링크
   │
   ├─ 개념 추출 → wiki/concepts/{concept}.md
   │   - 파일명: lowercase-hyphenated (예: machine-learning.md)
   │   - 기존 파일 있으면: 읽고 병합 (append 아닌 rewrite)
   │   - 새 파일이면: 정의, 핵심 포인트, 소스 백링크
   │
   └─ 연결 발견 → wiki/connections/{a}--{b}.md
       - 파일명: 알파벳순 (중복 방지)
       - 양방향 관계 설명
   │
3. wiki/index.md 전체 재구축
   - 모든 wiki 디렉토리 스캔
   - 소스, 개념, 연결 목록 + 간략 설명
   - 최근 추가 항목
   - 500줄 초과 시 경고 표시
   │
4. .kb_state.json 업데이트 (성공한 파일만)
   │
5. kb_verify_integrity.py 실행 → 구조적 무결성 확인
```

**핵심 포인트:**
- **배치 캡 10개**: context window 오버플로우 방지. 대량 파일은 여러 번 실행
- **개념 병합(merge)**: 기존 concept 파일이 있으면 새 정보를 합쳐 재작성. append하면 중복/품질 저하
- **인덱스 전체 재구축**: 매 컴파일마다 index.md를 처음부터 다시 생성하여 항상 최신 상태 보장
- **상태 원자성**: `.kb_state.json`은 성공적으로 컴파일된 파일에 대해서만 해시를 업데이트. 부분 실패 시 미완료 파일은 pending 상태 유지

---

### `/knowledge-base:ask` 구현 흐름

```
1. wiki/index.md 읽기
   │  (1000줄 초과 시 경고)
   │  (wiki 비어있으면 "소스를 먼저 ingest하세요" 안내)
   │
2. 질문 분석 → 관련 문서 특정
   │  - 정의 질문 → concepts/ 우선
   │  - 소스별 질문 → summaries/ 우선
   │  - 관계 질문 → connections/ 우선
   │
3. 관련 파일만 Read (전체 위키를 읽지 않음)
   │
4. 답변 합성
   │  - 위키 내용에만 근거 (학습 데이터로 채우지 않음)
   │  - 파일 경로로 출처 인용
   │  - 답변 불가 시 명시 + ingest 제안
   │
5. 출력: 답변 + 출처 목록
```

**핵심 포인트:**
- **RAG 없음**: 벡터 DB, 임베딩 없이 index.md 기반 직접 읽기. Karpathy의 핵심 인사이트 — 소규모 개인 KB에서는 인덱스가 context window에 충분히 들어간다
- **선택적 읽기**: 인덱스에서 관련 문서만 골라 읽음. 전체 위키를 context에 넣지 않아 토큰 효율적
- **근거 기반 답변**: LLM 학습 지식이 아닌 위키 내용만으로 답변. 위키에 없는 내용은 "답변 불가"로 명시

---

### `/knowledge-base:health-check` 구현 흐름

```
Phase 1: 구조적 무결성 (결정론적)
  │  kb_verify_integrity.py 실행
  │  - 모든 컴파일된 raw 파일에 summary 존재하는지
  │  - connections/의 concept 참조가 실제 존재하는지
  │  - index.md에 모든 문서가 등록되어 있는지
  │  - 내부 마크다운 링크가 깨지지 않았는지
  │
Phase 2: 내용 일관성 (LLM)
  │  - 문서 간 모순 탐지 (concept ↔ summary 교차 검증)
  │  - 오래된 참조 발견
  │  - 요약과 원본 소스 간 사실 일치 확인
  │
Phase 3: 누락 데이터 보강
  │  - 3문장 미만의 빈약한 concept 파일 탐지
  │  - LLM 지식으로 보충 (모든 보강 내용에 [imputed] 마커)
  │  - (v2에서 웹 검색 기반 보강 예정)
  │
Phase 4: 연결 발견
  │  - 기존 concept들 사이의 미발견 관계 탐지
  │  - 새 connection 파일 자동 생성
  │
Phase 5: 자동 수정
  │  - 누락된 summary 재생성
  │  - 깨진 링크 수정/제거
  │  - 고아 파일 인덱스에 등록
  │  - index.md 전체 재구축
  │
Phase 6: 수정 후 재검증
  │  kb_verify_integrity.py 재실행
  │
Phase 7: 리포트 출력
   - 통계, 발견/수정 내역, 잔여 이슈
```

**핵심 포인트:**
- **이중 검증**: 결정론적 Python 스크립트(Phase 1)가 구조를 검증하고, LLM(Phase 2)이 내용을 검증. 같은 LLM이 만든 위키를 같은 LLM이 검증하는 "같은 모델 맹점" 문제를 구조적 검증 스크립트로 보완
- **[imputed] 마커**: LLM이 보강한 내용은 항상 표시하여 원본 데이터와 구분 가능
- **수정 후 재검증**: 자동 수정 후 다시 integrity 스크립트를 돌려 수정이 새 문제를 만들지 않았는지 확인

---

### Python 스크립트 상세

| 스크립트 | 줄 수 | 역할 | 입출력 |
|---|---|---|---|
| `kb_ingest_url.py` | 96줄 | URL HTML 다운로드 + 이미지 추출/저장 | stdin JSON → stdout JSON |
| `kb_compile_status.py` | 87줄 | raw/ 파일 해시 비교, 새/수정 파일 감지, 배치 캡 10 | stdin JSON → stdout JSON |
| `kb_verify_integrity.py` | 119줄 | 위키 구조적 무결성 검증 (4가지 체크) | stdin JSON → stdout JSON |

모든 스크립트는 **Python stdlib만** 사용 (외부 의존성 제로):
- `urllib.request` — HTTP 다운로드
- `html.parser` — HTML 파싱
- `hashlib` — MD5 해시
- `pathlib` — 경로 처리 (Windows 호환)
- `json` — 입출력 직렬화
