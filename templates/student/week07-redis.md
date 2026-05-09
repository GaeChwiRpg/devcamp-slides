<!--
TEMPLATE: Week 7 학생 내부 발표 — Redis 캐시
운영: 토 15:00–16:30, 3분 발표 + 2분 피드백, 팀별 1명 로테이션
제출: 금 18:00 까지 `{cohort}-리뷰` 채널에 본인 사본 링크

작성 흐름 (15분):
  1. W7 미션에서 _캐시 적용한 엔드포인트 1개_ 고르기
  2. {{...}} placeholder 채우기 (hit rate, latency 수치 필수)
  3. 빌드 또는 Google Slides 로 변환
  4. 사본 링크 채널 게시
-->

---
marp: true
theme: rpg
paginate: true
title: 'Week 7 학생 발표 — Redis 캐시'
---

<!-- _class: cover -->
<!-- _paginate: false -->

# Redis — hit rate + latency 검증

## {{본인 이름}}

Week 7 · 2026-07-18 (토) · {{팀명}}

---

# 캐시 적용한 엔드포인트 1개 ⚡

**미션**: `08-week7-redis-cache`
**PR**: [{{PR 제목}}]({{PR URL}})

```text
[엔드포인트]
{{GET /posts/popular — 인기 게시글 목록}}

[캐시 키]
{{posts:popular:{date} — 1일 단위}}

[TTL / 정책]
{{TTL 60s · LRU · cache-aside}}
```

> 어디에 _왜_ 캐시 — 한 줄 명확히.

---

# Before / After 수치 📊

```text
[Before — 캐시 없음]
p50 latency  {{120ms}}
p99 latency  {{480ms}}
DB QPS       {{800}}

[After — Redis 캐시]
p50 latency  {{8ms}}      ({{-93%}})
p99 latency  {{45ms}}     ({{-90%}})
DB QPS       {{42}}       ({{-95%}})
hit rate     {{94.2%}}

evidence/cache-hit-rate-report.md
```

> 수치 _4종_ (latency × 2, QPS, hit rate) — 캐시 효과 _증명_.

---

# 정책 결정 — TTL / 무효화 🧠

```text
[고려]
1. TTL 만 — 단순, 짧은 stale 허용
2. write-through — 쓰기 시 캐시 갱신
3. cache-aside + 이벤트 무효화 — 정확

[선택]
{{1줄 — 예: TTL 60s + 글 작성 시 invalidate}}

[근거]
{{1줄 — 예: 인기 글 변동 분 단위 → 60s OK, 글 작성은 즉시 반영}}
```

> 정책 _근거_ = 도메인 이해.

---

# 함정 — Cache Stampede / 일관성 ⚠️

```text
[발견]
{{TTL 만료 직후 동시 N요청 → DB 부하 spike 관찰}}

[대응]
{{1줄 — 예: 낙관적 락 갱신 + jittered TTL}}

[교훈]
{{1줄 — 예: 캐시는 _빨라지는 것_ 아니라 _깨지면 더 위험_}}
```

> _안 깨진 척_ 말고 _깨진 케이스_ 보여주기.

---

# P-O-D-A-R 카드 📇

```text
P (문제) /posts/popular p99 480ms, DB QPS 800
O (옵션) 인덱스 / 캐시 / 비동기 / read replica
D (결정) Redis cache-aside (TTL 60s + 이벤트 무효화)
A (행동) Spring @Cacheable + 무효화 이벤트 리스너
R (결과) p99 45ms (-90%), hit rate 94%, DB QPS -95%
```

> 면접에서 _그대로 말하기_ 좋도록.

---

<!-- _class: end -->

# 피드백 받기 ❓

**잘한 점 1줄 / 개선 1줄** 자유롭게 — 비판적이지만 _격려 톤_.

> 다음 주: Week 8 AI 네이티브.
