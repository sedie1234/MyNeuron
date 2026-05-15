---
name: reorganize-tree
description: neuron/ 트리 전체를 콘텐츠 기반으로 다시 짜는 주기적 재구축 스킬. greedy 누적 드리프트 보정. 모든 문서를 다시 클러스터링하여 새 tree 도출 → 승인 후 일괄 이동 + 모든 wikilink 갱신 + domain 필드 갱신. 백업·롤백 가능.
workflow: agent/workflows/reorganize-tree.md
---

# reorganize-tree — 트리 전체 재구축 스킬

`transfer-knowledge`가 greedy로 분류한 결과 누적된 드리프트를 **주기적으로 한 번에 보정**. neuron/ 전체를 콘텐츠 기반으로 다시 클러스터링하여 새 tree를 짜고, 사용자 승인 후 일괄 이동.

## 활성화 조건

- "지식 트리 정리해줘", "내부 지식 정리"
- "트리 재구축", "neuron 재분류"
- "전체 카테고리 재정비"
- 분기/연 단위 정기 정리

## 비활성화 조건

- 부분 정리 (→ `organize-knowledge`)
- 단일 문서 이동 (→ `transfer-knowledge`나 직접 mv)

## 역할

다음을 책임진다:

1. **전체 스캔**: 모든 top-level × 전체 tree 깊이
2. **콘텐츠 재클러스터링**: 현 경로/카테고리에 얽매이지 않고 frontmatter+본문 기반으로 자연스러운 분류 도출
3. **새 tree 제안**: 도출된 클러스터를 tree로 표현, 모든 파일의 새 경로 매핑 제시
4. **승인 절차**: 사용자가 부분 수정 가능
5. **백업**: 실행 전 스냅샷 (롤백 가능)
6. **일괄 실행**: 파일 이동 + 모든 wikilink 갱신 + frontmatter `domain` 갱신
7. **검증**: 실행 후 끊긴 링크·이름 불일치 점검
8. **commit** (push 금지)

## 핵심 원칙

- **콘텐츠 우선** — 기존 카테고리는 힌트일 뿐, 절대적 기준 아님
- **가로 일관성** — 모든 top-level이 같은 domain tree 공유 (이론/compiler/mlir, 지식/compiler/mlir 동일 leaf)
- **백업 필수** — 실행 전 `temp/neuron-snapshot-<date>/`에 복사 또는 git tag
- **무손실** — 어떤 문서도 누락·삭제되지 않음 (이동만)
- **사용자 단계별 승인** — 트리 안, 매핑, 실행 각 단계

## 절차

`agent/workflows/reorganize-tree.md` (max effort).

## 절대 하지 말 것

- ❌ 백업 없이 실행
- ❌ 사용자 승인 없이 파일 이동
- ❌ wikilink 갱신 누락 (이동만 하고 링크 깨뜨림)
- ❌ frontmatter `domain` 필드 무시 (새 경로와 일치 강제)
- ❌ 문서 삭제 (절대) — 이동만
- ❌ 한 번에 commit (실행 자체는 한 번에, 다만 검증 후 commit 분리 권장)
- ❌ neuron/ remote push
- ❌ 부분 정리 케이스에 호출 (그건 organize-knowledge)
