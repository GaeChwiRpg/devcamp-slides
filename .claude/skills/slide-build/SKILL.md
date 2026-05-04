---
name: slide-build
description: Marp 슬라이드 (devcamp-slides) 작성·편집 시 자동 호출되는 가이드. 제목/코드/표 폭 검증, 톤 규칙, RPG 테마 사용법, 새 슬라이드 만드는 30분 워크플로우. 슬라이드 .md 편집 / "마프"/"marp"/"슬라이드"/"강의"/"발표" 키워드 / weekly-kickoff·lecture·offline 디렉토리 접근 시 트리거.
---

# slide-build — Marp 슬라이드 작성 가이드

이 스킬은 `GaeChwiRpg/devcamp-slides` 부트캠프 발표 슬라이드를 _작성·편집_ 할 때 호출된다. _DEVELOPER RPG_ 톤 + 빌드 검증 하네스 + 톤 규칙을 한 곳에서 보장.

## 언제 사용

- `weekly-kickoff/*.md`, `lecture/*.md`, `offline/*.md`, `templates/*.md` 편집·작성
- 새 주차 슬라이드 만들기 ("Week N kickoff 슬라이드 만들어줘")
- 발표 자료 / 슬라이드 수정 요청

## 절대 깨지면 안 되는 규칙 (빌드 차단)

`scripts/build.sh` 시작 시 자동 검증. CI 도 동일. 폭 초과 시 `exit 1` → 빌드 중단.

### 1. 제목 폭 (`scripts/check-titles.py`)
- **H1 ≤ 32 EAW** (한글 1자 = 2폭, 영문 1자 = 1폭)
- **H2 ≤ 48 EAW**
- **H3 ≤ 56 EAW**
- **`<!-- _class: quest -->` 슬라이드의 H1** 은 `::before "⚔ QUEST "` (8폭) 추가 → 본문 ≤ **24 EAW**

### 2. 코드/표 폭 (`scripts/check-content.py`)
- **일반 슬라이드 코드 블록** ≤ 70 EAW
- **`<!-- _class: lesson -->` 슬라이드 코드** ≤ 52 EAW (양분할 cell 폭 + 17px 폰트)
- **일반 표 cell** ≤ 60 EAW
- **lesson 표 cell** ≤ 42 EAW

### 빌드 + 검증 1회 명령
```bash
npm run build
# 또는 단독 검증
python3 scripts/check-titles.py && python3 scripts/check-content.py
```

폭 초과 시 메시지에 라인번호 + 폭 + 한도 + 내용이 나옴. 줄바꿈 또는 단축으로 해결.

## 절대 사용하지 않는 단어

- ❌ "진급 게이트" → ✅ "통과 조건" / "분기점" / "이번 주 목표"
- ❌ "라이브 데모" / "라이브 시연" → 발표에 라이브 데모 없음. _시스템 흐름 설명_ 형태로
- ❌ "특강" → ✅ "강의" (외부 초청 아님, 총괄 직접)
- ❌ "비전공자가 진짜로 백엔드 개발자가" 같은 표현 — 톤 너무 처져 보임

## Discord 채널 표기

실제 서버: `gaechwirpg` (ID `1486978301909270602`). 코호트별 카테고리.

- 질문 / 막힘 → `{cohort}-질문`
- PR / AI 리뷰 알림 → `{cohort}-리뷰`
- 매일 학습 로그 → `{cohort}-til`
- 자유 / 잡담 → `{cohort}-자유`
- 공식 공지 → `{cohort}-공지`
- 학습 블로그 → `{cohort}-blog`
- 팀 전용 → `{cohort}-team-NN`
- 졸업생 (코호트 무관) → `졸업생-라운지`
- 오피스아워 시간: 화·목 `21:00` → `{cohort}-질문` 채널 스레드

## 환경 / 미션 표기

- Java 버전: **JDK 21** (Spring Boot 3.3.5 매칭, JDK 17 아님)
- Spring Boot 3.3.x
- 학생 레포는 _이미 부트스트랩됨_ (`{cohort}-{username}`) — "fork + clone" / "새 프로젝트 생성" 표현 X. "본인 학생 레포의 `<missionId>/project/` 폴더에 코드 시작"

## 슬라이드 분류 (폴더 구조)

| 폴더 | 슬롯 | 발표자 | 분량 |
| --- | --- | --- | --- |
| `weekly-kickoff/` | 매주 토 14:00–15:00 미션 공개 | 총괄 | 15-25장 / 30-45분 |
| `lecture/` | 격주 토 15:00–16:30 강의 (W2/4/6/8) | 총괄 직접 | 30-40장 / 60-70분 |
| `offline/` | 1주차 OT (5/30) / 10주차 피날레 (8/8) | 총괄 | 25-30장 |
| `templates/` | 위 3종 표준 양식 (`_kickoff` / `_lecture` / `_offline`) | — | — |

학생 발표 (3·5·7·9주차 내부 발표) 는 Google Slides — 이 repo 안 다루지 않음.

## 강의 슬라이드 구조 (절충안 C)

매 격주 강의는 다음 흐름:

1. **표지** (cover class)
2. **왜 이 주제인가** (quest class)
3. **본문 강의 70%** — 미션 통과 조건 직결
4. **한 발 더 30%** — 실무 함정 / 다른 선택지 / hallucination
5. **도메인에서** — 같은 패턴이 다른 도메인에서 어떻게 보이는지 (5 사례 표)
6. **이력서에서** — P-O-D-A-R 카드 sample (학생 `evidence/interview-cards/<topic>.md` 누적용)
7. **다음 단계 — 미션 연결** (이번 주 evidence 어디에 박을지)
8. **Q&A** (end class)

## 디자인 톤 — DEVELOPER RPG

`/Users/hyunjoon.park/project/dev-camp/logo.png` 베이스. `theme/rpg.css` 가 SoT.

- 컬러: 딥 네이비 `#0d1138` + 골드 `#f4c84b` + 화이트
- 폰트: Galmuri11 (제목 픽셀, OFL) + Pretendard (본문)
- 메타포: 매주 = 퀘스트 / W10 = FINAL BOSS / 미션 = 통과 조건
- 슬라이드 layout class:
  - `<!-- _class: cover -->` — 표지 (로고 + 주차 배지)
  - `<!-- _class: quest -->` — 퀘스트 시작 (h1 에 `⚔ QUEST` prefix 자동)
  - `<!-- _class: lesson -->` — 본문 양분할 (좌: 텍스트, 우: 코드/그림)
  - `<!-- _class: boss -->` — FINAL BOSS (10주차 / 면접)
  - `<!-- _class: end -->` — 마무리 (Q&A, 다음 주 예고)

## 새 슬라이드 만드는 워크플로우 (30분)

1. **템플릿 복제**
   ```bash
   # 매주 14:00 슬롯
   cp templates/_kickoff-template.md weekly-kickoff/weekNN.md

   # 격주 강의 (W2/4/6/8)
   cp templates/_lecture-template.md lecture/weekNN-{topic}.md

   # 첫·마지막 오프라인
   cp templates/_offline-template.md offline/weekNN-ot.md
   ```

2. **placeholder 채우기** (`{{...}}`)
   - `mission_id` / `title` → `bootcamp-admin/src/lib/mission-catalog.ts`
   - 학습 목표 → `bootcamp-admin/docs/bootcamp/curriculum.md` 진급조건 그대로
   - evidence 체크리스트 → `devcamp-submission-sample/<missionId>/README.md`
   - 평가 기준 → `bootcamp-admin/docs/bootcamp/review-rubric.md`

3. **검증 + 빌드**
   ```bash
   npm run build
   ```
   - 폭 검증 자동 통과해야 PDF 생성됨
   - 폭 초과 시 메시지대로 단축

4. **푸시 → CI → Pages**
   ```bash
   git add weekly-kickoff/weekNN.md
   git commit -m "feat(slides): Week N kickoff"
   git push
   ```
   GitHub Actions 가 자동 빌드 → https://gaechwirpg.github.io/devcamp-slides/ 에 PDF 배포.

## 발표 노트

- `*-notes.md` 파일은 운영자 전용 — `dist/` 에서 자동 제거 (Pages 비공개)
- frontmatter 없이 일반 마크다운으로 작성 — Marp 가 무시

## 자주 막히는 곳

### 제목 폭 초과
- `# Part 3 — LAZY 기본 + N+1 해결` (29 EAW + quest prefix 8 = 37, 한도 32 초과)
- 해결: `# Part 3 — N+1 해결` (16 EAW + 8 = 24, 한도 24 통과)

### 코드 블록 폭 초과 (lesson 슬라이드)
- 한도 52 EAW. 한글 섞이면 빠르게 초과
- 해결: 변수명 짧게 (`postRepository` → `postRepo`), 주석 압축, 줄바꿈 추가

### 표 cell 폭 초과 (lesson)
- 한도 42 EAW
- 해결: cell 내용 짧게, 또는 표 자체를 lesson 양분할 _밖_ 으로 (h2 다음에 두면 grid-column: 1 / -1 적용 안 됨 — `<!-- _class: -->` 없는 일반 슬라이드로)

### lesson 인데 코드가 너무 김
- 그 슬라이드의 lesson class 제거 → 일반 슬라이드 (한도 70) 로
- 또는 코드 본질만 남기고 _상세는 다음 슬라이드_ 로 분리

## 참고

- 슬라이드 톤·디자인 SoT: `theme/rpg.css`
- 제목 폭 검증: `scripts/check-titles.py`
- 코드/표 폭 검증: `scripts/check-content.py`
- 빌드 스크립트: `scripts/build.sh`
- CI: `.github/workflows/build.yml`
- 운영 가이드 (행사 슬롯·발표자·도구): `bootcamp-admin/docs/bootcamp/presentations.md`
