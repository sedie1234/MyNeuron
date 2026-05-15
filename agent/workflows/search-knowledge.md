---
name: search-knowledge
type: workflow
description: tree-aware 가로 검색 절차 — 모든 top-level의 같은 leaf 경로를 모으고 frontmatter+요약으로 반환
---

# Workflow — search-knowledge

활성화 조건은 `agent/skills/search-knowledge/SKILL.md` 참조.

---

## Step 1: 검색 어휘 정규화

사용자 입력에서 주제어 추출:
- 원어 (예: "MLIR", "polyhedral", "mojo")
- 동의어/대역 (예: "다면체" ↔ "polyhedral", "다단계 IR" ↔ "MLIR")
- 표기 변형 (대소문자, 하이픈/언더스코어)

검색 키워드 셋 = {원어, 동의어, 변형}.

---

## Step 2: Tree 경로 후보 만들기

주제어 → 가능한 leaf 디렉토리명 후보:

```
candidates = ["mlir", "MLIR"]  # 카테고리 명명 규칙상 소문자가 표준
```

부모 경로 후보(주제어의 일반화된 상위 도메인):

```
parents = ["compiler/ai-compiler/", "compiler/", "compiler/ir/"]
```

---

## Step 3: Tree 가로 스캔

### 3.1 leaf 직접 매칭

```bash
# 모든 top-level에서 같은 leaf 이름
find neuron/ -type d -name "mlir" 2>/dev/null

# 결과 예:
# neuron/이론/compiler/ai-compiler/mlir/
# neuron/지식/compiler/ai-compiler/mlir/
# neuron/실험/npu-compiler/compiler/ai-compiler/mlir/
```

### 3.2 부분 매칭 (leaf가 없거나 다른 깊이 가능성)

```bash
# 경로 어딘가에 주제어
find neuron/ -path "*mlir*" -name "*.md" 2>/dev/null
```

### 3.3 본문/frontmatter 검색 (tree에 안 잡히면)

```bash
# 본문 키워드
grep -ril "mlir" neuron/ --include="*.md"

# tags
grep -ril "tags:.*mlir" neuron/ --include="*.md"

# title
grep -ril "^title:.*mlir" neuron/ --include="*.md"
```

---

## Step 4: 결과 분류 (top-level별)

발견된 파일을 top-level별로 그룹화:

```
이론/   → 순수 이론 지식
지식/   → 확정된 정리·전이 지식
실험/   → 실험 기록 (project별)
프로젝트/ → 프로젝트 컨텍스트 지식 (project별)
대화/   → 대화 추출물
```

각 파일에서 추출:
- 경로
- frontmatter (title, type, status, summary, tags, domain)
- updated 날짜
- (옵션) related 필드 (그래프 확장용)

---

## Step 5: 관련 그래프 확장 (요청 시)

- "X에 대한 모든 지식" 같은 요청이면 related 따라가기
- 직접 매칭 문서들의 `related` → 추가 문서 발견
- 같은 `tags` 가진 문서 → 군집 식별
- 한 hop만 확장 (그 이상은 noise 큼)

---

## Step 6: 응답 포맷

```
🔍 "<주제>" 검색 결과 (총 N개, top-level M개에 분포)

## 이론/ (K개)
| 경로 | summary | status | updated |
|------|---------|--------|---------|
| neuron/이론/compiler/ai-compiler/mlir/overview.md | ... | confirmed | 2026-04-07 |

## 지식/ (K개)
| 경로 | summary | status | updated |
...

## 실험/ (project별, K개)
- **npu-compiler**:
  - neuron/실험/npu-compiler/compiler/ai-compiler/mlir/lowering.md (...)

## 프로젝트/ (project별, K개)
...

## 대화/ (K개)
...

## 관련 그래프 (1-hop, J개)
| 경로 | 어느 문서에서 related? |
|------|-----------------------|

## 핵심 요약 (200-500자)
[직접 매칭 문서들의 frontmatter summary를 종합한 짧은 요약]
```

---

## 검색 깊이 조절

| 요청 유형 | 깊이 |
|---------|------|
| "X 있어?" | 얕음 — 경로 + 존재 여부 |
| "X 찾아줘" | 중간 — 경로 + summary |
| "X에 관한 모든 지식" | 깊음 — 경로 + summary + 본문 핵심 + 관련 그래프 |

---

## 효율성 원칙

- 전체 neuron/ 통째로 grep 금지 — tree 후보부터 좁힘
- Read 시 frontmatter + 첫 섹션 위주 (전체 본문 자제)
- 결과 0개 시: 동의어/일반화된 leaf로 재시도
- top-level별 N개 초과면 절단 + "...외 K개" 표시

---

## 절대 하지 말 것

- ❌ 검색 결과로 답변 생성 (다른 스킬)
- ❌ 파일 수정
- ❌ 추측으로 결과 만들기
- ❌ 표 없이 비구조화된 dump
- ❌ tree 구조 무시한 flat list 반환 (top-level 그룹화 필수)
