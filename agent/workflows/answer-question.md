---
name: answer-question
type: workflow
description: 질문 응답의 step-by-step 절차 — clarify → search → 답변 구성 → 출력
---

# Workflow — answer-question

활성화 조건은 `agent/skills/answer-question/SKILL.md` 참조.

---

## Step 1: 질문 이해

질문에서 식별:
- **주제**: 무엇에 관한 질문?
- **범위**: 정의/개념/예시/응용/비교?
- **깊이 수준**: 1줄 vs 개요 vs 상세 vs 수학적 상세?
- **컨텍스트**: 이전 대화/문서/PDF/특정 페이지?

모호하면 `clarify-question` 스킬 적용 (2-3가지 해석 짚고 기본으로 진행).

---

## Step 2: 사전 검색 (필수)

`search-knowledge` 스킬/워크플로우로 neuron/ 탐색:

```
주제어 → tree 가로 검색 → top-level별 결과
```

추출:
- 직접 매칭 문서 (frontmatter summary + 핵심 본문)
- 1-hop related 문서

검색 비용이 크면 `knowledge-searcher` 에이전트에 위임 가능.

---

## Step 3: 답변 구성

### 3.1 깊이 결정

| 질문 유형 | 깊이 |
|---------|------|
| "X가 뭐야?" | 정의 + 핵심 예시 (간결) |
| "X에 대해 설명" | 배경 + 정의 + 예시 + 응용 (중간) |
| "X 자세히 / 깊이" | 수학적 정의 + 워크스루 + 다이어그램 (상세) |
| "X와 Y 차이" | 표 비교 + 각 측면 설명 |

### 3.2 본문 작성

기존 지식 인용:
```markdown
[[neuron/이론/compiler/ai-compiler/mlir/overview.md]]에 따르면,
MLIR은 ...
```

추론 보완 (명시 필수):
```markdown
**이 부분은 기존 지식에 없는 내용입니다.** [추론 결과]...
```

### 3.3 시각 자료

자주 사용:
- **표**: 비교, 분류
- **Mermaid**: 흐름, 관계 (관계가 3+ 노드일 때 적극)
- **ASCII art**: 격자, 좌표
- **수식**: LaTeX 또는 평문
- **코드 블록**: 예시

### 3.4 참조 표기

답변 말미에 참조한 neuron/ 문서 경로 나열:

```markdown
## 참고
- [[neuron/이론/.../overview.md]]
- [[neuron/지식/.../practical.md]]
```

---

## Step 4: 출력

- 마크다운 (GitHub-flavored)
- frontmatter 등 메타데이터 포함 금지 (답변은 채팅 응답이지 지식 문서가 아님)
- 길이는 질문 유형에 맞게 (1줄 질문에 5쪽 답변 금지)

---

## 다른 스킬·에이전트 호출

| 시점 | 호출 대상 |
|------|---------|
| 질문 모호 | `clarify-question` 스킬 |
| 광범위 검색 | `search-knowledge` 또는 `knowledge-searcher` 에이전트 |
| 답변 후 "저장해줘" | `transfer-knowledge` 스킬 (위임 권장) |

---

## 절대 하지 말 것

- ❌ neuron/ 검색 없이 답변 시작
- ❌ 추론을 기존 지식인 양 단정
- ❌ neuron/ 문서 수정 (별개 스킬)
- ❌ 답변에 frontmatter (`---` YAML) 포함
- ❌ 명확한 질문에 clarify 과잉 적용
- ❌ 답변 길이가 질문 깊이와 동떨어짐
