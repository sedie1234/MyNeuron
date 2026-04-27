---
name: create-knowledge-mdbook
description: 사용자가 특정 주제에 대해 mdbook을 만들어 달라고 할 때 사용. neuron/ 하위 관련 지식을 수집하고 챕터로 구성하여 auto theme이 적용된 mdbook을 생성한다. 기본 위치는 temp/<topic>_mdbook/. 백그라운드 에이전트로 위임 권장.
---

# create-knowledge-mdbook — 지식 모음 mdbook 자동 생성 스킬

사용자가 "X에 대해 mdbook 만들어줘" 같은 요청을 하면, neuron/ 하위 관련 지식을 수집·재구성하여 mdbook을 생성한다.

---

## 활성화 조건

다음과 같은 사용자 요청에서 작동:

- "X에 대해 mdbook 만들어줘" / "책으로 정리해줘"
- "X 관련 지식 모아서 mdbook으로"
- "X 학습 자료 mdbook으로 묶어줘"
- "X 가이드 만들어줘" (mdbook 형태로)

**비활성화 조건**:
- 단일 파일 작성 요청 ("X에 대해 정리해줘") — 이건 일반 markdown
- PDF 등 외부 자료에서 직접 만들기 요청 — 별개 (이전 polyhedral 사례 참조)
- 기존 mdbook 수정 요청 — 일반 작업으로 처리

---

## 작동 방식 (Workflow)

### Step 1: 주제와 범위 식별

사용자 요청에서 다음을 파악:
- **주제** (topic): 무엇에 대한 mdbook?
- **범위** (scope): 광범위(예: "compiler 전체") vs 특정(예: "polyhedral만")
- **위치** (location): 기본 `temp/<topic>_mdbook/` 또는 사용자 지정
- **언어/스타일**: 기본 한국어 본문 + 영어 기술용어

**모호하면 clarify-question 적용**:
```
주제 범위가 모호합니다. 기본적으로 [기본 해석]으로 진행하겠습니다:
- A: [좁은 해석]
- B: [넓은 해석]
- C: [다른 해석]

다른 방향이시면 알려주세요.
```

### Step 2: 관련 지식 수집

`neuron/` 하위에서 관련 문서 수집:

```bash
# 키워드 기반 검색
grep -r "주제키워드" neuron/ --include="*.md" -l

# tags 기반
grep -r "tags:.*주제키워드" neuron/ -l

# 디렉토리 기반 (이론/, 실험/, 지식/, 프로젝트/, 대화/)
find neuron/ -name "*주제*" -o -name "*topic*"
```

각 문서에서 다음 정보 추출:
- frontmatter (title, type, summary, tags, related)
- 본문 핵심 내용

### Step 3: 챕터 구조 설계

수집된 문서를 **논리적 챕터**로 그룹화. 보통 다음 패턴:

| 그룹 방식 | 예시 |
|----------|------|
| **type 기준** | 이론(theory) → 지식(knowledge) → 실험(experiment) → 대화(conversation) |
| **주제 기준** | 기초 → 심화 → 응용 (난이도 순) |
| **시간 기준** | 역사 → 현재 → 전망 |
| **사용자 지정** | 사용자가 명시한 구조 따름 |

기본은 **이론→지식→실험→프로젝트→대화** 순. 모호하면 사용자에게 확인.

### Step 4: mdbook 생성

#### 4.1 디렉토리 구조

```
temp/<topic>_mdbook/
├── book.toml
├── theme/
│   ├── custom.css
│   └── mermaid-init.js
└── src/
    ├── SUMMARY.md
    ├── introduction.md
    └── chN_*.md  (챕터별)
```

#### 4.2 book.toml (auto theme 표준)

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

#### 4.3 theme/custom.css

한국어 가독성 + 표/코드/blockquote 스타일링. 표준 템플릿 사용 (이전 polyhedral_mdbook 참조).

#### 4.4 theme/mermaid-init.js

Mermaid CDN 동적 로딩 (light/dark 자동 감지). 표준 템플릿 사용.

#### 4.5 SUMMARY.md

```markdown
# Summary

[Introduction](./introduction.md)

# Part I — 이론
- [Chapter 1: ...](./ch01_*.md)

# Part II — 지식
- [Chapter 2: ...](./ch02_*.md)

# Part III — 실험
...
```

#### 4.6 각 챕터 markdown

기존 neuron/ 문서를 적절히 변환:
- frontmatter 제거 (또는 위쪽 메타 박스로)
- 위키링크 `[[X]]`를 mdbook 링크로 변환
- 챕터 내 섹션 구조 유지
- 필요 시 다이어그램/표 추가

### Step 5: 사용 안내

생성 후 다음 안내:

```
mdbook 생성 완료: temp/<topic>_mdbook/

미리보기:
  mdbook serve temp/<topic>_mdbook --open

빌드만:
  mdbook build temp/<topic>_mdbook
  → temp/<topic>_mdbook/book/index.html

설치 필요:
  cargo install mdbook
  (또는 https://github.com/rust-lang/mdBook/releases 에서 binary)
```

---

## 백그라운드 에이전트로 위임 권장

**왜?**
- 지식 수집·구조화·작성 모두 시간 소요
- 컨텍스트 부담 큼 (여러 파일 읽고 종합)
- 사용자가 다른 작업 진행 가능

**위임 시 프롬프트에 포함**:
- 주제와 범위
- 수집할 디렉토리 (보통 neuron/)
- 출력 위치
- 챕터 구조 (자유 또는 지정)
- 표준 템플릿 위치 (`temp/polyhedral_mdbook`을 레퍼런스로)
- 제약 (git push 금지 등)

---

## 표준 템플릿 위치

기존 `temp/polyhedral_mdbook/`이 표준 템플릿 역할:
- `book.toml`: auto theme 설정 표준
- `theme/custom.css`: Korean-friendly CSS
- `theme/mermaid-init.js`: Mermaid CDN 로더

새 mdbook 생성 시 이 파일들을 복사·수정하여 시작.

---

## 절대 하지 말 것

### 강요/되묻기 금지
- ❌ 모호점 너무 많이 짚기 (clarify-question 원칙 따르기)
- ❌ "구조를 먼저 정해주세요"로 되묻기만 하기

### 위치 위반
- ❌ `neuron/` 하위에 mdbook 만들기 (지식 문서 영역 침범)
- ❌ 프로젝트 루트에 `book/` 등 임의 위치 생성
- 기본은 `temp/<topic>_mdbook/` 

### 지식 영역 변경
- ❌ neuron/ 원본 문서 수정 (mdbook은 복사본 사용)
- ❌ 신규 지식을 만들면서 mdbook에 포함 (지식 전이는 별개 작업)

### Git
- ❌ 자의적으로 commit/push (.claude/skills/도 .gitignore 됨)
- 사용자 명시적 요청 있을 때만

---

## 좋은 예시

### 예 1: 명확한 주제

**사용자**: "polyhedral 관련 지식 모아서 mdbook 만들어줘"

**스킬 동작**:
1. `neuron/` 하위 polyhedral 관련 문서 수집 (`grep -r polyhedral`)
   - `이론/compiler/polyhedral_model.md`
   - `대화/polyhedral_*.md` (7개)
   - `지식/compiler/polyhedral_history.md`
2. 챕터 구성:
   - Part I — 이론 (polyhedral_model)
   - Part II — 핵심 개념 (access function, dependence, mapping)
   - Part III — 구체 사례 (SOR, transformation sequence)
   - Part IV — 역사
3. `temp/polyhedral_knowledge_mdbook/` 생성
4. 안내 출력

### 예 2: 모호한 주제 — clarify-question 적용

**사용자**: "compiler에 대해 mdbook 만들어줘"

**스킬 동작**:
```
"compiler"는 범위가 넓습니다. 기본적으로 이론(이론/compiler/)을 중심으로
mdbook을 만들겠습니다. 다른 방향이시면 알려주세요:
- A: 컴파일러 이론 전체 (이론/compiler/ 16개 문서)
- B: AI 컴파일러 중심 (이론/AICompiler/ + 관련 지식)
- C: 폴리헤드럴 중심 (해당 주제만)

[A 방향으로 진행]
```

---

## 스킬과 다른 스킬의 관계

| 다른 스킬 | 관계 |
|----------|------|
| **clarify-question** | 주제 모호할 때 호출 |
| (가상) **knowledge-search** | neuron/ 검색 도구 (있다면 활용) |

---

## 한 문장 요약

> **사용자가 특정 주제로 mdbook을 요청하면, neuron/ 하위 관련 지식을 수집·재구성하여 auto theme이 적용된 mdbook을 `temp/<topic>_mdbook/`에 생성한다. 모호하면 clarify-question을 적용하고, 작업은 백그라운드 에이전트에 위임하는 것이 효율적이다.**
