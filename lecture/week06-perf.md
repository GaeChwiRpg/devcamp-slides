---
marp: true
theme: rpg
paginate: true
title: 'Week 6 강의 — 프로파일링'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week 6 강의

## 프로파일링 / 측정 기반 최적화

Week 6 · 격주 강의 · 2026-07-04

---

<!-- _class: quest -->

# 왜 프로파일링 인가

- "느려요" 만으론 _고칠 수 없다_
- _어디가_ 느린지 _수치_ 로 답해야 시작
- 면접 단골 (서버 성능 어떻게 개선?)
- Week 6 통과 조건 = 핫스팟 1+ 개선 + 우선순위 근거

> "추측 금지, 측정만 신뢰."

---

# 오늘 다루는 것

1. 비유 — 건강검진
2. CPU / 메모리 / IO / 락 — 무엇을 보나
3. flamegraph 읽는 법 (3 분)
4. 임팩트 × 노력 우선순위
5. 도메인에서 + 이력서에서

---

# 사전 지식 체크 (1분)

| 질문 | □ |
| --- | --- |
| 프로파일링 한 줄 정의 | □ |
| flamegraph 가 무엇 | □ |
| 핫스팟 vs 콜드스팟 | □ |
| p95 / p99 의미 | □ |

---

<!-- _class: quest -->

# Part 1 — 비유부터

몸 어디가 안 좋다 → _감_ 으로 약 안 먹음.

- **혈액 검사** = CPU 프로파일러
- **X-ray** = 메모리 / heap dump
- **심전도** = 실시간 latency
- **MRI** = 깊은 분산 추적

> 의사 = 본인. 환자 = 본인 코드.

---

# 무엇을 측정하나

```text
🔥 CPU       — 어떤 메서드가 가장 오래 도나
💧 메모리    — GC 빈도, heap 사용량, leak
🚪 IO        — DB / 디스크 / 네트워크 대기
🎯 락 경합   — 동시성 대기 시간
📊 처리량    — RPS, throughput
⏱️  latency  — 평균, p95, p99
```

> 보통은 _CPU 부터_. CPU 핫스팟 1 개가 latency 70% 차지하는 경우 흔함.

---

<!-- _class: quest -->

# Part 2 — flamegraph

```text
█████████████████████████████  HTTP handler
████████████████████  └─ Service.findAll()
██████████████        └─ JPA query
████████              └─ N+1 추가 쿼리   ← 핫스팟!
██████                └─ JSON 직렬화
```

가로 = 시간 비율. 가장 _넓은_ 막대 = 가장 오래 걸린 함수.

---

# flamegraph 읽는 법 — 3 단계

1. **위 → 아래**: 호출 깊이
2. **왼쪽 → 오른쪽**: 시간 순서 (정확하지 않음)
3. **막대 폭**: 그 함수가 _차지한 시간_

> 가장 _굵은_ 막대 1 개 짚어서 _그 함수_ 부터 본다.

---

# 측정 도구 — 본인 선택

| 도구 | 장점 | 단점 |
| --- | --- | --- |
| async-profiler | 빠름, flamegraph | CLI |
| VisualVM | GUI 무료 | 무거움 |
| JFR | JVM 내장, 가벼움 | 분석 별도 |
| JProfiler | 강력 | 유료 |

> sample = async-profiler. 본인이 다른 거 골라도 OK.

---

<!-- _class: lesson -->

## async-profiler 사용

```bash
# 다운로드
wget .../async-profiler.tar.gz

# CPU 프로파일 30초
./profiler.sh -d 30 -f /tmp/profile.html <PID>

# heap (메모리)
./profiler.sh -d 30 -e alloc \
  -f /tmp/heap.html <PID>
```

```text
결과 = .html flamegraph
브라우저로 열어서 가장 굵은 막대 클릭.
```

---

<!-- _class: lesson -->

## 핫스팟 — 무엇을 고치나

| 핫스팟 | 흔한 원인 | 개선 |
| --- | --- | --- |
| JPA 쿼리 | N+1, fetch join | W2 강의 |
| JSON 직렬화 | 중복 변환 | DTO 단순화 |
| 정규식 매칭 | 매번 컴파일 | static |
| 로깅 | 동기 / 잦은 IO | 비동기 |
| 외부 API | 동기 + 직렬 | 비동기 + 병렬 |

> 9 시 5 분에 들어온 _임팩트 큰 1 개_ 부터.

---

<!-- _class: quest -->

# Part 3 — 우선순위

핫스팟 5 개 잡았다 — 다 고칠 시간 없음.

| | 적은 노력 | 큰 노력 |
| --- | --- | --- |
| **큰 임팩트** | ⭐ 먼저! | 좋지만 |
| **작은 임팩트** | 스킵 | 나중 |

> _임팩트 큰 1 개_ + _노력 적은 1 개_ = 본인 PR 의 핵심.

---

# 함정 — 흔한 실수

- ❌ "느려요" 보고서 → ✅ "p99 1.2s, 평균 600ms"
- ❌ 감으로 최적화 → ✅ flamegraph _증거_ 후
- ❌ 5 개 다 고치기 → ✅ _임팩트 큰 1 개_
- ❌ 고친 후 _재측정 안 함_ → ✅ before/after 모두
- ❌ 프로덕션 _live_ 에 강한 프로파일러 → ✅ 샘플링 모드

---

# 도메인에서 — 프로파일링 자리

| 도메인 | 핫스팟 패턴 |
| --- | --- |
| API 응답 지연 | JPA N+1 / JSON 직렬화 |
| 배치 잡 | 메모리 누수 / GC |
| 결제 / 외부 API | 동기 호출 / 타임아웃 |
| 검색 | 정규식 / 인덱스 미적중 |
| 알림 발송 | 직렬 처리 / 락 경합 |

> 같은 _flamegraph 읽기_ 가 모든 도메인에 통한다.

---

# 이력서에서 — 프로파일링 카드

```text
[API 응답 p99 1.2s → 180ms 개선]
P (문제) /posts p99 1.2s — async-profiler 50%가 N+1
O (옵션) fetch join / @EntityGraph / batch fetch
D (결정) @EntityGraph + paging — 컬렉션 fetch 메모리 폭발 회피
A (행동) PostRepository 메서드 추가, JFR 재측정
R (결과) p99 1.2s → 180ms (-85%), CPU 30% → 8%
```

---

# AI 보조 — 잘 쓰는 법

- **잘하는 것**: flamegraph 핵심 함수 해석, 개선 후보 추천
- **자주 hallucinate**: 측정 _수치_ 추측, 도구 옵션 잘못 알려줌
- **검증 루프**:
  1. AI 답 받기
  2. 본인 환경에서 _직접_ 프로파일러 실행
  3. 실측 데이터 비교
  4. 개선 후 _재측정_ 으로 효과 확인

---

# 다음 단계 — 미션 연결

- 미션 `07-week6-profiling` 통과 조건 = 핫스팟 1+ 개선 + 우선순위 근거
- evidence: `profile-flamegraph.html` + `bottlenecks.md` + `before-after-table.md`
- 본인 코드 1 개 골라서 _임팩트 큰 1 개_ 만 잡기

---

<!-- _class: end -->

# Q&A

```text
이번 주 = "내 코드 어디가 느린지 _그림_ 으로"
다음 면접 = "성능 어떻게 개선?" 답할 수 있게
```

> 다음 격주 강의(Week 8): **AI Native — 검증 루프**.
