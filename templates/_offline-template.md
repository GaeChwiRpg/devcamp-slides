<!--
TEMPLATE: 첫·마지막 오프라인 모임 (20-30장)
- 1주차 OT (5/30): mode = OT — 비전 / 10주 RPG 맵 / 팀 매칭 / 시작 신호
- 10주차 피날레 (8/8): mode = FINALE — 회고 / 팀 데모 / 면접 답변 정렬 / 수료

사용법:
  cp templates/_offline-template.md offline/week01-ot.md
  cp templates/_offline-template.md offline/week10-finale.md
  → 한쪽 모드를 선택해서 다른 쪽 슬라이드는 삭제

점심 모임 분량 기준 60-90분, 슬라이드 25-30장.
-->

---
marp: true
theme: rpg
paginate: true
title: '{{Week N · OT 또는 Finale}}'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# {{타이틀}}

## {{서브타이틀}}

{{2026-MM-DD}} · 오프라인 점심 모임

---

# 오늘의 흐름

1. {{블록 1}}
2. {{블록 2}}
3. {{블록 3}}
4. 네트워킹 + Q&A

---

<!-- =======================================
     === MODE: OT (1주차, 5/30) =========
     ======================================= -->

<!-- _class: quest -->

# 왜 이 부트캠프인가

- _말로 답할 수 있는_ 백엔드 코드 — 면접에서 본인 입으로
- 책 7주차 베이스 + AI Native 4 요소
- 검증 루프 + 팀 라이프사이클 5단계 = 면접에서 _말할 수 있는_ 결과물

> "이 10주가 끝나면, 본인 입으로 본인 코드를 설명할 수 있다."

---

# 10-Week RPG Map

![w:900](../theme/assets/logo.png)

| W1 | W2 | W3 | W4 | W5 |
| --- | --- | --- | --- | --- |
| Spring Boot | JPA | 이력서 | 인덱스 | 동시성 |

| W6 | W7 | W8 | W9 | W10 |
| --- | --- | --- | --- | --- |
| 프로파일링 | Redis | AI Native | 팀 프로젝트 | **FINAL BOSS** |

---

# 6 공통 필수 기능

- 권한 / 인가
- 트랜잭션 / 동시성
- 검색 / 인덱스
- 캐시 (Redis)
- 비동기 / 이벤트
- AI 보조 기능

> 모든 팀 프로젝트가 6 영역을 _최소 1번씩_ 커버.

---

# 라이프사이클 5단계

| 단계 | 산출물 |
| --- | --- |
| 기획 | `PRD.md` + Jira 티켓 |
| 코딩 | PR + 코드 + 테스트 |
| 테스트 | E2E (Playwright MCP) |
| 리뷰 | Claude Actions / CodeRabbit |
| 운영 | Sentry MCP / `MONITORING.md` |

---

# 평가·통과 조건

- 매주 미션 mission-guard CI green
- AI 리뷰 평균 **3점 이상** (5축 — review-rubric.md)
- 4주차 종료 시 누적 평균 점검
- 8주차 종료 시 팀 프로젝트 진입 조건 점검

---

# 팀 매칭 룰

- 4명 팀 기본
- 기술 영역 4종 × 라이프사이클 5단계 매트릭스로 분담
- `week9-team-role-split.md` sample 그대로 따라가도 OK
- 팀별 1개 레포 (`{cohort}-team-NN`) 자동 부트스트랩

---

# 제출 흐름

- `submit/<mission_id>` 브랜치 push
- mission-guard CI 가 형식 + 내용 검증
- AI 리뷰가 5축 점수 + 한국어 피드백
- `{cohort}-리뷰` 채널 알림 + `latest_score` DB 업데이트

> sample repo `GaeChwiRpg/devcamp-submission-sample` 의 PR 들을 _참고_ — 같은 형식.

---

# AI Native 4 요소

- **Context Engineering** — `CLAUDE.md` 헌법
- **Slash Commands** — 자주 하는 작업 자동화
- **Hooks** — 커밋/푸시 단계에 검증
- **Sub-agents** — 병렬 작업 / 검증

> 매주 미션마다 _AI 보조 흔적_ 을 evidence 에 누적.

---

# 1주차 첫 미션 공개

- **mission_id**: `02-week1-spring-boot`
- **마감**: {{2026-06-05 23:59}}
- **검증**: mission-guard + AI 리뷰
- **진급**: 점수 ≥3.0 권장

> 토 14:00-15:00 슬롯에서 상세 안내.

---

<!-- =======================================
     === MODE: FINALE (10주차, 8/8) ========
     ======================================= -->

<!-- _class: boss -->

# FINAL BOSS DEFEATED

## 10 Weeks of Backend Mastery

{{N}}명 졸업 / {{M}}개 팀 / {{K}}개 머지된 PR

---

# 10주 클리어 마크

| W1 ✓ | W2 ✓ | W3 ✓ | W4 ✓ | W5 ✓ |
| --- | --- | --- | --- | --- |
| Spring Boot | JPA | 이력서 | 인덱스 | 동시성 |

| W6 ✓ | W7 ✓ | W8 ✓ | W9 ✓ | W10 ✓ |
| --- | --- | --- | --- | --- |
| 프로파일링 | Redis | AI Native | 팀 PR | **클리어** |

---

# 개인 성장 지표

- 미션 통과: 평균 {{X}}/10
- AI 리뷰 점수: 1주차 평균 {{a}}점 → 10주차 평균 {{b}}점
- 팀 기여도: 라이프사이클 단계 1개 + 기술 영역 1개

> 본인 PR 모음이 그대로 _포트폴리오_.

---

# 팀 프로젝트 데모 (각 5분)

- 팀 1: {{팀명}} — {{한 줄 도메인}}
- 팀 2: {{팀명}} — {{한 줄}}
- 팀 3: {{팀명}} — {{한 줄}}

> 각 팀 5분 데모. SLIDE-OUTLINE.md 12장 양식.

---

# 회고 — 10주 학습 여정

- 5주차 동시성 구간 살아남기 → ?
- 8주차 AI Native 첫 도입 → ?
- 9주차 팀 프로젝트 → ?

> 본인 입으로 본인 답.

---

# 면접 답변 공식

**P-O-D-A-R**: Problem · Options · Decision · Action · Result

**A-B-C**: 결론 → 근거(비교) → 본인 경험

> 매주 evidence 에 박은 _숫자_ 가 답변의 근거. Week 10 책 베이스.

---

# 다음 단계

- 본인 GitHub 프로필에 PR 모음 고정
- 이력서: `04-week3-backend-resume` 의 정량 표현 그대로
- AI Native 흔적: `prompt-log.md` + hallucination 잡힌 사례 evidence

---

<!-- _class: end -->

# 수료 인증

축하합니다 — 다음 시즌에서 만나요.

> Press Continue.
