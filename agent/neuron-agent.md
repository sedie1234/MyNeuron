# MyNeuron Agent — 공유 원칙 (Shared Principles)

이 문서는 MyNeuron 프로젝트의 모든 에이전트(메인 + 서브에이전트)가 공유하는 **핵심 원칙**과 **표준**을 정의한다. 역할별 구체 동작은 `agent/agents/<role>.md`에 정의됨.

---

## 핵심 원칙

- 모든 지식 문서는 `neuron/` 하위에 저장한다.
- 모든 문서는 YAML frontmatter를 포함한다.
- 기본 언어는 한국어, 기술 용어는 영어로 표기한다.
- 영어 외의 원문 표기가 더 적절한 경우 사용자에게 제안하고, 승인 시 원문으로 표기할 수 있다.
- frontmatter의 필드명과 태그는 영어로 통일한다.
- 지식 간 연결은 Obsidian `[[위키링크]]`를 적극 활용한다.
- **애매한 판단을 자의적으로 내리지 않는다.** 판단이 불확실하거나 여러 해석이 가능한 경우, 반드시 사용자에게 질문하여 확인한 후 진행한다. 추측으로 행동하지 않는다.
- **지식 문서는 상세하게 작성한다.** 나중에 읽었을 때 배경과 근거까지 이해할 수 있어야 한다.
  - 수치, 테이블, 수식을 적극 활용하여 정량적으로 표현한다.
  - 개념의 관계나 흐름이 복잡할 경우 Mermaid 다이어그램을 삽입한다.
  - 시각적 설명이 이해에 도움이 되는 경우 이미지를 적극 생성·활용한다.
  - 배경(왜 이 지식이 필요한가)과 근거(어떻게 도출되었는가)를 반드시 포함한다.

---

## Frontmatter 명세

### 공통 필드 (모든 문서)

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

- **draft**: 초기 기록, 검증 전. 새 문서의 기본값.
- **confirmed**: 검증 완료, 신뢰할 수 있는 지식.
- **deprecated**: 더 이상 유효하지 않음 (문서는 보존).
- **conflicted**: 다른 지식과 모순, 사용자 판단 필요.

### type별 추가 필드

**experiment (실험)**:
```yaml
objective: "실험 목적"
hypothesis: "가설"
result: success | failure | partial | ongoing
lessons: "핵심 교훈 한 줄 요약"
transferred_to: ["[[전이된 지식문서]]"]
```
> result는 실험의 성패, status는 문서/지식의 검증 상태. 실패한 실험도 confirmed 지식이 될 수 있다.

**project (프로젝트)**:
```yaml
project_name: "프로젝트명"
ip_cleared: true | false
phase: planning | in-progress | completed | archived
```

**conversation (대화)**:
```yaml
topic: "대화 주제"
conversation_date: YYYY-MM-DD
source: "Claude Code" | "동료" | "세미나" | etc.
```

**theory (이론)**:
```yaml
domain: "분야"
references: ["출처"]
confidence: high | medium | low
```

**knowledge (지식)**:
```yaml
origin: ["[[출처 문서]]"]
domain: "분야"
```

---

## 지식 연결 (Link) 전략

- 새 문서 생성 시, 기존 문서 중 관련 문서를 탐색하여 **양방향 링크**를 삽입한다.
  - 새 문서의 `related` 필드에 관련 문서 링크를 추가.
  - 기존 관련 문서의 `related` 필드에도 새 문서 링크를 추가.
- 본문에서 다른 문서가 다루는 개념이 언급되면 `[[위키링크]]`를 건다.
- 지식 전이 시 `origin`/`transferred_to` 필드로 출처 관계를 명시한다.
- `tags`는 카테고리 횡단 검색용. 같은 주제를 다루는 문서는 동일 태그를 부여한다.

---

## 디렉토리 구조

```
neuron/
├── 이론/          # 이론 지식 (영구 보존)
├── 실험/          # 실험 경험 (성공/실패 기록)
├── 프로젝트/      # 프로젝트 기반 지식
├── 대화/          # 대화에서 얻은 지식
├── 지식/          # 전이된 확정 지식
└── images/        # 이미지 통합 저장
```

- 각 카테고리 하위에 주제별 서브 카테고리를 생성할 수 있다.
- 카테고리가 어지러워지면 `knowledge-organizer` 서브에이전트로 정리한다.

---

## 이미지 관리

- 모든 이미지는 `neuron/images/`에 저장한다.
- 파일명 규칙: `{문서키워드}_{설명}_{번호}.png` (예: `transformer_attention_mechanism_01.png`)
- 문서에서 참조: `![[이미지파일명]]` Obsidian 형식 사용.
- 이미지가 지식 이해에 도움이 된다면 적극 활용한다.
- 이미지 생성 도구는 `tools/`에 위치한다.

---

## 버전 관리

- 지식 추가/수정/정리 후 적절한 단위로 git commit한다.
- commit 메시지는 어떤 지식이 추가/수정/정리되었는지 알 수 있도록 작성한다.
- `neuron/` 하위 지식 문서는 **절대 원격 push 금지**. agent 설정/도구/CLAUDE.md만 push 허용.
- 원격 push는 `https://github.com/sedie1234/MyNeuron`으로만 허용.

---

## 역할 분담 (서브에이전트)

이전 버전의 6가지 역할(지식 축적, temp 처리, 회상, 확장 질문, 정리, 대화에서 생성)은 **서브에이전트로 분리**되어 `agent/agents/`에 정의됨:

| 역할 | 서브에이전트 |
|------|------------|
| 지식 축적/저장 (이전 #1, #2, #6) | `knowledge-curator` |
| 기존 지식 검색 | `knowledge-searcher` |
| 질문 답변 / 회상 / 확장 (이전 #3, #4) | `knowledge-qa` |
| 문서 정리 (이전 #5) | `knowledge-organizer` |
| mdbook 생성 | `mdbook-builder` |
| 공부 리스트 관리 | `study-tracker` |

각 서브에이전트는 이 문서의 공유 원칙을 **반드시 준수**한다.

라우팅 정책은 `CLAUDE.md`에 정의됨.

---

## 관련 문서

- `agent/README.md` — agent/ 디렉토리 구조 및 관리 가이드
- `agent/agents/<role>.md` — 각 서브에이전트 정의
- `agent/skills/<skill>/SKILL.md` — 인라인 동작 스킬
- `agent/templates/` — 다른 프로젝트용 CLAUDE.md 템플릿
