---
name: transfer-knowledge
description: 새 지식을 neuron/ 하위 적절한 카테고리 트리에 저장. temp/ 초안 또는 대화 내용 전이, 외부 자료 정리 시 사용. tree 경로(<top-level>/<domain>/.../<topic>/) 결정, 흡수/공존/신규 판단, 양방향 링크 갱신, temp/ 원본 처리.
workflow: agent/workflows/transfer-knowledge.md
---

# transfer-knowledge — 지식 전이/저장 스킬

새 지식을 `neuron/` 트리에 정확하게 카테고리화·저장. greedy 분류 원칙(작성 시점 best-fit) + 누적 드리프트는 `reorganize-tree`로 보정.

## 활성화 조건

- "지식 전이", "이거 저장해줘", "기억 전이", "neuron에 추가"
- `temp/` 초안을 정식 지식으로 승격
- 대화 내용을 지식으로 추출
- 외부 자료(논문 노트 등)를 neuron/에 정리

## 비활성화 조건

- 단순 질문 응답 (→ `answer-question`)
- 기존 문서 검색 (→ `search-knowledge`)
- 정기 정리/병합 (→ `organize-knowledge`)
- 전체 재구축 (→ `reorganize-tree`)

## 역할

지식 전이의 **저장자**. 다음을 책임진다:

1. **type 결정**: theory/knowledge/experiment/project/conversation
2. **tree 경로 결정**: `neuron/<top-level>/<domain-tree>/<topic>/` (greedy)
3. **흡수/공존/신규 판단**: 기존 노드 안의 문서들과 어떻게 관계 맺을지
4. **frontmatter 작성**: 공유 원칙의 명세 따름
5. **양방향 링크**: `related` + `origin`/`transferred_to`
6. **temp/ 원본 처리**: 전이 후 disposition (status 갱신 또는 사용자 확인)
7. **commit** (push 절대 금지 — neuron/ 정책)

## Tree 경로 정책

공유 원칙(`neuron-agent.md`) 참조:
- `이론/`, `지식/`: `<top>/<domain-tree>/<topic>/`
- `실험/`, `프로젝트/`: `<top>/<project>/<domain-tree>/<topic>/`
- `대화/`: `<top>/<domain-tree>/<topic>/` (project 키 선택)

## 절차

`agent/workflows/transfer-knowledge.md`.

## 절대 하지 말 것

- ❌ `neuron/` 외부에 지식 문서 저장
- ❌ flat 파일로 저장 (반드시 tree leaf 디렉토리 아래)
- ❌ frontmatter 누락
- ❌ 모호한 카테고리를 자의로 결정 (사용자 확인 필수)
- ❌ 양방향 링크 한쪽만 갱신
- ❌ neuron/ remote push
- ❌ temp/ 원본을 사용자 확인 없이 삭제
