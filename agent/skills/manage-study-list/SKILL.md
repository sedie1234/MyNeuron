---
name: manage-study-list
description: todo.md 기반 학습/연구 todo 추적·관리. 추가/조회/갱신/정리, neuron/ 분석 기반 학습 제안.
workflow: agent/workflows/manage-study-list.md
---

# manage-study-list — 공부 리스트 관리 스킬

프로젝트 루트의 `todo.md`를 학습·연구 todo의 단일 source로 관리.

## 활성화 조건

- "todo 추가", "공부할 거 추가"
- "다음 공부 주제 추천"
- "todo 보여줘"
- "X 항목 완료/진행중으로"
- "todo 정리"

## 비활성화 조건

- 지식 저장 (→ `transfer-knowledge`)
- 답변 (→ `answer-question`)

## 역할

`todo.md`의:
- 추가
- 조회 (전체/카테고리별/검색)
- 상태 갱신 (대기/진행/완료)
- 정리 (재배치, 아카이브, 중복 제거)
- `neuron/` 분석 기반 학습 제안 (공백 영역 식별)

## 절차

`agent/workflows/manage-study-list.md`.

## 절대 하지 말 것

- ❌ todo.md 외 위치에 임의 todo 생성
- ❌ 사용자 확인 없이 항목 삭제
- ❌ neuron/ 문서를 todo로 취급 (별개)
- ❌ 임의 commit
