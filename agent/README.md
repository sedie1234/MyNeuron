# agent/ — Claude 설정 관리 디렉토리

MyNeuron 프로젝트의 모든 Claude Code 설정과 에이전트 정의가 여기 모여 있다.

`.claude/agents`와 `.claude/skills`는 이 디렉토리에 대한 **symlink**이므로, 실제 편집은 모두 여기서 한다.

---

## 대전제

- **`.claude/`에는 새 설정 파일을 만들지 않는다.** 모든 설정은 `agent/` 아래에.
- **모든 스킬은 SKILL + workflow를 분리한다.** SKILL.md = "언제·왜", workflow = "어떻게".
- Claude Code가 `.claude/agents`, `.claude/skills`를 표준 위치로 사용하므로 symlink로 연결한다 (운영 측면 보장).

---

## 디렉토리 구조

```
agent/
├── README.md                      # 이 파일
├── neuron-agent.md                # 공유 원칙 (모든 에이전트가 준수)
├── agents/                        # 서브에이전트 정의 (.claude/agents 미러)
│   ├── knowledge-curator.md       # 새 지식 저장/전이
│   ├── knowledge-searcher.md      # 기존 지식 검색 (read-only)
│   ├── knowledge-organizer.md     # 부분 정리/유지보수
│   ├── knowledge-reorganizer.md   # 트리 전체 재구축 (NEW)
│   ├── knowledge-qa.md            # 질문 답변
│   ├── mdbook-builder.md          # mdbook 생성
│   └── study-tracker.md           # 공부 리스트 관리
├── skills/                        # 스킬 정의 (.claude/skills 미러, 활성화 조건만)
│   ├── clarify-question/SKILL.md
│   ├── transfer-knowledge/SKILL.md
│   ├── search-knowledge/SKILL.md
│   ├── organize-knowledge/SKILL.md
│   ├── reorganize-tree/SKILL.md
│   ├── answer-question/SKILL.md
│   ├── create-knowledge-mdbook/SKILL.md
│   └── manage-study-list/SKILL.md
├── workflows/                     # 워크플로우 정의 (step-by-step, NEW)
│   ├── clarify-question.md
│   ├── transfer-knowledge.md
│   ├── search-knowledge.md
│   ├── organize-knowledge.md
│   ├── reorganize-tree.md
│   ├── answer-question.md
│   ├── create-knowledge-mdbook.md
│   └── manage-study-list.md
└── templates/                     # 다른 프로젝트용 CLAUDE.md 템플릿
    ├── experiment-agent.md
    └── project-agent.md
```

---

## 파일 종류

### 1. 공유 원칙 (`neuron-agent.md`)

모든 에이전트가 따르는 원칙·표준:
- 핵심 원칙 (상세 작성, 애매 판단 금지 등)
- Frontmatter 명세 (type별 필드)
- 디렉토리 정책 (tree 기반, 가로 일관성, greedy + 주기적 재구축)
- 지식 연결 전략
- 이미지·버전 관리

### 2. 서브에이전트 (`agents/*.md`)

특정 역할을 담당하는 Claude Code 서브에이전트. 메인 에이전트가 사용자 요청을 받아 적절한 에이전트로 위임.

**얇음**: role + tools + skill 포인터만. 절차는 workflow로 분리.

| 에이전트 | 역할 | 주 스킬 | 도구 |
|---------|------|--------|------|
| knowledge-curator | 새 지식 저장 | transfer-knowledge | Read, Write, Edit, Bash, Grep, Glob |
| knowledge-searcher | 검색 (read-only) | search-knowledge | Read, Grep, Glob |
| knowledge-organizer | 부분 정리 | organize-knowledge | Read, Write, Edit, Bash, Grep, Glob |
| knowledge-reorganizer | 트리 재구축 (NEW) | reorganize-tree | Read, Write, Edit, Bash, Grep, Glob |
| knowledge-qa | 질문 답변 | answer-question + clarify-question | Read, Grep, Glob, Bash, WebFetch, WebSearch |
| mdbook-builder | mdbook 생성 | create-knowledge-mdbook | Read, Write, Edit, Bash, Grep, Glob, Agent |
| study-tracker | 공부 리스트 | manage-study-list | Read, Write, Edit, Grep, Glob |

### 3. 스킬 (`skills/<name>/SKILL.md`)

**얇음**: 활성화 조건 + 비활성화 조건 + 역할 + workflow 포인터. 절차 자체는 들어가지 않음.

| 스킬 | 용도 | 워크플로우 |
|------|------|-----------|
| clarify-question | 지식 질문 모호 시 2-3가지 해석 제안 | workflows/clarify-question.md |
| transfer-knowledge | temp/대화 → neuron/ tree 저장 | workflows/transfer-knowledge.md |
| search-knowledge | tree 가로 단면 검색 | workflows/search-knowledge.md |
| organize-knowledge | 부분 정리 (진단 → 승인 → 실행) | workflows/organize-knowledge.md |
| reorganize-tree | 트리 전면 재구축 (max effort) | workflows/reorganize-tree.md |
| answer-question | neuron/ + 추론 결합 답변 | workflows/answer-question.md |
| create-knowledge-mdbook | content-first mdbook 생성 | workflows/create-knowledge-mdbook.md |
| manage-study-list | todo.md 관리 | workflows/manage-study-list.md |

### 4. 워크플로우 (`workflows/<name>.md`)

**두꺼움**: step-by-step 절차, 예시, 금지 사항. 실제 동작이 여기 정의됨.

frontmatter:
```yaml
---
name: <skill-name>
type: workflow
description: <one-line>
---
```

### 5. 템플릿 (`templates/*.md`)

다른 프로젝트에서 CLAUDE.md로 복사해 사용. MyNeuron 자체 동작과 독립.

| 템플릿 | 사용처 |
|-------|------|
| experiment-agent.md | 실험 프로젝트 |
| project-agent.md | 일반 프로젝트 |

---

## .claude/와의 관계

Claude Code는 `.claude/agents/`, `.claude/skills/`를 표준 위치로 사용. 이 프로젝트에서는 두 경로가 `agent/`로 향하는 **symlink**:

```
.claude/agents  ──symlink──>  ../agent/agents
.claude/skills  ──symlink──>  ../agent/skills
```

따라서:
- **편집은 `agent/`에서**: 단일 source of truth
- **Claude Code는 `.claude/`에서 자동 로드**: 운영 측면 보장

> 워크플로우 디렉토리(`agent/workflows/`)는 `.claude/`로 미러하지 않는다 — Claude Code가 자동 로드하는 영역이 아니라, SKILL.md에서 명시적으로 참조하는 보조 문서.

### Symlink 재생성 (필요 시)

```bash
# Linux/macOS
cd .claude/
rm -f agents skills
ln -s ../agent/agents agents
ln -s ../agent/skills skills
```

```bash
# Windows
rmdir .claude\agents
rmdir .claude\skills
cmd /c mklink /J .claude\agents agent\agents
cmd /c mklink /J .claude\skills agent\skills
```

---

## 새 에이전트 추가

1. `agent/agents/<new-agent>.md` 작성 — frontmatter (name, description, tools) + 얇은 본문 (role + skill 포인터)
2. 필요한 새 스킬·워크플로우를 `agent/skills/`, `agent/workflows/`에 추가
3. `CLAUDE.md`의 라우팅 표 업데이트

## 새 스킬 추가

1. `agent/skills/<name>/SKILL.md` 작성 — frontmatter (name, description, workflow 포인터) + 활성화 조건
2. `agent/workflows/<name>.md` 작성 — step-by-step 절차
3. 관련 에이전트의 정의에 스킬 활용 안내 추가

> **SKILL과 workflow는 반드시 분리.** SKILL에 절차를 넣지 않는다.

---

## 정책 요약

| 정책 | 설명 |
|------|------|
| 단일 source of truth | 모든 편집은 `agent/`에서 |
| `.claude/`에 신규 설정 금지 | 모두 `agent/` 아래에 두고 symlink |
| SKILL ⊥ workflow | 분리해서 관리 |
| 미러링 | `.claude/`는 symlink로 자동 동기화 |
| Push 정책 | `agent/`, `tools/`, `CLAUDE.md`만 remote push 허용 |
| neuron/ 격리 | 지식 문서는 절대 remote push 금지 |
| neuron/ 정책 | tree 기반 (top-level × domain tree), greedy + 주기적 재구축 |

---

## 참고

- `CLAUDE.md` (프로젝트 루트): 라우팅 정책, 빠른 참조
- `agent/neuron-agent.md`: 공유 원칙, frontmatter 명세, 디렉토리 정책
- 각 에이전트/스킬/워크플로우 파일: 구체 정의
