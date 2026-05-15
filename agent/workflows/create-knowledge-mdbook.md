---
name: create-knowledge-mdbook
type: workflow
description: mdbook 생성 step-by-step 절차 (Content-First)
---

# Workflow — create-knowledge-mdbook

활성화 조건은 `agent/skills/create-knowledge-mdbook/SKILL.md` 참조.

> **핵심 원칙**: 카테고리·챕터 구조·템플릿을 미리 정하지 않는다. 자료를 모은 뒤 모인 콘텐츠 기반으로 자연스러운 분류를 도출한 후에야 mdbook 골격을 짠다.

---

## Step 1: 주제와 범위만 식별

사용자 요청에서 다음**만** 파악:
- **주제** (book): 무엇에 대한 mdbook?
- **범위** (scope): 광범위 vs 특정 주제
- **언어/스타일**: 기본 한국어 본문 + 영어 기술용어

이 단계에서 **결정하지 않는 것**:
- ❌ 카테고리 (`compiler`, `hardware` 등)
- ❌ 출력 위치
- ❌ 챕터 구조
- ❌ 템플릿 적용

모호하면 짧게 확인:
```
"X" mdbook 작업 시작합니다. 범위가 좁다/넓다 정도만 알려주시면
그에 맞춰 자료를 모으겠습니다. (카테고리·챕터는 모은 후에 정합니다)
```

---

## Step 2: 지식 수집 (광범위)

`neuron/` 하위에서 관련 문서를 빠짐없이 모은다. tree 구조(공통 domain tree)를 활용:

### A) 직접 수집 (소규모)

```bash
# 키워드 본문
grep -ri "주제키워드" neuron/ --include="*.md" -l

# tags
grep -r "tags:.*주제키워드" neuron/ -l

# tree 경로 (모든 top-level의 같은 leaf)
find neuron/ -type d -name "주제" -o -path "*/주제/*"
```

### B) 다른 에이전트에 위임 (광범위)

| 위임 | 시점 |
|------|------|
| `knowledge-searcher` | 광역 검색 + 분류 결과 회신 |
| `knowledge-qa` | 수집 문서 사이의 개념 흐름·빈 칸 분석 (read-only) |
| `knowledge-curator` | 자료 부족 시 외부 자료로 신규 지식 생성 (별도 단계) |
| `general-purpose` (background) | 대규모 수집 |

위임 프롬프트에 "neuron/ 본문 수정 금지, 수집·분석만" 명시.

### 추출 정보

- frontmatter (title, type, summary, tags, related)
- 본문 핵심 1-3줄 요약
- 본문 핵심 주제어 (분류 단계 입력)

---

## Step 3: 콘텐츠 분석 → 분류·챕터 도출

자료를 펼치고 **자연스럽게 갈라지는 지점**을 찾는다.

1. **주제어 추출** — 각 문서 1-2개씩
2. **클러스터링** — 비슷한 주제어 묶기, 어디에도 안 붙는 것은 "기타" 후보로 분리
3. **순서 결정** — 클러스터 간 의존, 추상→구체, 시간 흐름
4. **크기 조정** — 너무 큰 클러스터는 sub-chapter, 너무 작은 것은 합치기
5. **카테고리·책 이름 확정** — 클러스터 공통 상위 도메인 = 카테고리(예: `compiler`), 주제 = 책(예: `mlir`)
6. **출력 위치** — `books/<category>/<book>/`

분류 도출 결과 보고:
```
수집된 N개 문서 + 외부자료 K개를 분석한 결과 다음 분류를 제안합니다:

출력 위치: books/<category>/<book>/

챕터:
  Ch1. <클러스터 1>  (문서: A, B)
  Ch2. <클러스터 2>  (문서: C, D, E)
  Ch3. ...

이대로 진행할까요?
```

승인 후에만 Step 4 진행. **승인 전에 mdbook 디렉토리 생성 금지**.

### 그룹화 패턴 (참고)

| 방식 | 적용 조건 |
|------|---------|
| 주제어 기준 | 주제별 분기 명확 (가장 일반적) |
| 난이도 기준 | 기초 → 심화 → 응용 흐름 자연스러움 |
| 시간 기준 | 역사·발전사가 핵심 |
| type 기준 | 이론/실험/지식 형식 차이가 본질 (드뭄) |

---

## Step 4: mdbook 생성

### 4.1 디렉토리

```
books/<category>/<book>/
├── book.toml
├── theme/
│   ├── custom.css
│   └── mermaid-init.js
└── src/
    ├── SUMMARY.md
    ├── introduction.md
    └── chN_*.md
```

```bash
mkdir -p books/<category>/<book>/src books/<category>/<book>/theme
```

### 4.2 book.toml (auto theme 표준)

```toml
[book]
title = "<주제> 가이드"
authors = ["Suhwan"]
language = "ko"
src = "src"

[output.html]
default-theme = "light"
preferred-dark-theme = "navy"
mathjax-support = true
smart-punctuation = true
copy-fonts = true
additional-css = ["theme/custom.css"]
additional-js = ["theme/mermaid-init.js"]

[output.html.search]
enable = true
limit-results = 30
boost-title = 2
boost-hierarchy = 1
boost-paragraph = 1
expand = true
heading-split-level = 3

[output.html.fold]
enable = true
level = 0

[output.html.print]
enable = true
page-break = true

[output.html.playground]
editable = false
copyable = true
runnable = false
```

### 4.3 theme/

`temp/polyhedral_mdbook/theme/custom.css`, `mermaid-init.js`를 복사. **`src/` 챕터는 절대 베끼지 않는다** — polyhedral 책 구조이지 새 책 구조가 아님.

### 4.4 SUMMARY.md

```markdown
# Summary

[Introduction](./introduction.md)

# Part I — 이론
- [Chapter 1: ...](./ch01_*.md)

# Part II — 지식
- [Chapter 2: ...](./ch02_*.md)
```

### 4.5 챕터 markdown 변환

기존 neuron/ 문서를 적절히 변환:
- frontmatter 제거 (또는 상단 메타 박스)
- 위키링크 `[[X]]` → mdbook 상대 링크
- 챕터 내 섹션 구조 유지
- 필요 시 다이어그램·표 추가

---

## Step 5: 사용 안내

```
mdbook 생성 완료: books/<category>/<book>/

미리보기:
  mdbook serve books/<category>/<book> --open

빌드:
  mdbook build books/<category>/<book>
  → books/<category>/<book>/book/index.html

설치 필요:
  cargo install mdbook
```

---

## 표준 템플릿 위치

`temp/polyhedral_mdbook/`:
- `book.toml`
- `theme/custom.css`
- `theme/mermaid-init.js`

**복사 대상은 위 세 가지만**. `src/`의 챕터 구성은 절대 따라가지 않는다.

---

## 절대 하지 말 것

- ❌ Step 3 승인 전에 디렉토리 생성
- ❌ neuron/ 본문 수정
- ❌ 신규 지식 만들면서 mdbook에 포함
- ❌ `books/<book>/` 직행 (반드시 `books/<category>/<book>/`)
- ❌ `neuron/` 또는 프로젝트 루트에 book 생성
- ❌ 자의적 commit/push
- ❌ `temp/polyhedral_mdbook/src/` 챕터 베끼기
