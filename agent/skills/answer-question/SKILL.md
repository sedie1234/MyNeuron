---
name: answer-question
description: 학습/탐구 질문에 neuron/ 기존 지식 + 새 추론을 결합하여 답변. search-knowledge로 사전 검색 후 답변 구성. 답변 저장은 별개(transfer-knowledge).
workflow: agent/workflows/answer-question.md
---

# answer-question — 질문 응답 스킬

학습/탐구 질문에 대해 **기존 지식(neuron/) + 새 추론**을 결합해 답변. 답변 자체를 저장하는 것은 별개 스킬.

## 활성화 조건

- "X에 대해 설명해줘"
- "X와 Y의 차이는?"
- "왜 X인가?", "어떻게 X인가?"
- 기술/이론/개념 일반 질문
- 논문/PDF 페이지 의미 질문

## 비활성화 조건

- 단순 사실 (파일 존재 여부 등)
- 검색만 원함 (→ `search-knowledge`)
- 저장 요청 (→ `transfer-knowledge`)
- 실행 요청 (commit, mv 등)

## 역할

답변 생성. 다음을 책임진다:

1. 질문 모호 시 `clarify-question` 스킬 활용
2. **사전 검색 필수** — `search-knowledge`로 neuron/ 탐색
3. 답변 구성: 기존 지식 인용 + 부족분 추론 보완
4. **새 추론은 명시** — "기존 지식에는 없는 내용" 표기
5. 깊이 조절 (질문 유형 기반)
6. 시각 자료 (표/Mermaid/ASCII art/수식) 적극

## 시스템 원칙

- 추측을 사실처럼 단정 금지
- 답변에 frontmatter 등 메타데이터 포함 금지 (지식 문서 형식 ≠ 답변 형식)
- neuron/ 수정·저장 안 함 (별개 스킬)

## 절차

`agent/workflows/answer-question.md`.

## 절대 하지 말 것

- ❌ neuron/ 검색 생략하고 바로 답변
- ❌ 추론을 사실처럼 단정 (반드시 "기존 지식에 없음" 명시)
- ❌ neuron/ 문서 수정
- ❌ clarify-question 과잉 적용 (명확한 질문에)
