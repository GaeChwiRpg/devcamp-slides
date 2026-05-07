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

운영급 함정 · 2026-06-27

---

# 왜?! 도대체 왜!

![w:500](../theme/assets/memes/w4-lecture.jpg)


---

<!-- _class: quest -->

# 왜 이 주제인가

![w:240](../theme/assets/images/turtle.jpg)

- 운영 백엔드가 _가장 자주_ 받는 알림: "쿼리 느려요"
- 면접 단골: "이 쿼리 왜 느린지?"
- 5 가지 운영급 함정

> "느린 쿼리를 _고치는_ 사람보다 _찾는_ 사람이 더 귀하다."

---

# 오늘 다루는 것

- 운영급 사례 5 개 — 학생도 본 적 있을 패턴
- 각 사례 _이게 왜?_ 30 초 추측
- EXPLAIN + 운영 도구로 정답 확인
- 해결 + 이력서 카드

> 5 개 = 5 개 카드. `evidence/interview-cards/` 누적.

---

# 시작 전 — 용어 카드

| 용어 | 한 줄 정의 |
| --- | --- |
| **슬로우 쿼리** | 임계 시간(보통 1초+) 넘는 쿼리 |
| **슬로우 쿼리 로그** | DB 가 자동으로 남기는 느린 쿼리 모음 |
| **EXPLAIN** | 쿼리 _실행 전_ 옵티마이저 계획 보기 |
| **카디널리티** | 컬럼 값의 _다양성_ (낮으면 인덱스 효과 X) |
| **옵티마이저** | DB 가 쿼리 _실행 계획_ 결정하는 두뇌 |

> 모르는 단어 나오면 _이 표_ 다시.

---

<!-- _class: quest -->

# 사례 1 — deep page 8 초

```sql
SELECT * FROM order
ORDER BY created DESC
LIMIT 100 OFFSET 50000;
```

```text
order: 100만 row
created 인덱스 _있음_

⏱️  page 1   = 10ms
⏱️  page 500 = 8 초
🤔 왜 deep page 만 느릴까?
```

---

# 사례 1 — 정답 + 실무 패턴

```text
OFFSET 50000
→ DB 가 50,100 row 읽고 _50,000 버림_
→ 페이지 깊을수록 _더 느려짐_
```

```text
✅ 커서 기반 페이지네이션:
WHERE created < '2026-01-01 12:00:00'
ORDER BY created DESC
LIMIT 100;

→ 8 초 → 10ms (페이지 깊이 무관)
```

> 페이스북·인스타 타임라인이 _커서_ 인 이유.

---

<!-- _class: quest -->

# 사례 2 — 갑자기 느려짐

```sql
SELECT * FROM post
WHERE status = 'PUBLISHED'
  AND user_id = 5
ORDER BY created DESC;
```

```text
어제까지: 50ms
오늘:    3 초
DB 변경 없음. 코드 변경 없음.
🤔 무엇이 바뀌었나?
```

---

# 사례 2 — 정답

```text
status='PUBLISHED' 카디널리티 _바뀜_
어제: 30% (적중) → 오늘: 95% (대다수)
→ 옵티마이저가 _풀스캔_ 선택
```

```text
✅ ANALYZE TABLE post (통계 갱신)
✅ 복합 인덱스 (user_id, status, created)
✅ USE INDEX 힌트 (마지막 수단)
```

> _데이터 분포_ 가 옵티마이저를 좌우.

---

<!-- _class: quest -->

# 사례 3 — 평균만 8초

```sql
-- 단일 호출 측정: 80ms ✓
SELECT * FROM product WHERE id = 5;
```

```text
APM 평균:           8 초
슬로우 쿼리 로그:    이 쿼리 _다수_ 보임
DB CPU:             20%
🤔 단일은 빠른데 _평균_ 은 왜?
```

---

# 사례 3 — 정답: 락 대기

```java
@Transactional
public void bigBatch() {
  product.findById(5);  // row 락 잡음
  externalApi.call();   // 30 초 대기 (!)
  product.save();
}
// → 그 사이 같은 row 조회·수정 _대기_
```

```text
✅ 트랜잭션 _짧게_ — 외부 호출은 Tx 밖
✅ innodb_lock_wait + 슬로우 쿼리 같이
```

---

<!-- _class: quest -->

# 사례 4 — TEXT 컬럼 함정

```sql
SELECT * FROM post WHERE id = 5;
```

```text
어제까지: 5ms
오늘:    150ms

변경: post 에 content_long (TEXT) 컬럼 추가
🤔 인덱스로 가져오는 1 row 인데 30 배 느림?
```

---

# 사례 4 — 정답: SELECT *

```text
TEXT/BLOB 컬럼은 _별도 페이지_ 에 저장
→ id 로 row 찾고도 _TEXT 페이지 IO_ 추가
→ 1 row 인데 _IO 폭발_

게다가 네트워크로 100KB 전송 → 클라 메모리 ↑
```

```text
✅ SELECT id, title, summary  (필요한 컬럼만)
✅ TEXT 는 _별도 테이블_ (PostBody 분리)
✅ 큰 컬럼은 _요청 시_ 만 fetch (lazy column)
```

> "백엔드는 `SELECT *` 안 쓴다." — 면접 답변.

---

<!-- _class: quest -->

# 사례 5 — 인덱스 적중인데

```sql
SELECT * FROM order o
JOIN user u ON o.user_id = u.id
WHERE o.status = 'PENDING'
  AND u.tier = 'VIP';
```

```text
order, user 모두 인덱스 _많음_
EXPLAIN 결과: 모든 컬럼 인덱스 적중
⏱️  실측: 4 초
🤔 인덱스가 다 적중인데 왜 느릴까?
```

---

# 사례 5 — 정답: JOIN 순서

```text
✅ 좋은 순서: user(VIP 100) → order JOIN
   → 100 × lookup = 빠름

❌ 잘못 고른 순서: order(50만) → user JOIN
   → 50만 × lookup = 느림
```

```text
✅ ANALYZE TABLE (통계 정확)
✅ STRAIGHT_JOIN 힌트 (마지막)
```

---

# 5 사례 정리

| # | 사례 | 핵심 |
| --- | --- | --- |
| 1 | deep page 8 초 | 커서 페이지네이션 |
| 2 | 갑자기 느려진 쿼리 | 통계 + 카디널리티 |
| 3 | 단일 빠른데 평균 느림 | 트랜잭션 길이·락 대기 |
| 4 | TEXT 추가 후 30배 | SELECT * 안 쓰기 |
| 5 | 인덱스 적중인데 느림 | JOIN 순서·통계 |

> 면접에서 _이 5 개 패턴_ 짚을 수 있으면 _운영 감각_.

---

# 운영 도구 — 슬로우 쿼리 로그

```ini
# my.cnf
slow_query_log = 1
long_query_time = 1.0       # 1 초 이상
log_queries_not_using_indexes = 1
```

```text
✅ Percona pt-query-digest    — 자동 분석
✅ DataDog / NewRelic APM     — UI 시각화
✅ pg_stat_statements (PG)    — 누적 통계
✅ AWS RDS Performance Insights
```

> 면접에서 _슬로우 쿼리 로그_ + _APM_ 언급 = 운영 감각 신호.

---

# 도메인에서 — 슬로우 쿼리 자리

| 도메인 | 흔한 사례 |
| --- | --- |
| 페이지네이션 | OFFSET deep page (사례 1) |
| 관리자 통계 | 통계 노후 (사례 2) |
| 결제 / 주문 | 트랜잭션 길이 (사례 3) |
| 게시판 / CMS | TEXT 컬럼 (사례 4) |
| 검색 / 필터 | JOIN 순서 (사례 5) |

> 5 개 _도메인 무관_ 패턴. 어떤 회사 가도 _이 5 개_ 봄.

---

# 이력서에서 — 슬로우 쿼리 카드

```text
[관리자 페이지 deep page 8s → 10ms]
P (문제) /admin/orders page=500 응답 8s — 사용자 클레임
O (옵션) 캐시 / 인덱스 변경 / 커서 페이지네이션
D (결정) 커서 기반 — DB 부하 _일정_ (페이지 무관)
A (행동) created_id 복합 커서 + API 변경 + frontend 협업
R (결과) page 500 8s → 10ms (-99%), DB CPU 60% → 5%
```

---

# AI 보조 — 잘 쓰는 법

- **잘하는 것**: EXPLAIN 1 차 해석, 인덱스 후보 추천
- **자주 hallucinate**: _카디널리티_ 추측, 옵티마이저 _예측_
- **검증 루프**:
  1. 슬로우 쿼리 로그 _실제_ 추출
  2. AI 에 EXPLAIN + 데이터 분포 함께 전달
  3. 본인 환경에서 EXPLAIN 직접
  4. before/after 측정 → evidence

> AI 추천 인덱스가 _진짜로_ 쓰이는지 EXPLAIN 으로 확인.

---

# 다음 단계 — 미션 연결

- W4 미션 `05-week4-index` 통과 조건 = before/after EXPLAIN + latency
- 오늘 5 사례 중 _본인 코드와 비슷한_ 1 개 골라 evidence
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
