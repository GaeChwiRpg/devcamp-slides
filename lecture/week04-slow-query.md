---
marp: true
theme: rpg
paginate: true
title: 'Week 4 강의 — 슬로우 쿼리 사례 5선'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week 4 강의

## 슬로우 쿼리 사례 5선

이게 왜 느릴까? 퀴즈 · 2026-06-20

---

<!-- _class: quest -->

# 왜 이 주제인가

- 운영 백엔드 개발자가 _가장 자주_ 받는 알림: "쿼리 느려요"
- 면접 단골: "이 쿼리 왜 느린지 분석해보세요"
- W3 이력서의 _수치_ 가 어디서 나오나 → 슬로우 쿼리 분석
- W4 미션 (인덱스) 보강 — 사례로 학습

> "느린 쿼리를 _고치는_ 사람보다 _찾는_ 사람이 더 귀하다."

---

# 오늘 다루는 것

- 사례 5 개 — 모두 실무에서 빈번
- 각 사례마다 _이게 왜?_ 30 초 추측
- EXPLAIN 보고 정답 확인
- 해결 방법 + 이력서 카드

> 5 개 사례 = 5 개 카드. 본인 evidence/interview-cards/ 에 누적.

---

# 사전 지식 체크 (1분)

| 질문 | □ |
| --- | --- |
| 슬로우 쿼리 정의 (시간) | □ |
| 슬로우 쿼리 로그가 무엇 | □ |
| EXPLAIN type 값 5 가지 | □ |
| 카디널리티 한 줄 정의 | □ |

---

<!-- _class: quest -->

# 사례 1 — 검색 800ms

```sql
SELECT * FROM post
WHERE title LIKE '%검색어%'
ORDER BY created DESC
LIMIT 20;
```

```text
post 테이블: 100만 row
title 에 인덱스 _있음_

⏱️  실측: 800ms
🤔 왜 느릴까?
```

---

# 사례 1 — 정답

```text
WHERE title LIKE '%검색어%'
              ↑
       앞에 와일드카드
```

→ 인덱스 _못 씀_ (B-Tree 는 _접두사_ 매칭만)

```text
✅ 해결:
1. LIKE '검색어%' (앞 와일드카드 제거)
2. 풀텍스트 인덱스 (FULLTEXT)
3. 검색 엔진 도입 (Elasticsearch)
```

---

<!-- _class: quest -->

# 사례 2 — 일별 통계 12초

```sql
SELECT YEAR(created), MONTH(created),
       COUNT(*)
FROM order
WHERE YEAR(created) = 2026
GROUP BY YEAR(created), MONTH(created);
```

```text
order: 500만 row
created 에 인덱스 _있음_

⏱️  실측: 12초
🤔 왜?
```

---

# 사례 2 — 정답

```text
WHERE YEAR(created) = 2026
       ↑
    함수로 가공
```

→ 인덱스 _못 씀_ (좌변에 함수)

```text
✅ 해결:
WHERE created >= '2026-01-01'
  AND created <  '2027-01-01'

→ 12초 → 0.3초
```

---

<!-- _class: quest -->

# 사례 3 — 마이페이지 2초

```sql
SELECT u.*,
       (SELECT COUNT(*) FROM order o
        WHERE o.user_id = u.id) order_cnt,
       (SELECT COUNT(*) FROM review r
        WHERE r.user_id = u.id) review_cnt
FROM user u
WHERE u.id = 5;
```

```text
🤔 user 1명 조회인데 _왜_ 2초?
```

---

# 사례 3 — 정답

```text
서브쿼리 2개가 _독립_ 으로 실행
→ 각각 풀스캔 또는 인덱스 스캔
```

```text
✅ 해결:
1. 서브쿼리를 JOIN 으로 변경
2. 또는 _카운터 테이블_ 캐시 (W7)
3. 또는 비동기 집계

핵심: 서브쿼리도 _쿼리_. EXPLAIN 으로 모두 확인.
```

---

<!-- _class: quest -->

# 사례 4 — 갑자기 느려진

```sql
SELECT * FROM post
WHERE status = 'PUBLISHED'
  AND user_id = 5
ORDER BY created DESC;
```

```text
어제까지 50ms.
오늘 갑자기 3초.
DB 변경 없음.
🤔 무엇이 바뀌었나?
```

---

# 사례 4 — 정답

```text
status='PUBLISHED' 의 카디널리티 _바뀜_

어제: 30% (적중)
오늘: 95% (대다수)
→ 옵티마이저가 _풀스캔_ 선택
```

```text
✅ 해결:
1. ANALYZE TABLE — 통계 갱신
2. 인덱스 _힌트_ 명시 (USE INDEX)
3. 복합 인덱스 (user_id, status, created)

교훈: _데이터 분포_ 가 옵티마이저 결정 좌우.
```

---

<!-- _class: quest -->

# 사례 5 — deep page

```sql
SELECT * FROM post
ORDER BY created DESC
LIMIT 100 OFFSET 50000;
```

```text
post: 100만 row
created 인덱스 _있음_

⏱️  page 1   = 10ms
⏱️  page 500 = 8초
🤔 왜?
```

---

# 사례 5 — 정답

```text
OFFSET 50000
→ DB 가 50,100 row 읽고 _50,000 버림_
→ 페이지 깊을수록 _더 느려짐_
```

```text
✅ 해결 — 커서 기반 페이지네이션:

WHERE created < '2026-01-01 12:00:00'  -- 마지막 row
ORDER BY created DESC
LIMIT 100;

→ 8초 → 10ms
```

---

# 5 사례 정리

| # | 패턴 | 핵심 |
| --- | --- | --- |
| 1 | LIKE 앞 와일드카드 | 풀텍스트 / 검색 엔진 |
| 2 | 좌변 함수 | 범위 조건으로 변환 |
| 3 | 서브쿼리 폭발 | JOIN 또는 캐시 |
| 4 | 카디널리티 변화 | ANALYZE + 인덱스 힌트 |
| 5 | OFFSET deep page | 커서 페이지네이션 |

> 면접에서 _이 5 개_ 짚을 수 있으면 +1 점.

---

# 도메인에서 — 슬로우 쿼리 자리

| 도메인 | 흔한 패턴 |
| --- | --- |
| 검색 | LIKE %% / FULLTEXT 미적용 |
| 통계·대시보드 | 좌변 함수 / 집계 서브쿼리 |
| 마이페이지 | 다중 서브쿼리 / N+1 |
| 관리자 | 페이지네이션 deep page |
| 신규 기능 | 카디널리티 변화 (운영 후 발견) |

> 같은 _5 가지 패턴_ 이 도메인 바뀌어도 반복됨.

---

# 이력서에서 — 슬로우 쿼리 카드

```text
[관리자 페이지 8초 → 10ms 개선]
P (문제) /admin/posts page=500 응답 8초 — 사용자 클레임
O (옵션) 캐시 / 인덱스 / 커서 페이지네이션
D (결정) 커서 페이지네이션 — DB 부하도 일정 (페이지 깊이 무관)
A (행동) created_id 복합 커서 + API 변경 + frontend 협업
R (결과) page 500 8초 → 10ms (-99%), DB CPU 60% → 5%
```

---

# 운영 도구 — 슬로우 쿼리 로그

```text
my.cnf 설정:
slow_query_log = 1
long_query_time = 1.0  # 1초 이상

→ 자동 누적 → 매일 점검
```

```text
✅ Percona pt-query-digest — 분석 자동화
✅ DataDog / NewRelic APM — UI 로 분석
✅ MySQL Workbench — 쿼리별 시각화
```

> 면접에서 _슬로우 쿼리 로그_ 언급하면 _운영 감각_ 있음 인상.

---

# AI 보조 — 잘 쓰는 법

- **잘하는 것**: EXPLAIN 결과 1차 해석, 인덱스 후보 추천
- **자주 hallucinate**: _카디널리티_ 추측, 옵티마이저 _예측_
- **검증 루프**:
  1. 슬로우 쿼리 로그 실제 추출
  2. AI 에 EXPLAIN + 데이터 분포 함께 전달
  3. 본인 환경에서 EXPLAIN 직접
  4. before/after 측정 → evidence

> AI 추천 인덱스가 _실제로_ 쓰이는지 EXPLAIN 으로 _직접_ 확인.

---

# 다음 단계 — 미션 연결

- W4 미션 `05-week4-index` 통과 조건 = before/after EXPLAIN + latency 비교
- 오늘 5 사례 중 _본인 코드와 비슷한_ 것 1 개 골라 evidence
- `latency-comparison.md` 표 형식

> 막히면 → `{cohort}-질문` 채널 + 오피스아워 (화·목 `21:00`)

---

<!-- _class: end -->

# Q&A

```text
이번 주 = "내 쿼리에 5 패턴 있는지 점검"
다음 면접 = "이 쿼리 왜 느릴까?" 답할 수 있게
```

> 다음 격주 강의(W6): **분산 추적의 세계**.
