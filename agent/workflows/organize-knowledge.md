---
name: organize-knowledge
type: workflow
description: neuron/ 부분 정리 절차 — 진단 → 보고 → 승인 → 실행 → 마무리
---

# Workflow — organize-knowledge

활성화 조건은 `agent/skills/organize-knowledge/SKILL.md` 참조.

> 트리 전체 재구축이 아니라 **부분 정리**. 범위를 좁혀 진행한다.

---

## Phase 0: 범위 합의

사용자에게 짧게 확인 (자명하면 생략):
```
정리 범위를 알려주세요:
- A. 특정 leaf (예: neuron/이론/compiler/ai-compiler/mlir/)
- B. 특정 top-level (예: neuron/지식/)
- C. 특정 domain subtree (예: neuron/*/compiler/)
- D. 전체 neuron/  ← 큰 작업이면 reorganize-tree 검토
```

이후 단계는 합의된 범위 안에서만 진행.

---

## Phase 1: 진단 (Diagnose)

### 1.1 통계 수집

```bash
# 범위 내 문서 수
find <범위> -name "*.md" | wc -l

# top-level별 / leaf별 분포
find <범위> -name "*.md" | awk -F/ '{print $2}' | sort | uniq -c
```

### 1.2 항목별 스캔

| 항목 | 방법 |
|------|------|
| **중복** | title/summary/tags 비교 (Levenshtein 또는 jaccard) |
| **충돌** | `grep -l "status: conflicted" <범위>` |
| **끊긴 링크** | 본문 `[[X]]`와 `related` 필드 → 실제 파일 매칭 |
| **고아** | inbound 0 + outbound 0 |
| **카테고리 불일치** | frontmatter `domain` vs 실제 경로 비교 |
| **frontmatter 비표준** | 필수 필드 누락, 한국어 필드명, 날짜 형식 |
| **stale** | `updated` < 6개월 전 |
| **양방향 미일치** | A의 related에 B 있는데 B에 A 없음 |
| **빈 디렉토리** | `find <범위> -type d -empty` |
| **오래된 draft** | `status: draft` + `created` 오래됨 |

### 1.3 발견 사항 수집

각 항목을 우선순위로 분류:
- 🔴 높음 (즉시 조치 권장): 끊긴 링크, 충돌, 중복 (80%+ 유사)
- 🟡 중간 (검토 권장): 고아, 카테고리 불일치, frontmatter 누락
- 🟢 낮음 (선택): stale, 양방향 미일치, 빈 디렉토리

---

## Phase 2: 보고 (Report)

표 형식으로:

```markdown
# 📊 neuron 진단 보고 (범위: <범위>)

## 전체 통계
- 문서 수: N개
- top-level 분포: 이론 X, 지식 Y, 실험 Z, ...
- 마지막 정리 후 신규: M개

## 발견 사항

### 🔴 높음
| # | 항목 | 영향 파일 | 제안 |
|---|------|---------|------|
| 1 | 중복 의심 | A.md, B.md (유사도 0.85) | 병합 |
| 2 | 끊긴 링크 | C.md → [[D]] (D 없음) | 대상 찾기/제거 |

### 🟡 중간
...

### 🟢 낮음
...

## 진행 옵션
[A] 1번 병합 — A.md + B.md → AB.md
[B] 2번 링크 수정 — C.md의 [[D]] 해결
[C] 전부 진행
[D] 건너뛰기

진행할 항목 알려주세요.
```

---

## Phase 3: 실행 (Execute)

사용자 승인 받은 항목에 한해.

### 3.1 병합

1. 두 문서 frontmatter 통합:
   - tags = 합집합
   - related = 합집합
   - created = 둘 중 더 이른 날짜
   - updated = 오늘
   - status = 더 높은 검증 단계
2. 본문 통합 (중복 제거, 차이 보존)
3. 새 파일 작성, 원본 2개 deprecated 또는 삭제 (사용자 선택)
4. 양방향 링크 갱신 (다른 문서의 related/wikilink)

### 3.2 이동 (카테고리 불일치)

1. `mv` 또는 git mv
2. 모든 wikilink 갱신 (`grep -rl '[[old_name]]' neuron/`)
3. `domain` 필드 새 경로로

### 3.3 링크 수정

1. 의도된 대상 추정 (이름 유사도, related context)
2. 사용자 확인 후 갱신 또는 제거

### 3.4 Frontmatter 표준화

1. 필수 필드 추가
2. 형식 통일 (날짜, tags lowercase 등)
3. type별 추가 필드 채우기 (가능한 경우)

---

## Phase 4: 마무리 보고

```markdown
# ✅ 정리 완료

## 수행
- 병합: N건
- 이동: M건
- 링크 수정: K건
- Frontmatter 갱신: L건

## 변경 파일
[목록]

## 남은 항목
- 사용자 보류한 J건 (다음 회차 검토)

## 다음 정리 권장 시점
- 약 N개 문서 추가 후, 또는 1개월 후
```

---

## 절대 하지 말 것

- ❌ 사용자 승인 없이 변경
- ❌ 정보 손실 (병합 시 unique 내용 누락)
- ❌ 임의 새 카테고리 생성
- ❌ 한 번에 50건+ 일괄 실행 (사용자 검토 불가) — 점진적
- ❌ commit/push 자의 (사용자 명시 시에만)
- ❌ 트리 전체 재구축 (그건 reorganize-tree)
