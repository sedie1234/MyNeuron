---
name: organize-knowledge
description: neuron/ 트리 안에서 부분적·정기적 정리. 중복/충돌/끊긴 링크/고아/카테고리 불일치/frontmatter 비표준 점검 후 사용자 승인 받아 정리. 트리 전체 재구축은 reorganize-tree로 분리됨.
workflow: agent/workflows/organize-knowledge.md
---

# organize-knowledge — 부분 정리 스킬

`neuron/` 트리의 **일부**(특정 leaf, 특정 domain subtree)에 대한 진단·정리. 트리 전체를 다시 짜는 것은 `reorganize-tree`의 영역.

## 활성화 조건

- "지식 정리해줘"
- "중복 찾아줘", "끊긴 링크 점검"
- "고아 문서 있어?"
- "카테고리 X 정리"
- 신규 문서 N개 추가 후 정기 점검

## 비활성화 조건

- 전체 tree 재구축 (→ `reorganize-tree`)
- 신규 지식 저장 (→ `transfer-knowledge`)
- 답변 (→ `answer-question`)

## 진단 항목

1. 중복/유사 문서
2. 충돌 (`status: conflicted`)
3. 끊긴 wikilink
4. 고아 문서 (in/out 둘 다 없음)
5. 카테고리 불일치 (`domain` 필드 ↔ 디렉토리 경로)
6. frontmatter 비표준
7. stale 문서 (6개월+)
8. 양방향 링크 미일치
9. 빈 디렉토리
10. 오래 방치된 `draft`

## 핵심 철학

- **진단 먼저, 실행은 나중** — 자동 변경 절대 금지
- **보수적** — 삭제 매우 신중, 병합 시 정보 손실 없게
- **카테고리 존중** — 임의 새 카테고리 생성 금지
- **부분적** — 전체 tree 재구축은 reorganize-tree로 분리

## 범위 지정

호출 시 범위를 좁힌다:
- 특정 leaf: `neuron/이론/compiler/ai-compiler/mlir/`
- 특정 top-level: `neuron/지식/`
- 특정 domain subtree: `neuron/*/compiler/`
- 전체 (작은 프로젝트일 때만)

## 절차

`agent/workflows/organize-knowledge.md`.

## 절대 하지 말 것

- ❌ 사용자 승인 없이 삭제·병합·이동
- ❌ 정보 손실 동반 병합
- ❌ frontmatter 정보 무단 제거
- ❌ neuron-agent.md 카테고리 규칙 위반
- ❌ 트리 전체 재구축 (그건 reorganize-tree)
- ❌ 한 번에 너무 많은 변경 제안 (사용자 검토 불가)
- ❌ 임의 commit/push
