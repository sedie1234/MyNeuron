# agent/ — Claude 설정 관리 디렉토리

MyNeuron 프로젝트의 모든 Claude Code 설정과 에이전트 정의가 여기 모여 있다.

`.claude/agents`와 `.claude/skills`는 이 디렉토리에 대한 **junction point**이므로, 실제 편집은 모두 여기서 한다.

---

## 디렉토리 구조

```
agent/
├── README.md                    # 이 파일
├── neuron-agent.md              # 공유 원칙 (모든 에이전트가 준수)
├── agents/                      # Claude Code 서브에이전트 (.claude/agents 미러)
│   ├── knowledge-curator.md     # 새 지식 저장/전이
│   ├── knowledge-searcher.md    # 기존 지식 검색 (read-only)
│   ├── knowledge-organizer.md   # 정기 정리/유지보수
│   ├── knowledge-qa.md          # 질문 답변
│   ├── mdbook-builder.md        # mdbook 생성
│   └── study-tracker.md         # 공부 리스트 관리
├── skills/                      # Claude Code 스킬 (.claude/skills 미러)
│   ├── clarify-question/
│   │   └── SKILL.md             # 모호한 질문 명확화 제안
│   └── create-knowledge-mdbook/
│       └── SKILL.md             # mdbook 생성 워크플로우
└── templates/                   # 다른 프로젝트용 CLAUDE.md 템플릿
    ├── experiment-agent.md      # 실험 프로젝트용
    └── project-agent.md         # 일반 프로젝트용
```

---

## 파일 종류

### 1. 공유 원칙 (`neuron-agent.md`)

모든 에이전트(메인 + 서브)가 따르는 원칙과 표준:
- 핵심 원칙 (상세 작성, 애매 판단 금지 등)
- Frontmatter 명세 (type별 필드)
- 지식 연결 전략
- 디렉토리 구조
- 이미지 관리
- 버전 관리 (git push 정책)

### 2. 서브에이전트 (`agents/*.md`)

특정 역할을 담당하는 Claude Code 서브에이전트. 메인 에이전트가 사용자 요청을 받아 적절한 서브에이전트에 위임.

각 파일은 frontmatter (name, description, tools)와 시스템 프롬프트로 구성됨.

| 에이전트 | 핵심 역할 | 도구 |
|---------|---------|------|
| knowledge-curator | 새 지식 저장 | Read, Write, Edit, Bash, Grep, Glob |
| knowledge-searcher | 검색 (read-only) | Read, Grep, Glob |
| knowledge-organizer | 정기 정리 | Read, Write, Edit, Bash, Grep, Glob |
| knowledge-qa | 질문 답변 | Read, Grep, Glob, Bash, WebFetch, WebSearch |
| mdbook-builder | mdbook 생성 | Read, Write, Edit, Bash, Grep, Glob |
| study-tracker | 공부 리스트 | Read, Write, Edit, Grep, Glob |

### 3. 스킬 (`skills/<name>/SKILL.md`)

인라인 동작 모디파이어. 메인/서브에이전트가 특정 상황에 적용하는 행동 규칙.

| 스킬 | 용도 |
|------|------|
| clarify-question | 지식 질문이 모호할 때 2-3가지 해석 제안 |
| create-knowledge-mdbook | mdbook 생성 워크플로우 정의 (mdbook-builder가 활용) |

### 4. 템플릿 (`templates/*.md`)

다른 프로젝트(실험, 일반 프로젝트)에서 CLAUDE.md로 복사해 사용하는 템플릿. MyNeuron 자체의 동작과는 독립적.

| 템플릿 | 사용처 |
|-------|------|
| experiment-agent.md | 실험 프로젝트 (CLAUDE.md로 복사) |
| project-agent.md | 일반 프로젝트 (CLAUDE.md로 복사) |

이 템플릿들은 `__MyNeuron/temp/`로 결과물을 보내 메인 시스템에 통합되도록 설계됨.

---

## .claude/와의 관계

Claude Code는 `.claude/agents/`와 `.claude/skills/`를 표준 위치로 사용.

이 프로젝트에서는 두 경로가 **Windows junction point**로 `agent/agents/`와 `agent/skills/`를 가리킴:

```
.claude/agents  ──junction──>  agent/agents
.claude/skills  ──junction──>  agent/skills
```

따라서:
- **편집은 `agent/`에서**: 단일 source of truth
- **Claude Code는 `.claude/`에서 자동 로드**: 운영 측면 보장

### Junction 재생성 (필요 시)

```bash
# 기존 junction 제거
rmdir .claude/agents
rmdir .claude/skills

# 재생성
cmd //c "mklink /J .claude\\agents agent\\agents"
cmd //c "mklink /J .claude\\skills agent\\skills"
```

### 다른 OS에서

macOS/Linux에서는 symbolic link 사용:
```bash
ln -s ../agent/agents .claude/agents
ln -s ../agent/skills .claude/skills
```

---

## 새 에이전트 추가 방법

1. `agent/agents/<new-agent>.md` 작성
   - frontmatter: `name`, `description`, `tools`
   - 본문: 시스템 프롬프트
2. `CLAUDE.md`의 라우팅 표 업데이트 (트리거 패턴 추가)
3. 필요 시 `agent/neuron-agent.md` 또는 다른 에이전트와의 협업 정책 명시

## 새 스킬 추가 방법

1. `agent/skills/<skill-name>/SKILL.md` 작성
   - frontmatter: `name`, `description`
   - 본문: 활성화 조건, 동작 방식
2. 관련 에이전트의 정의에 스킬 활용 안내 추가

---

## 정책 요약

| 정책 | 설명 |
|------|------|
| 단일 source of truth | 모든 편집은 `agent/`에서 |
| 미러링 | `.claude/`는 junction으로 자동 동기화 |
| Push 정책 | `agent/`, `tools/`, `CLAUDE.md`만 remote push 허용 |
| neuron/ 격리 | 지식 문서는 절대 remote push 금지 |
| 공유 원칙 준수 | 모든 에이전트가 `neuron-agent.md` 원칙 따름 |

---

## 참고

- `CLAUDE.md` (프로젝트 루트): 라우팅 정책, 빠른 참조
- `agent/neuron-agent.md`: 공유 원칙, frontmatter 명세
- 각 에이전트/스킬 파일: 구체 동작 정의
