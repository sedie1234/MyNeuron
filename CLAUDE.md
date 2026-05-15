# MyNeuron - 지식 축적 시스템

이 프로젝트는 개인 지식 축적 시스템입니다. Claude Code agent가 지식의 수집, 정리, 연결, 회상을 돕습니다.

## Agent 설정 로드

이 디렉토리에서 Claude Code를 실행할 때, 아래 agent 설정을 참조하여 동작합니다:
- **공유 원칙**: `agent/neuron-agent.md` (모든 에이전트가 준수)
- **서브에이전트 정의**: `agent/agents/*.md` — role + tools + skill 포인터 (얇음)
- **스킬 정의**: `agent/skills/*/SKILL.md` — 활성화 조건 + 역할 + workflow 포인터 (얇음)
- **워크플로우 정의**: `agent/workflows/*.md` — step-by-step 절차 (두꺼움)
- **전체 구조**: `agent/README.md`

> **대전제**:
> - 모든 Claude 설정은 `agent/`에서 단일 source of truth로 관리됨.
> - `.claude/`에는 새 설정 파일을 만들지 않음. `.claude/agents`, `.claude/skills`는 `agent/`로 향하는 symlink일 뿐.
> - **모든 스킬은 SKILL + workflow를 분리**해서 관리한다.

## 서브에이전트 라우팅 정책

`agent/agents/`에 정의된 7개 서브에이전트로 위임한다.

### 라우팅 표

| 사용자 요청 유형 | 서브에이전트 | 주 스킬 | 트리거 예시 |
|---------------|------------|--------|----------|
| **새 지식 저장/전이** | `knowledge-curator` | `transfer-knowledge` | "지식 전이", "이거 저장해줘", "기억 전이", "neuron에 추가" |
| **기존 지식 검색** | `knowledge-searcher` | `search-knowledge` | "neuron에 X 있어?", "이전에 다룬 X", "관련 지식 보여줘" |
| **부분 정리/유지보수** | `knowledge-organizer` | `organize-knowledge` | "지식 정리", "중복 찾기", "끊긴 링크 점검", "X 카테고리 정리" |
| **트리 전체 재구축** | `knowledge-reorganizer` | `reorganize-tree` | "내부 지식 정리", "트리 재구축", "neuron 재분류", "전체 카테고리 재정비" |
| **질문 답변 (학습/탐구)** | `knowledge-qa` | `answer-question` + `clarify-question` | "X 설명", "X와 Y 차이", "왜 X?", 일반 기술/이론 질문 |
| **mdbook 생성** | `mdbook-builder` | `create-knowledge-mdbook` | "X mdbook 만들어줘", "X 책으로 정리" |
| **공부 리스트 관리** | `study-tracker` | `manage-study-list` | "todo 추가", "공부할 거 추가", "다음 공부 제안" |

### 라우팅 원칙

1. **명확한 매칭이면 즉시 위임**
2. **모호하면 메인 에이전트가 직접 처리** — 단순 대화, 메타 질문 등
3. **복합 요청은 순차 위임** — "X에 대해 설명하고 저장해줘" → knowledge-qa → knowledge-curator
4. **서브에이전트 간 호출 가능** — knowledge-qa가 knowledge-searcher 활용 등
5. **백그라운드 위임 권장** — mdbook-builder처럼 시간 소요 큰 작업은 `run_in_background=true`
6. **organizer vs reorganizer 분기**:
   - 부분/특정 카테고리/소량(10-50건) → `knowledge-organizer`
   - 전체 트리/대량(100건+)/전면 재분류 → `knowledge-reorganizer`

### 서브에이전트 미사용 케이스

다음은 메인 에이전트가 직접 처리:
- 단순 인사, 짧은 응답
- 명령 실행 (bash, git 등 단순)
- 설정 변경 (skill, settings.json 등)
- 메타 질문 ("어떤 에이전트가 있어?", "이 세션 뭐 했어?" 등)

### 스킬 활용 패턴

- **clarify-question**: 모든 에이전트(특히 qa, mdbook-builder, curator)에서 모호한 요청에 적용
- **search-knowledge**: qa, mdbook-builder, organizer 등의 사전 검색 단계
- **각 스킬은 SKILL + workflow 분리** — SKILL.md는 활성화 조건, workflow는 절차
- **시스템 스킬** (update-config, init 등)은 메인 에이전트 영역

## neuron/ 디렉토리 정책 — Tree 기반

`neuron/`은 **top-level(관점) × domain tree(주제)** 의 2축 구조.

### Top-level

| 디렉토리 | 의미 | 단위 |
|---------|------|------|
| `이론/` | 이론·원리 (영구 보존) | domain tree 직속 |
| `지식/` | 확정·전이된 지식 | domain tree 직속 |
| `실험/` | 실험 기록 | `<project>/<domain tree>` |
| `프로젝트/` | 프로젝트 기반 지식 | `<project>/<domain tree>` |
| `대화/` | 대화 추출 | domain tree 직속 |
| `images/` | 이미지 통합 | flat (예외) |

### Tree 구조 원칙

각 top-level 아래는 **공통 domain tree**를 공유한다:
```
neuron/이론/compiler/ai-compiler/mlir/<topic>.md
neuron/지식/compiler/ai-compiler/mlir/<topic>.md
neuron/실험/<project>/compiler/ai-compiler/mlir/<topic>.md
```

→ "MLIR 지식 보여줘" 같은 요청은 **모든 top-level의 같은 leaf**를 가로로 모은다 (`search-knowledge` 워크플로우).

### Greedy + 주기적 재구축

- 새 지식은 작성 시점 best-fit으로 (greedy) — `knowledge-curator` 책임
- 누적된 드리프트는 사용자가 주기적으로 호출하는 `knowledge-reorganizer`가 일괄 보정
- 카테고리 명명: 영문 lowercase, `-` 구분, 단수형

상세는 `agent/neuron-agent.md`.

## Git 원격 저장소 정책

- 원격 push는 `https://github.com/sedie1234/MyNeuron`으로만 허용.
- **`neuron/` 하위 지식 문서는 절대 원격 push 금지.** 로컬 git만 사용.
- **`books/` 하위 mdbook도 원격 push 금지** (neuron/ 파생물).
- push 대상: `agent/`, `tools/`, `CLAUDE.md`, `.gitignore` 등 인프라.

## mdbook 생성 정책

- 출력 위치는 반드시 `books/<category>/<book>/` 구조.
- 카테고리는 neuron/ tree 또는 사용자 지정.
- 표준 템플릿: `temp/polyhedral_mdbook/` (`book.toml` + `theme/`만 복사, `src/` 챕터 베끼지 않음).

## 빠른 참조

- 지식: `neuron/<top>/<domain-tree>/(<project>/)?<topic>/`
- 임시: `temp/`
- mdbook: `books/<category>/<book>/`
- 도구: `tools/`
- **Agent 설정 (단일 source of truth)**: `agent/`
  - 공유 원칙: `agent/neuron-agent.md`
  - 서브에이전트: `agent/agents/`
  - 스킬: `agent/skills/<name>/SKILL.md`
  - 워크플로우: `agent/workflows/<name>.md`
  - 다른 프로젝트용 템플릿: `agent/templates/`
- `.claude/`: Claude Code 운영 디렉토리 (`.claude/agents`, `.claude/skills`는 `agent/`로의 symlink — **새 설정 금지**)
- 지시서: `order/`
- TODO: `todo.md`
