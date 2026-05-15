---
name: search-knowledge
description: neuron/ 하위에서 기존 지식을 검색. tree 기반 구조를 활용해 모든 top-level(이론/지식/실험/프로젝트/대화)의 동일 leaf 경로를 가로로 모아 반환하는 read-only 스킬.
workflow: agent/workflows/search-knowledge.md
---

# search-knowledge — 기존 지식 검색 스킬

`neuron/` 트리 구조를 활용해 주제별 지식을 **가로 단면(cross-section)** 으로 모은다. 답변 생성이 아니라 정보 조회.

## 활성화 조건

- "neuron에 X 있어?", "X 찾아줘", "이전에 다룬 X"
- 답변 에이전트(`knowledge-qa` 등)의 사전 검색 단계
- mdbook 생성의 콘텐츠 수집 단계

## 비활성화 조건

- 답변 생성 (→ `answer-question`)
- 새 지식 저장 (→ `transfer-knowledge`)

## 역할 (READ-ONLY)

### 할 수 있는 것

- 주제어로 모든 top-level에서 동일 leaf 후보 탐색
- 디렉토리 tree 탐색 (Glob)
- 본문/태그/title grep
- frontmatter 추출 + 1-3줄 요약
- related 그래프 확장

### 할 수 없는 것

- ❌ 파일 작성/수정
- ❌ 답변 생성 (다른 스킬 영역)
- ❌ 결과를 사실처럼 단정 (검색일 뿐)

## Tree-aware 검색

핵심: 같은 주제는 모든 top-level의 같은 leaf에 있을 수 있다.

```
neuron/이론/<domain-tree>/<topic>/
neuron/지식/<domain-tree>/<topic>/
neuron/실험/<project>/<domain-tree>/<topic>/
neuron/프로젝트/<project>/<domain-tree>/<topic>/
neuron/대화/<domain-tree>/<topic>/
```

가로 검색 결과를 top-level별로 그룹화하여 반환.

## 절차

`agent/workflows/search-knowledge.md`.

## 절대 하지 말 것

- ❌ 검색 결과로 "답변" 생성
- ❌ 파일 수정
- ❌ 결과 없을 때 추측으로 만들어내기
- ❌ 모든 결과 통째 dump (상위 N개 + "더 많음")
