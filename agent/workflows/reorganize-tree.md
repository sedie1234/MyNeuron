---
name: reorganize-tree
type: workflow
description: neuron/ 트리 전체 재구축의 step-by-step 절차 (max effort). 백업 → 스캔 → 클러스터링 → 새 트리 도출 → 승인 → 일괄 이동 → 링크 갱신 → 검증 → commit.
---

# Workflow — reorganize-tree

활성화 조건은 `agent/skills/reorganize-tree/SKILL.md` 참조.

> 이 작업은 **거대한 변경**이다. 단계별 사용자 승인 + 백업 + 검증을 모두 거친다.

---

## Phase 0: 사전 합의 & 백업

### 0.1 의도 확인

```
neuron/ 트리 전체 재구축을 시작합니다. 큰 작업이며 단계별 승인이 필요합니다:

1. 스캔 (read-only)
2. 콘텐츠 클러스터링 → 새 트리 제안
3. 파일별 새 경로 매핑 제시
4. 사용자 검토·수정
5. 백업 후 일괄 실행
6. 링크 갱신·검증
7. commit

진행할까요? (백업 위치는 temp/neuron-snapshot-<오늘날짜>/ 또는 git tag로 잡습니다)
```

### 0.2 백업 실행

승인되면 **무조건 백업부터**:

```bash
DATE=$(date +%Y-%m-%d)
mkdir -p temp/neuron-snapshot-$DATE
cp -r neuron/ temp/neuron-snapshot-$DATE/

# git tag도 병행 (이미 git repo면)
git tag neuron-pre-reorg-$DATE
```

백업 완료 보고 후 Phase 1 진행.

---

## Phase 1: 전체 스캔

### 1.1 인벤토리

```bash
# 모든 문서 목록
find neuron/ -name "*.md" -not -path "*/images/*" > /tmp/inventory.txt
wc -l /tmp/inventory.txt
```

### 1.2 각 문서에서 추출

각 파일에 대해:
- 경로 (현재 위치)
- frontmatter 전체 (type, status, tags, related, domain, summary)
- 본문 핵심 키워드 (제목 + 첫 H1/H2 + 본문 빈도 상위)
- 본문 길이

결과를 메모리 또는 임시 인덱스 파일로 보관:

```
파일별 레코드:
{
  path: "neuron/이론/compiler/mlir.md",
  type: "theory",
  tags: [...],
  domain_field: "compiler",
  keywords: ["mlir", "dialect", "ir", ...],
  related: [...],
  size: 1024
}
```

### 1.3 통계 보고

```
스캔 완료: N개 문서

top-level 분포: 이론 X, 지식 Y, 실험 Z, 프로젝트 W, 대화 V
현재 tree 깊이 분포: 1단(N1), 2단(N2), 3단(N3), 4단+(N4)
tags 빈도 top 30: ...
keyword 빈도 top 50: ...
```

---

## Phase 2: 콘텐츠 재클러스터링

### 2.1 도메인 클러스터 추출

기존 경로 무시하고 **콘텐츠 기반**:

- tags + keywords로 문서별 벡터 구성
- 키워드 기반 클러스터링 (간단한 keyword-frequency 또는 LLM 직접 분류)
- 클러스터의 자연스러운 이름 부여 (예: `compiler/ai-compiler/mlir`)

### 2.2 클러스터 hierarchy 도출

- 클러스터 간 포함 관계 식별 (예: mlir ⊂ ai-compiler ⊂ compiler)
- 트리 깊이 결정: 의미가 분기할 때만 깊이 증가
- 카테고리 명명: 영문 소문자, `-` 구분, 단수형

### 2.3 가로 일관성 확보

각 클러스터(leaf)에 대해 모든 top-level의 후보 문서 확인:

```
mlir 클러스터:
- 이론/: [overview, three-principles, ...]
- 지식/: [practical-guide, pass-pattern, ...]
- 실험/: project별 [{npu-compiler: [lowering]}, ...]
- 프로젝트/: project별 [...]
- 대화/: [...]
```

→ leaf 경로는 동일하게 (`compiler/ai-compiler/mlir/`), top-level과 project 키만 다름.

---

## Phase 3: 새 트리 제안

### 3.1 트리 표현

ASCII tree로 사용자에게 제시:

```
neuron/ (제안된 새 구조)
├── 이론/
│   └── compiler/
│       ├── ai-compiler/
│       │   ├── mlir/
│       │   │   ├── overview.md            ← 기존 이론/compiler/mlir.md
│       │   │   ├── three-principles.md   ← 기존 temp/2026-05-15_mlir-three-principles-and-limits.md
│       │   │   └── dialect-system.md
│       │   └── ...
│       └── polyhedral/
│           ├── model.md
│           └── ...
├── 지식/
│   └── compiler/
│       ├── ai-compiler/
│       │   ├── mlir/
│       │   │   ├── practical-guide.md
│       │   │   └── pass-pattern.md
│       │   └── ...
│       └── ...
└── ...
```

### 3.2 매핑 표 (전체)

```markdown
| 현재 경로 | 새 경로 | type 변경 | 비고 |
|---------|---------|-----------|------|
| 이론/compiler/mlir.md | 이론/compiler/ai-compiler/mlir/overview.md | - | 깊이 추가 |
| 지식/compiler/mlir_practical_guide.md | 지식/compiler/ai-compiler/mlir/practical-guide.md | - | 파일명 영문화 |
| 지식/compiler/지식_가상_컴파일러와_실제_컴파일러의_역할_분리.md | 지식/compiler/role-separation-virtual-vs-real.md | - | 한국어→영문 |
| temp/2026-05-15_mlir-paper-overview.md | 이론/compiler/ai-compiler/mlir/paper-overview.md | draft→theory | temp 전이 |
| ... | ... | ... | ... |
```

매핑 표를 사용자에게 제시:
```
N개 문서 매핑입니다. 전체를 검토해주세요:

[표 출력 또는 별도 파일: temp/reorg-mapping-<date>.md]

수정 사항 있으면 다음 형식으로:
- 변경: <행번호> <새 경로>
- 보류: <행번호>
- 추가 클러스터: <설명>

또는 "전체 승인"으로 다음 단계 진행.
```

### 3.3 수정 반영 루프

사용자 피드백을 받아 매핑 갱신. 합의될 때까지 반복.

---

## Phase 4: 일괄 실행 (승인 후)

### 4.1 실행 순서

1. **신규 디렉토리 생성** (`mkdir -p`)
2. **파일 이동** (`git mv` 또는 `mv` — git repo면 git mv 권장으로 히스토리 보존)
3. **frontmatter `domain` 필드 갱신** (새 경로로)
4. **frontmatter `updated` 필드 갱신** (오늘)
5. **wikilink 갱신** — 모든 `[[old_name]]` → `[[new_name]]` (이름 바뀐 경우)
6. **related 필드 갱신** — 끊긴 wikilink 수정
7. **빈 구 디렉토리 제거**

### 4.2 wikilink 일괄 갱신 스크립트

```bash
# 이름 변경 매핑 파일 (예: temp/rename-map.txt 형식 "old\tnew" 행)
while IFS=$'\t' read -r OLD NEW; do
  grep -rl "\[\[$OLD\]\]" neuron/ | while read F; do
    sed -i "s|\[\[$OLD\]\]|\[\[$NEW\]\]|g" "$F"
  done
done < temp/rename-map.txt
```

(실제 실행 시 dry-run 먼저: `sed -n 's|...|...|p'`)

### 4.3 디렉토리 정리

```bash
# 빈 디렉토리 제거 (재귀)
find neuron/ -type d -empty -delete
```

---

## Phase 5: 검증

### 5.1 끊긴 wikilink 검사

```bash
# 모든 [[X]] 추출 → 실제 파일 존재 여부 확인
grep -roh '\[\[[^]]*\]\]' neuron/ | sort -u > /tmp/wikilinks.txt
# 각 X에 대해 파일 존재 확인 스크립트
```

### 5.2 frontmatter ↔ 경로 일치

```bash
# 각 .md 파일의 frontmatter `domain` 필드 추출 → 실제 경로와 비교
```

### 5.3 무손실 확인

```bash
# 백업과 새 구조의 파일 수 비교
find temp/neuron-snapshot-$DATE -name "*.md" | wc -l
find neuron/ -name "*.md" | wc -l
# 동일해야 함 (이동만, 삭제·생성 없음)
```

### 5.4 보고

```
재구축 완료 검증:

총 문서: N개 (백업과 동일 ✓)
끊긴 wikilink: K개  ← 사용자에 알림
frontmatter ↔ 경로 불일치: M개  ← 일괄 수정
신규 디렉토리: P개
제거된 빈 디렉토리: Q개
```

문제가 있으면 사용자에게 보고 후 수정. 심각하면 백업 복원:
```bash
rm -rf neuron/
cp -r temp/neuron-snapshot-$DATE/neuron neuron/
# 또는: git reset --hard neuron-pre-reorg-$DATE
```

---

## Phase 6: commit

검증 통과 시:

```bash
git add neuron/
git commit -m "neuron: tree reorganization on <date> — N files moved, M renamed

Triggered by: <사용자 요청>
Backup: temp/neuron-snapshot-<date>/ (또는 tag neuron-pre-reorg-<date>)
"
```

**push 절대 금지** — neuron/ 정책.

---

## Phase 7: 마무리 보고

```markdown
# ✅ Tree 재구축 완료

## 변경 요약
- 이동: N건
- 이름 변경: M건
- 깊이 변경: K건
- temp/ 전이: L건
- 빈 디렉토리 정리: P건

## 백업
- temp/neuron-snapshot-<date>/ (rm으로 정리 가능)
- git tag: neuron-pre-reorg-<date>

## 추후 권장
- index 문서(INDEX_*.md) 재검토
- 끊긴 wikilink K개 수동 확인
- 다음 재구축은 N개 문서 추가 후 또는 분기 단위
```

---

## 절대 하지 말 것

- ❌ 백업 없이 실행
- ❌ Phase 3 매핑 표 없이 바로 이동
- ❌ wikilink 갱신 생략 (이동만 해서 링크 깨뜨림)
- ❌ frontmatter `domain` 갱신 생략
- ❌ 어떤 문서든 삭제 (이동만, 삭제는 별도 organize-knowledge로)
- ❌ 백업과 결과 파일 수 다른 채로 commit (무손실 깨짐)
- ❌ neuron/ remote push
- ❌ 부분 작업으로 호출 (그건 organize-knowledge)
