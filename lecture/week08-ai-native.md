---
marp: true
theme: rpg
paginate: true
title: 'Week 8 강의 — AI Native'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week 8 강의

## AI Native — 검증 루프 + Context Engineering

Week 8 · 격주 강의 · 2026-07-18

---

<!-- _class: quest -->

# 왜 AI Native 인가

- 2026 년 백엔드 개발자 = AI 와 _협업하는_ 개발자
- "AI 가 잘 짜준다" ≠ "본인이 잘한다"
- 면접 단골 (AI 도구 어떻게 활용?)
- Week 8 통과 조건 = 검증 루프 흔적 7 evidence

> "AI 가 _쓴 코드_ 가 아니라, AI 와 _협업한 흔적_."

---

# 오늘 다루는 것

1. 비유 — 새로 합류한 시니어
2. Context Engineering = `CLAUDE.md`
3. 페목형제 — 4 축 프롬프트
4. Hooks / Slash Commands / Sub-agents
5. 검증 루프 + hallucination 잡기
6. 도메인에서 + 이력서에서

---

# 사전 지식 체크 (1분)

| 질문 | □ |
| --- | --- |
| Context Engineering 한 줄 | □ |
| `CLAUDE.md` 가 무엇 | □ |
| hallucination 잡은 사례 1 개 | □ |
| Slash Command vs Hook 차이 | □ |

---

<!-- _class: quest -->

# Part 1 — 비유

AI = _새로 합류한 시니어 개발자_.

- 빠르고 박학다식
- 가끔 _자신감 있게 틀린 답_ 을 줌
- _맥락_ 모르면 엉뚱한 코드
- 본인 _코드 리뷰_ 받아야 머지

> 시니어 PR 도 리뷰하잖아? AI 답도 똑같다.

---

# AI 협업 — 5 가지 사실

```text
1. AI 는 _빠름_, 하지만 _정확하지 않음_
2. AI 는 _맥락_ 을 줘야 좋은 답
3. AI 는 _공식 문서_ 를 본인보다 _못_ 봤을 수도
4. AI 답 _그대로_ 머지하면 _본인 책임_
5. _검증 루프_ 가 본인 실력의 차별화
```

> 면접에서 _"AI 활용"_ 답할 때 이 5 가지가 근거.

---

<!-- _class: quest -->

# Part 2 — Context

AI 답이 _좋아지는_ 가장 큰 레버.

- 빈 프롬프트 → AI 가 _상상_ 으로 답
- 맥락 박힘 → AI 가 _제약_ 안에서 답
- 가장 강력한 맥락 = `CLAUDE.md`

---

<!-- _class: lesson -->

## `CLAUDE.md` — 본인/팀 헌법

```markdown
# Project Rules

## 도메인
- 게시판 + 댓글
- 사용자는 회원만 작성 가능

## 코딩 규칙
- 응답 DTO 는 record
- camelCase JSON
- @Transactional 은 Service 만

## 금지
- console.log 커밋 금지
- API 응답에 Entity 직접 노출 금지
```

```text
AI 가 매 프롬프트마다 _이걸 먼저_ 읽고 답.
빈 슬레이트가 아니라 _합의된 맥락_ 위에서.
```

---

# 페목형제 — 4 축 프롬프트

```text
페어 — 누가 짝인가 (시니어 / 신입 / 스타일)
목적 — 무엇을 하려나 (구현 / 리팩토링 / 디버그)
형태 — 어떤 결과 (코드 / 설명 / 비교)
제약 — 무엇은 안 됨 (라이브러리 / 패턴)
```

```text
프롬프트 1 줄 → 답변 1 줄짜리.
페목형제 4 줄 → 답변 _쓸 수 있는_ 코드.
```

---

<!-- _class: quest -->

# Part 3 — 자동화 도구

매 작업마다 _수동_ 이 아닌 _도구_ 로.

- **Slash Commands** — 자주 하는 작업 명령화
- **Hooks** — 커밋·푸시 시점 검증 자동
- **Sub-agents** — 병렬 / 독립 검증

---

<!-- _class: lesson -->

## Slash Commands

```bash
# .claude/commands/test-week.md
/test-week 4

# 자동 실행:
# 1. 05-week4-index/project 빌드
# 2. 테스트 실행
# 3. evidence/* 검증
# 4. PR 본문 미리보기
```

```text
매번 같은 명령 = 슬래시 1 개로
실수 줄고, 시간 절약, 일관성 확보
```

---

<!-- _class: lesson -->

## Hooks

```yaml
# .claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit",
      "hooks": [{
        "type": "command",
        "command": "npm run lint"
      }]
    }]
  }
}
```

```text
파일 편집 후 _자동_ lint
잊어버려도 hook 이 잡아줌
```

---

# Sub-agents — 병렬 / 독립 검증

```text
main agent     → "이 PR 머지 가능?"
  ├ sub: 보안 리뷰  (독립 컨텍스트)
  ├ sub: 성능 리뷰
  └ sub: 테스트 커버리지

→ 3 개 결과 종합 후 결정
```

> 본인 코드 + AI 코드 모두 _다른 시각_ 으로 검증.

---

<!-- _class: quest -->

# Part 4 — 검증 루프

AI 답을 _믿지 않는_ 5 단계.

```text
1. AI 답 받기            (3초)
2. 본인 손으로 실행       (1분)
3. SQL/로그/응답 확인     (2분)
4. 의심 시 공식 문서 교차 (5분)
5. evidence 에 _차이_ 기록 (3분)
```

> 매 강의의 _이력서 카드_ 가 이 루프의 결과물.

---

# Hallucination — 흔한 케이스

```text
❌ 존재하지 않는 메서드 호출
❌ 라이브러리 버전 mismatch
❌ JPA 어노테이션 위치 잘못
❌ Spring Boot 3.x 인데 javax.* import
❌ Lombok 의 @Builder 와 @Entity 충돌 무시
```

> 잡힌 사례 1 개 = `evidence/failure-cases.md` 누적. Week 10 면접 답변에 _직접_ 사용.

---

# 도메인에서 — AI 협업 자리

| 도메인 | AI 협업 패턴 |
| --- | --- |
| 새 도메인 | PRD → AI 가 Entity 1 차안 |
| 디버그 | 스택 트레이스 → AI 추론 후 본인 검증 |
| 리팩토링 | AI 가 패턴 추천 → 본인 컨텍스트 적용 |
| 테스트 | E2E 시나리오 작성 |
| 문서 | API 명세 자동 생성 |

> AI 협업 = _혼자 못 하던 것_ 을 같이.

---

# 이력서에서 — AI Native 카드

```text
[AI 협업으로 N+1 발견 + 개선 1.5h → 30m]
P (문제) Week 9 팀 PR 에 N+1 의심, 직접 분석 1.5h 예상
O (옵션) 직접 분석 / AI 협업 / 시니어 페어
D (결정) AI 협업 + 검증 루프 — 검증 흔적 evidence 가능
A (행동) Claude 에 프롬프트, 직접 EXPLAIN, hallucination 1 건 잡음
R (결과) 분석 30m 단축, evidence/failure-cases 1 건 누적
```

---

# 다음 단계 — 미션 연결

- 미션 `09-week8-ai-native` 통과 조건 = 축 A 7 + 축 B 2 + hallucination 1+
- evidence: `context-engineering.md` / `pemok.md` / `slash-commands.md` / `hooks.md` / `failure-cases.md`
- Week 9 팀 프로젝트 = 4 명이 _다 같이_ AI Native 적용

---

<!-- _class: end -->

# Q&A

```text
이번 주 = "AI 답 → 검증 루프 → evidence"
다음 면접 = "AI 도구 어떻게 활용?" 답할 수 있게
```

> 다음 주: **Week 9 — 팀 프로젝트** (격주 강의 끝, 마지막 학생 발표).
