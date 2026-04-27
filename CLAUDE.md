# MyNeuron - 지식 축적 시스템

이 프로젝트는 개인 지식 축적 시스템입니다. Claude Code agent가 지식의 수집, 정리, 연결, 회상을 돕습니다.

## Agent 설정 로드

이 디렉토리에서 Claude Code를 실행할 때, 아래 agent 설정을 참조하여 동작합니다:
- **공유 원칙**: `agent/neuron-agent.md` (모든 에이전트가 준수)
- **서브에이전트 정의**: `agent/agents/*.md` (`.claude/agents/`에 junction)
- **스킬 정의**: `agent/skills/*/SKILL.md` (`.claude/skills/`에 junction)
- **전체 구조**: `agent/README.md`

> 모든 Claude 설정은 `agent/`에서 단일 source of truth로 관리되며, `.claude/`는 junction point로 자동 미러됨.

## 서브에이전트 라우팅 정책

역할별로 분리된 6개 서브에이전트가 `agent/agents/`에 정의되어 있다.
사용자 요청 유형에 따라 **적절한 서브에이전트로 위임**한다.

### 라우팅 표

| 사용자 요청 유형 | 서브에이전트 | 트리거 예시 |
|---------------|------------|----------|
| **새 지식 저장/전이** | `knowledge-curator` | "지식 전이", "이거 저장해줘", "기억 전이", "neuron에 추가" |
| **기존 지식 검색** | `knowledge-searcher` | "neuron에 X 있어?", "이전에 정리한 X 찾아줘", "관련 지식 보여줘" |
| **지식 정리/유지보수** | `knowledge-organizer` | "지식 정리", "neuron 청소", "중복 찾기", "끊긴 링크 점검", "정리 제안" |
| **질문 답변 (학습/탐구)** | `knowledge-qa` | "X에 대해 설명", "X와 Y 차이는?", "왜 X?", 일반 기술/이론 질문 |
| **mdbook 생성** | `mdbook-builder` | "X mdbook 만들어줘", "X 책으로 정리", "X 가이드 만들기" |
| **공부 리스트 관리** | `study-tracker` | "todo 추가", "공부할 거 추가", "다음 공부 제안", "todo 보여줘" |

### 라우팅 원칙

1. **명확한 매칭이면 즉시 위임** — 위 표의 트리거 패턴이 명확하면 해당 에이전트 호출
2. **모호하면 메인 에이전트가 직접 처리** — 단순 대화, 짧은 확인 등
3. **복합 요청은 순차 위임** — 예: "X에 대해 설명하고 저장해줘" → knowledge-qa → knowledge-curator
4. **서브에이전트 간 호출 가능** — knowledge-qa가 knowledge-searcher 활용 등
5. **백그라운드 위임 권장** — mdbook-builder처럼 시간 소요 큰 작업은 `run_in_background=true`

### 서브에이전트 미사용 케이스

다음은 메인 에이전트가 직접 처리:
- 단순 인사, 짧은 응답
- 명령 실행 (`bash`, git 등 단순)
- 설정 변경 (skill, settings.json 등)
- 메타 질문 ("어떤 에이전트가 있어?", "이 세션 뭐 했어?" 등)

### 기존 스킬과의 관계

- **clarify-question 스킬**: 모든 에이전트(특히 knowledge-qa, mdbook-builder)에서 모호한 요청에 적용
- **create-knowledge-mdbook 스킬**: mdbook-builder의 워크플로우 정의
- **update-config, init 등 시스템 스킬**: 메인 에이전트 영역

## Git 원격 저장소 정책

- 원격 push는 `https://github.com/sedie1234/MyNeuron` 으로만 허용한다.
- **`neuron/` 하위의 지식 문서는 절대 원격 저장소에 push하지 않는다.** 지식 문서는 로컬 git으로만 관리한다.
- push 대상: agent 설정(`agent/`), 도구(`tools/`), 프로젝트 설정(`CLAUDE.md`, `.gitignore` 등)

## 빠른 참조

- 지식 저장소: `neuron/` 하위 디렉토리
- 임시 문서: `temp/` (외부에서 가져온 문서)
- 도구: `tools/` (이미지 생성 등)
- **Agent 설정 (단일 source of truth)**: `agent/`
  - 공유 원칙: `agent/neuron-agent.md`
  - 서브에이전트: `agent/agents/`
  - 스킬: `agent/skills/`
  - 다른 프로젝트용 템플릿: `agent/templates/`
- `.claude/`: Claude Code 운영 디렉토리 (`.claude/agents`, `.claude/skills`는 `agent/`에 대한 junction)
- 지시서: `order/` (원본 지시서)
- TODO/연구 거리: `todo.md`
