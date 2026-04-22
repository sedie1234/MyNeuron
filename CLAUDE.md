# MyNeuron - 지식 축적 시스템

이 프로젝트는 개인 지식 축적 시스템입니다. Claude Code agent가 지식의 수집, 정리, 연결, 회상을 돕습니다.

## Agent 설정 로드

이 디렉토리에서 Claude Code를 실행할 때, 아래 agent 설정을 참조하여 동작합니다:
- 전체 시스템 지침: `agent/neuron-agent.md`를 읽고 그 내용에 따라 동작할 것.

## Git 원격 저장소 정책

- 원격 push는 `https://github.com/sedie1234/MyNeuron` 으로만 허용한다.
- **`neuron/` 하위의 지식 문서는 절대 원격 저장소에 push하지 않는다.** 지식 문서는 로컬 git으로만 관리한다.
- push 대상: agent 설정(`agent/`), 도구(`tools/`), 프로젝트 설정(`CLAUDE.md`, `.gitignore` 등)

## 빠른 참조

- 지식 저장소: `neuron/` 하위 디렉토리
- 임시 문서: `temp/` (외부에서 가져온 문서)
- 도구: `tools/` (이미지 생성 등)
- Agent 설정: `agent/` (agent 정의 파일)
- 지시서: `order/` (원본 지시서)
