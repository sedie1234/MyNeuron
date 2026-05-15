---
name: transfer-knowledge
type: workflow
description: 지식 전이의 step-by-step 절차 — type/tree path 결정, 흡수/공존/신규 판단, frontmatter/링크 갱신, temp 처리, commit
---

# Workflow — transfer-knowledge

활성화 조건은 `agent/skills/transfer-knowledge/SKILL.md` 참조.

---

## Step 1: 입력 식별

전이할 내용의 출처를 식별:

| 출처 | 형태 |
|------|------|
| `temp/<file>.md` | 초안 파일 (frontmatter 가능) |
| 대화 컨텍스트 | 사용자와의 직전 대화 내용 |
| 외부 자료 (PDF/논문) | 사용자가 노트로 전달 |
| 다른 프로젝트 | NAS 외부 워크스페이스에서 옮겨온 것 |

각 입력에서 추출:
- **주제어**: 문서가 다루는 핵심 개념 (예: MLIR, polyhedral)
- **type 후보**: theory / knowledge / experiment / project / conversation
- **project 키**: 실험/프로젝트의 경우 어느 프로젝트인지

---

## Step 2: type 결정

| 입력 특성 | type |
|----------|------|
| 일반화된 이론·원리·정의 | `theory` (→ `이론/`) |
| 검증된 결론·정리·전이 산출물 | `knowledge` (→ `지식/`) |
| 실험 기록 (성공/실패) | `experiment` (→ `실험/`) |
| 프로젝트 컨텍스트 종속 | `project` (→ `프로젝트/`) |
| 대화 추출물 | `conversation` (→ `대화/`) |

판단이 갈리면 사용자 확인. 일반적 분기:
- "논문 요약 + 일반 원리" → `theory`
- "논문 정리 후 본인 정리·검증 완료" → `knowledge`
- "특정 프로젝트에서 시도한 결과" → `experiment` 또는 `project`

---

## Step 3: domain tree 경로 결정 (greedy)

### 3.1 candidate path 후보 만들기

주제어를 기반으로 `neuron-agent.md` 카테고리 명명 규칙 (영문 소문자, `-` 구분, 단수형)에 따라 후보 경로 작성:

```
candidate 1: neuron/<top>/compiler/mlir/
candidate 2: neuron/<top>/compiler/ai-compiler/mlir/
candidate 3: neuron/<top>/compiler/ir/mlir/
```

### 3.2 기존 트리 정찰

```bash
# 동일 top-level의 기존 트리 확인
find neuron/<top>/ -type d | sort

# 가로(모든 top-level)에서 같은 leaf 후보 확인
find neuron/ -type d -name "<leaf-name>"
```

### 3.3 결정 규칙 (greedy)

- **이미 같은 leaf가 다른 top-level에 존재** → 동일 경로 채택 (가로 일관성)
- **하나도 없음** → 가장 자연스러운 후보로 신규 leaf 생성. 깊이는 의미가 분기할 때만 늘림.
- **두 candidate가 비등** → 사용자에게 단답형 질문 (선택지 2개 제시 후 즉시 진행)

> greedy 결정은 완벽함을 목표로 하지 않는다. 누적된 드리프트는 `reorganize-tree`로 보정.

### 3.4 실험/프로젝트의 경우

```
neuron/실험/<project>/<domain-tree>/<topic>/
neuron/프로젝트/<project>/<domain-tree>/<topic>/
```

project 키가 없으면 사용자에게 확인.

---

## Step 4: 흡수 / 공존 / 신규 판단

결정된 leaf 디렉토리 안의 기존 파일을 조사:

```bash
ls neuron/<top>/<...>/<leaf>/
```

각 기존 파일의 frontmatter + summary 비교:

| 상황 | 행동 |
|------|------|
| **흡수**: 기존 파일이 새 내용 상위집합 | 기존 파일 update, 새 내용 섹션으로 추가, frontmatter `updated` 갱신 |
| **확장**: 기존 파일이 부분집합 | 기존 파일을 새 내용으로 보강 (정보 손실 없게) |
| **공존**: 다루는 측면이 다름 | 신규 파일로 저장, 양쪽에 `related` 링크 |
| **신규**: 기존 무관 | 새 파일 작성 |
| **충돌**: 같은 사실에 다른 결론 | `status: conflicted`로 양쪽 표시, 사용자 판단 요청 |

판단이 갈리면 사용자에게 짧게 확인:
```
"기존 <path>/<file>.md"가 비슷한 주제입니다. 다음 중 어떻게 처리할까요?
- A. 흡수 (기존 파일에 새 내용 통합)
- B. 공존 (새 파일로 저장, related 링크)
- C. 대체 (기존 파일을 deprecated, 새 파일로)
```

---

## Step 5: 작성

### 5.1 파일명 규칙

영문 lowercase-hyphen. 예: `three-principles-and-limits.md`, `overview.md`, `pass-pattern-practical.md`.

(기존 한국어/underscore 파일은 reorganize-tree에서 일괄 처리 — 신규 작성에만 영문 강제.)

### 5.2 Frontmatter

```yaml
---
title: "문서 제목"
type: theory | knowledge | experiment | project | conversation
status: draft | confirmed | deprecated | conflicted
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [영어 태그]
related: ["[[관련문서1]]", "[[관련문서2]]"]
summary: "한 줄 요약"
# type별 추가
domain: "compiler/ai-compiler/mlir"   # tree 경로 그대로
# theory: references, confidence
# knowledge: origin (출처 문서 wikilink)
# experiment: objective, hypothesis, result, lessons, transferred_to
# project: project_name, ip_cleared, phase
# conversation: topic, conversation_date, source
---
```

`domain` 필드는 tree 경로와 일치시킨다 — 이동/재구축 시 일관성 검증의 anchor.

### 5.3 본문

공유 원칙: 상세 작성 (배경·근거·수치·표·다이어그램).

- 정의·예시·수식·코드 블록
- Mermaid 다이어그램 (관계가 복잡할 때)
- 다른 문서 언급 시 `[[위키링크]]`

---

## Step 6: 양방향 링크 갱신

### 6.1 새 문서 → 관련 문서

`related` 필드에 wikilink 추가.

### 6.2 관련 문서 → 새 문서

각 관련 문서의 `related` 필드에 새 문서 wikilink 추가 (Edit).

### 6.3 origin / transferred_to

- 새 문서가 temp/ 또는 외부 자료 기반이면:
  - 새 문서 frontmatter `origin: ["[[temp/...]]"]` 또는 `references: [...]`
- temp/ 원본이 markdown이면:
  - 원본 frontmatter `transferred_to: ["[[새문서]]"]` + `status: transferred` (또는 사용자 확인 후 삭제)

---

## Step 7: temp/ 원본 처리

전이 완료 후 temp/ 원본의 disposition:

| 옵션 | 적용 |
|------|------|
| `status: transferred` 마크 + 보관 | 기본. 원문(논문 노트 등) 보존 가치 있을 때 |
| 별도 archive 디렉토리로 이동 | temp/archive/ 등 (수동) |
| 삭제 | **사용자 명시 동의 시에만** |

기본 동작: 마크만 하고 보관. 사용자에게 disposition 짧게 보고:
```
temp/<file>.md → status: transferred 마크 (보관).
삭제 원하시면 알려주세요.
```

---

## Step 8: 검증 & commit

### 8.1 검증

- 파일이 결정된 tree leaf에 있는지
- frontmatter 모든 필수 필드 채워졌는지
- `domain` 필드와 디렉토리 경로 일치하는지
- 양방향 링크 일치하는지 (A→B 있으면 B→A도 있는지)

### 8.2 commit

```bash
git add neuron/<path>/<new-file>.md [관련 갱신 파일들]
git commit -m "knowledge: add <topic> under <path>"
```

**neuron/ 원격 push 절대 금지** — 공유 원칙.

---

## Step 9: 보고

```
✓ 전이 완료

신규: neuron/<top>/<domain-tree>/<topic>/<file>.md (type=<type>, status=<status>)
관계: 기존 N개 문서와 양방향 링크
출처: temp/<original>.md (status: transferred)
commit: <hash> (local only, push 안 함)
```

---

## 절대 하지 말 것

- ❌ 카테고리 결정을 자의로 (모호 → 사용자 확인)
- ❌ tree leaf 없이 top-level에 flat 저장
- ❌ frontmatter `domain`과 실제 경로 불일치
- ❌ 한쪽 링크만 갱신
- ❌ temp/ 원본 무단 삭제
- ❌ neuron/ remote push
- ❌ 흡수/공존/대체 판단 무단 결정 (충돌 시 사용자 확인)
