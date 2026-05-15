---
name: create-knowledge-mdbook
description: 사용자가 특정 주제에 대해 mdbook을 만들어 달라고 할 때 사용. neuron/ 하위 관련 지식을 수집하고 챕터로 구성하여 auto theme이 적용된 mdbook을 생성한다. 기본 위치는 books/<category>/<book>/. 백그라운드 에이전트로 위임 권장.
workflow: agent/workflows/create-knowledge-mdbook.md
---

# create-knowledge-mdbook — 지식 mdbook 자동 생성 스킬

`neuron/` 하위 지식을 수집·재구성하여 mdbook 생성. **Content-first** 원칙: 카테고리·챕터를 미리 정하지 않고, 자료를 모은 뒤 도출.

## 활성화 조건

- "X에 대해 mdbook 만들어줘"
- "X 책으로 정리해줘"
- "X 가이드 만들어줘" (mdbook 형식)
- "X 학습 자료 mdbook으로"

## 비활성화 조건

- 단일 파일 작성 ("X 정리해줘") — 일반 markdown
- 기존 mdbook 수정 — 일반 작업으로
- PDF 등 외부 원문에서 직접 변환 — 별개

## 역할

mdbook을 `books/<category>/<book>/`에 생성. neuron/ 원본은 절대 수정하지 않음. 콘텐츠 수집은 다른 에이전트(`knowledge-searcher` 등)에 위임 가능.

## 출력 위치 표준

```
books/<category>/<book>/
```

카테고리는 수집한 콘텐츠의 공통 상위 도메인에서 도출 (neuron/ tree와 일치하도록).

## 절차

`agent/workflows/create-knowledge-mdbook.md`.

## 백그라운드 위임 권장

큰 작업이면 `mdbook-builder` 에이전트를 `run_in_background=true`로.

## 절대 하지 말 것

- ❌ neuron/ 원본 수정
- ❌ 신규 지식 생성 후 mdbook에 포함 (별개 작업)
- ❌ `books/<category>/<book>/` 외 위치 생성
- ❌ 임의 commit/push
