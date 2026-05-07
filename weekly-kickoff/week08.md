---
marp: true
theme: rpg
paginate: true
title: 'Week 8 — AI 네이티브 워크플로우'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week 8

## AI 네이티브 워크플로우

2026-07-25 (토) · 미션 공개 + 주간 방향

---

# AI: 제가 다 했어요 (의심됨)

![w:500](../theme/assets/memes/w8.jpg)


---

# 지난 주 돌아보기 — Week 7 Redis

| 항목 | 결과 |
| --- | --- |
| **제출률** | {{N}}/{{M}} 명 |
| **잘된 점** | hit rate _수치_ 박은 학생 다수 |
| **아쉬운 점** | invalidation 전략 _근거_ 약함 |
| **이번 주 가져갈 것** | AI 와 _협업_ 하는 흔적을 _증명_ 하기 |

---

<!-- _class: quest -->

# 09-week8-ai-native

- **type**: `docs`
- **마감**: 2026-07-31 (금) `23:59`
- **검증**: PR → mission-guard CI → AI 리뷰
- **통과 조건**: 축 A 7 evidence + 축 B 옵션 ≥ 2 + 라이프사이클 단계 선택 근거

> "AI 가 _짠 코드_ 가 아니라, AI 와 _함께 짠 흔적_ 을 evidence 에."

---

# 비유 — AI = 새로 합류한 시니어

![w:280](../theme/assets/images/coding-team.jpg)

빠르고 박학다식. 하지만:
- 가끔 _자신감 있게 틀린 답_ (hallucination)
- _맥락_ 모르면 엉뚱한 코드
- _검증_ 없이 받으면 사고

---

# 이번 주 학습 목표

1. **축 A — 코딩 6 요소** evidence 7개
2. **축 B — 라이프사이클 단계** 옵션 ≥ 2 선택
3. **검증 루프** — AI 답 → 직접 실행 → 공식 문서 교차 → evidence

---

<!-- _class: lesson -->

## 축 A — 코딩 6 요소

| 요소 | 무엇 |
| --- | --- |
| Context Engineering | `CLAUDE.md` 헌법 작성 |
| Needle in Haystack | 큰 코드베이스에서 정확히 찾기 |
| 페목형제 | 페어·목적·형태·제약 4 축 프롬프트 |
| `claude.md` | 본인/팀 합의 박는 곳 |
| Slash Commands | 자주 하는 작업 명령화 |
| Hooks | 커밋/푸시 검증 자동 |

> 각 요소별 evidence 1개씩 = 6개 + 종합 1개.

---

<!-- _class: lesson -->

## 축 B — 라이프사이클 단계

```text
기획   — PRD.md + Jira MCP 티켓
코딩   — Claude Code 페어 프로그래밍
테스트 — Playwright MCP E2E
리뷰   — Claude Actions / CodeRabbit
운영   — Sentry MCP 모니터링
협업가속 — gh CLI / Sub-agents / claude-squad
```

이 중 **2 개 이상** 본인 사례로 evidence.

---

# 검증 루프 — AI 답을 _믿지 않기_

```text
1. AI 답 받기            (3초)
2. 본인 손으로 실행       (1분)
3. SQL/로그/응답 확인     (2분)
4. 의심 시 공식 문서 교차  (5분)
5. evidence 에 _차이_ 기록 (3분)
```

> 매 강의의 _이력서 카드_ 가 이 루프의 결과물.

---

# 함정 — AI 사용에서 흔한 실수

- ❌ AI 코드 _그대로_ 커밋 → ✅ 직접 실행 + 테스트 통과 후
- ❌ "이건 AI 가 줬어요" 는 답이 아님 → ✅ 본인이 _판단·검증_ 한 흔적
- ❌ hallucination 잡고 _안 기록_ → ✅ `evidence/failure-cases.md` 누적
- ❌ `CLAUDE.md` _빈_ 채로 시작 → ✅ 본인 도메인·규칙·금지 박기
- ❌ prompt 1 회 시도 → ✅ 페목형제 + Context Engineering 으로 다듬기

---

# 이번 주에 제출할 것

```
09-week8-ai-native/
├── report.md
└── evidence/
    ├── context-engineering.md
    ├── needle-in-haystack.md
    ├── pemok.md                  # 페목형제
    ├── claude-md-sample.md
    ├── slash-commands.md
    ├── hooks.md
    ├── lifecycle-*.md             # planning/testing/review/ops 중 2+
    └── failure-cases.md          # hallucination 잡힌 사례 누적
```

---

# 평가 기준 (5축)

| 축 | 가중 | 핵심 |
| --- | --- | --- |
| 요구사항 충족 | ★★ | 축 A 7 + 축 B 2 모두 |
| 구조 | ★ | evidence 폴더 정돈 |
| 기술 적용 | ★★ | 검증 루프 _실제_ 적용 |
| 검증 근거 | ★★ | hallucination 사례 1개+ |
| 설명력 | ★★★ | _AI 와 협업_ 본인 말로 |

> Week 8 는 _설명력_ 가중. AI 가 좋은 결과 줘도, 학생이 _검증 루프_ 안 적으면 3점 이하.

---

# 8주차 종료 — 팀 진입 점검

8주차 마감 후 다음 조건 충족 시 W9 팀 프로젝트 가동:

- 6 공통 필수 기능 _개념_ 이해 (W1~7 evidence 누적)
- 라이프사이클 단계 ≥ 2 흔적
- 환경 셀프체크 / 매주 PR 머지 누적

> 진입 가능 여부는 8주차 마감 후 운영진이 개별 안내.

---

# 운영 안내

- **제출 마감**: 2026-07-31 (금) `23:59`
- **토 15:00–16:30**: 격주 **강의** — AI Native 워크플로우 깊게
- **오피스아워**: 화·목 `21:00` `{cohort}-질문` 스레드
- **팀 매칭 발표**: 이번 주 종료 후

---

<!-- _class: end -->

# Q&A

```text
이번 주 = "AI 의 답을 _검증_ 하는 흔적"
다음 면접 = "AI 도구 어떻게 활용?" 답할 수 있게
```

> 오늘 15:00 — Event Sourcing 강의 (캐시 너머의 설계).
