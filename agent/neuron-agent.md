# MyNeuron Agent — 공유 원칙 (Shared Principles)

이 문서는 MyNeuron 프로젝트의 모든 에이전트(메인 + 서브)가 공유하는 **핵심 원칙**과 **표준**을 정의한다. 역할별 구체 동작은 `agent/agents/<role>.md`에, 절차는 `agent/workflows/<name>.md`에 분리되어 있다.

---

## 핵심 원칙

- 모든 지식 문서는 `neuron/` 하위에 저장한다.
- 모든 문서는 YAML frontmatter를 포함한다.
- 기본 언어는 한국어, 기술 용어는 영어로 표기한다.
- frontmatter의 필드명과 태그는 영어로 통일한다.
- 지식 간 연결은 Obsidian `[[위키링크]]`를 적극 활용한다.
- **애매한 판단을 자의적으로 내리지 않는다.** 판단이 불확실하면 사용자에게 질문한 후 진행한다.
- **지식 문서는 상세하게 작성한다.** 배경·근거·수치·표·다이어그램을 포함한다.

---

## 설정 구조 — 단일 source of truth

```
agent/
├── neuron-agent.md           # 이 문서 (공유 원칙)
├── README.md                  # 디렉토리 가이드
├── agents/<role>.md           # 서브에이전트 정의 (role + tools + skill 포인터, 얇음)
├── skills/<name>/SKILL.md     # 스킬 정의 (activation, role, workflow 포인터, 얇음)
├── workflows/<name>.md        # 절차 정의 (step-by-step, 두꺼움)
└── templates/                 # 다른 프로젝트용 CLAUDE.md 템플릿
```

**대전제**:
- `.claude/`에는 **새 설정 파일을 만들지 않는다**. 모든 설정은 `agent/` 아래에 둔다.
- `.claude/agents`, `.claude/skills`는 `agent/agents`, `agent/skills`로 향하는 symlink일 뿐이다 (Claude Code 자동 로드용).
- 스킬과 워크플로우는 **항상 분리**한다. SKILL.md는 "언제·왜", workflow는 "어떻게".

---

## Frontmatter 명세

### 공통 필드 (모든 지식 문서)

```yaml
---
title: "문서 제목"
type: theory | experiment | project | conversation | knowledge
status: draft | confirmed | deprecated | conflicted
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [영어 태그]
related: ["[[관련문서1]]", "[[관련문서2]]"]
summary: "한 줄 요약"
---
```

### status 정의

- **draft**: 초기 기록, 검증 전.
- **confirmed**: 검증 완료, 신뢰할 수 있는 지식.
- **deprecated**: 더 이상 유효하지 않음 (보존).
- **conflicted**: 다른 지식과 모순, 사용자 판단 필요.

### type별 추가 필드

**theory**: `domain`, `references`, `confidence`
**knowledge**: `origin` (출처 문서), `domain`
**experiment**: `objective`, `hypothesis`, `result`, `lessons`, `transferred_to`
**project**: `project_name`, `ip_cleared`, `phase`
**conversation**: `topic`, `conversation_date`, `source`

전체 명세는 `agent/workflows/transfer-knowledge.md` 참조.

---

## 디렉토리 구조 — Tree 기반 카테고리

`neuron/` 하위는 **top-level(관점) × domain tree(주제)**의 2축 구조다.

### Top-level (관점)

| Top-level | 의미 | 단위 |
|----------|------|------|
| `이론/` | 이론·원리 지식 (영구 보존) | domain tree 직속 |
| `지식/` | 확정·전이된 지식 | domain tree 직속 |
| `실험/` | 실험 기록 (성공/실패) | `<project>/<domain tree>` |
| `프로젝트/` | 프로젝트 기반 지식 | `<project>/<domain tree>` |
| `대화/` | 대화에서 얻은 지식 | domain tree 직속 (project 키 선택) |
| `images/` | 이미지 통합 저장 (예외) | flat |

### Domain Tree

각 top-level 아래에는 **공통 domain tree**를 둔다. 트리 노드는 디렉토리, leaf에 .md 파일이 들어간다.

```
neuron/
├── 이론/
│   └── compiler/
│       └── ai-compiler/
│           └── mlir/
│               ├── overview.md
│               ├── three-principles.md
│               └── dialect-system.md
├── 지식/
│   └── compiler/
│       └── ai-compiler/
│           └── mlir/
│               ├── practical-guide.md
│               └── pass-pattern.md
├── 실험/
│   └── npu-compiler/
│       └── compiler/
│           └── ai-compiler/
│               └── mlir/
│                   └── lowering-experiment.md
└── 프로젝트/
    └── npu-compiler/
        └── compiler/
            └── ai-compiler/
                └── mlir/
                    └── arch-decision.md
```

### Tree 노드 작명

- 영문 소문자, 단어 구분은 `-` (예: `ai-compiler`, `computer-architecture`)
- 단수형 우선 (예: `compiler`, `accelerator`)
- 노드 깊이는 의미가 분기될 때만 늘림. 깊이를 위한 깊이는 금지.
- **카테고리는 greedy로 결정**된다 (작성 시점 best-fit). 누적된 드리프트는 `reorganize-tree` 워크플로우로 주기적 보정.

### 가로 검색 (cross-section)

"MLIR에 대한 지식 보여줘" 같은 요청은 **모든 top-level에서 같은 leaf 경로**를 모은다:

```
neuron/*/compiler/ai-compiler/mlir/**/*.md
neuron/*/compiler/mlir/**/*.md      # 깊이 다른 변형도 후보
```

상세 절차는 `agent/workflows/search-knowledge.md`.

---

## 지식 연결 (Link) 전략

- 새 문서 생성 시 관련 기존 문서를 탐색해 **양방향 링크**를 삽입한다.
  - 새 문서의 `related` 필드에 기존 문서 추가
  - 기존 문서의 `related` 필드에도 새 문서 추가
- 본문에서 다른 문서가 다루는 개념이 언급되면 `[[위키링크]]`.
- 지식 전이 시 `origin` / `transferred_to`로 출처 관계 명시.
- `tags`는 카테고리 횡단 검색 보조용. 같은 주제 문서는 동일 태그 부여.

---

## 카테고리 운영 — Greedy + 주기적 재구축

새 지식은 작성 시점에 가장 적합한 노드에 **greedy**로 넣는다 (완벽한 위치를 고민하지 않는다 — 트리는 자라면서 어긋난다).

누적된 어긋남은 사용자가 `reorganize-tree`를 호출할 때 한 번에 보정:
1. `neuron/` 전체 스캔 (모든 top-level × 전체 트리)
2. 콘텐츠 기반으로 새 트리 도출 (현 트리에 얽매이지 않음)
3. 사용자 승인 후 일괄 재분류 (파일 이동 + 모든 wikilink 갱신)

상세 절차는 `agent/workflows/reorganize-tree.md`.

> 트리는 살아 있는 분류 체계다. 한 번 정한 카테고리가 영원할 필요는 없다 — 다만 같은 시점에는 일관되어야 한다.

---

## 이미지 관리

- 모든 이미지는 `neuron/images/`에 저장한다.
- 파일명: `{문서키워드}_{설명}_{번호}.png` (예: `transformer_attention_01.png`)
- 참조: `![[이미지파일명]]` Obsidian 형식.
- 이미지 생성 도구는 `tools/`.

---

## 버전 관리

- 지식 추가/수정 후 적절한 단위로 git commit.
- commit 메시지는 어떤 지식이 추가/수정/정리되었는지 명시.
- `neuron/` 하위 지식 문서는 **절대 원격 push 금지**. `agent/`, `tools/`, `CLAUDE.md` 등 인프라만 push.
- 원격: `https://github.com/sedie1234/MyNeuron`만 허용.

---

## 서브에이전트와 스킬

| 역할 | 서브에이전트 | 주 스킬 |
|------|-------------|--------|
| 새 지식 저장/전이 | `knowledge-curator` | `transfer-knowledge` |
| 기존 지식 검색 | `knowledge-searcher` | `search-knowledge` |
| 정기 정리 | `knowledge-organizer` | `organize-knowledge` |
| 트리 재구축 | `knowledge-reorganizer` | `reorganize-tree` |
| 질문 답변 | `knowledge-qa` | `answer-question` + `clarify-question` |
| mdbook 생성 | `mdbook-builder` | `create-knowledge-mdbook` |
| 공부 리스트 | `study-tracker` | `manage-study-list` |

각 에이전트는 이 문서의 공유 원칙을 **반드시 준수**한다. 라우팅은 프로젝트 루트 `CLAUDE.md`.

---

## 관련 문서

- `agent/README.md` — 디렉토리 가이드
- `agent/agents/<role>.md` — 서브에이전트 정의
- `agent/skills/<name>/SKILL.md` — 스킬 정의 (활성화 조건)
- `agent/workflows/<name>.md` — 워크플로우 (절차)
- `agent/templates/` — 다른 프로젝트용 CLAUDE.md 템플릿
