---
marp: true
theme: rpg
paginate: true
title: 'Week 4 강의 — 인덱스 / EXPLAIN'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week 4 강의

## 인덱스 / EXPLAIN — 쿼리 플랜 읽기

Week 4 · 격주 강의 · 2026-06-20

---

<!-- _class: quest -->

# 왜 인덱스 인가

- DB 가 _느려지는_ 가장 흔한 이유 1 위
- 인덱스 _하나_ 로 latency 800ms → 50ms 가능
- 면접 단골 (EXPLAIN 읽을 줄 아세요?)
- Week 4 미션 통과 조건 = before/after EXPLAIN

> "쿼리 _작성_ 은 누구나, _플랜 읽기_ 는 백엔드 개발자."

---

# 오늘 다루는 것

1. 인덱스 비유 — 책 목차
2. EXPLAIN 3 컬럼만 보기
3. 인덱스 _안 타는_ 5 가지 함정
4. 복합 인덱스 — 순서가 중요
5. 도메인에서 + 이력서에서

---

# 사전 지식 체크 (1분)

| 질문 | □ |
| --- | --- |
| 인덱스 한 줄 정의 | □ |
| EXPLAIN 의 `type` 값 의미 | □ |
| 풀스캔 vs 인덱스 스캔 차이 | □ |
| 인덱스 _안 타는_ 케이스 1 가지 | □ |

> 모르면 _이 강의를 들으면_ 답할 수 있게.

---

<!-- _class: quest -->

# Part 1 — 비유부터

책 한 권에서 _김철수_ 이름 찾기.

- **목차 없음** → 1 페이지부터 끝까지 (= 풀스캔)
- **가나다 목차** → 김씨 페이지 펼침 (= 인덱스 스캔)
- **이름·연도 목차** → 김씨 + 2024 동시 (= 복합 인덱스)

> DB 도 똑같다. 인덱스 = _미리 정렬된 목차_.

---

# 인덱스의 _대가_

빠른 조회는 공짜가 아님.

```text
✅ SELECT 빠름
❌ INSERT/UPDATE/DELETE 느림 (인덱스도 갱신)
❌ 디스크 공간 더 먹음
❌ 메모리 (버퍼풀) 더 먹음
```

> 인덱스 _많이_ 만들수록 읽기 빠름 + 쓰기 느림. 균형 필요.

---

<!-- _class: quest -->

# Part 2 — EXPLAIN 읽기

쿼리 _실행 전_ 옵티마이저가 어떻게 풀지 보여줌.

- 모든 백엔드 개발자가 _매일_ 본다
- 하지만 _3 컬럼_ 만 보면 95% 답
- type / key / rows

---

<!-- _class: lesson -->

## EXPLAIN 출력

```sql
EXPLAIN SELECT * FROM post WHERE user_id = 5;
```

| type | key | rows |
| --- | --- | --- |
| ALL | null | 100,000 |

```text
type=ALL → 풀스캔
key=null → 인덱스 미사용
rows=10만 → 10만 줄 스캔
→ 인덱스 추가 필요!
```

---

<!-- _class: lesson -->

## type 값 — 좋은 순서

```text
🟢 const     - PK 단일 row
🟢 ref       - 인덱스 적중 (가장 일반)
🟢 range     - 범위 스캔 (BETWEEN, <, >)
🟡 index     - 인덱스 풀스캔 (이상함)
🔴 ALL       - 풀스캔 (인덱스 없음)
```

```text
ref / range 면 OK
ALL 보이면 인덱스 추가 검토
```

---

# 인덱스 추가 — 명령 1줄

```sql
CREATE INDEX idx_post_user ON post(user_id);
```

이 명령으로:

```text
✅ type=ALL    → ref
✅ key=null    → idx_post_user
✅ rows=100000 → 23
✅ latency 800ms → 50ms
```

> 마이그레이션으로 관리. 운영 DB 는 _CONCURRENTLY_ 옵션.

---

<!-- _class: quest -->

# Part 3 — 인덱스 함정

인덱스가 _존재_ 한다 ≠ 인덱스가 _쓰인다_.

5 가지 함정 — 면접 단골.

---

# 함정 1 — 컬럼 가공

```sql
-- ❌ 인덱스 무시
WHERE YEAR(created_at) = 2026

-- ✅ 인덱스 적중
WHERE created_at >= '2026-01-01'
  AND created_at <  '2027-01-01'
```

> 좌변 컬럼에 함수·연산 들어가면 _인덱스 못 씀_.

---

# 함정 2 — LIKE 앞쪽 와일드카드

```sql
-- ❌ 인덱스 무시
WHERE name LIKE '%kim'

-- ✅ 인덱스 적중
WHERE name LIKE 'kim%'
```

> 풀텍스트 검색 필요하면 _전용 검색 엔진_ (Elasticsearch).

---

# 함정 3 — 카디널리티 낮음

```sql
-- ❌ 옵티마이저가 풀스캔 선택
WHERE deleted = 0
-- (deleted 컬럼 95% 가 0)
```

```text
인덱스가 _존재_ 해도, 결과가 _대부분_ 이면
풀스캔이 더 빠르다고 옵티마이저가 판단.
```

> 카디널리티 = 컬럼 _다양성_. 낮으면 인덱스 효과 X.

---

# 함정 4 — OR 조건

```sql
-- ❌ 두 컬럼 모두 인덱스 있어도 풀스캔 가능
WHERE a = 1 OR b = 2

-- ✅ UNION 으로 분리
SELECT * FROM t WHERE a = 1
UNION
SELECT * FROM t WHERE b = 2
```

---

# 함정 5 — 복합 인덱스 순서

```sql
CREATE INDEX idx_a_b ON t(a, b);

-- ✅ 인덱스 적중 (a 가 선두)
WHERE a = 1 AND b = 2
WHERE a = 1

-- ❌ 인덱스 무시 (b 만)
WHERE b = 2
```

> 복합 인덱스는 _선두 컬럼_ 부터 순서대로. 전화번호부에서 _이름_ 없이 _연도_ 만으론 못 찾는 것과 같음.

---

# 도메인에서 — 인덱스 자리

| 도메인 | 패턴 | 인덱스 후보 |
| --- | --- | --- |
| 게시판 | `WHERE user_id=?` | `idx_post_user` |
| 검색 | `WHERE title LIKE 'kim%'` | `idx_title` |
| 주문 목록 | `WHERE user_id=? ORDER BY created` | `idx_user_created` |
| 통계 | `WHERE created BETWEEN ?` | `idx_created` |
| 관리자 | `WHERE status=? AND created>?` | `idx_status_created` |

> 인덱스 설계 = _어떤 쿼리_ 가 자주 도는지 분석부터.

---

# 이력서에서 — 인덱스 카드 sample

```text
[게시판 응답 800ms → 50ms 개선]
P (문제) /posts?user_id=5 평균 800ms — EXPLAIN type=ALL
O (옵션) 인덱스 추가 / 캐시 / 페이징 변경
D (결정) idx_post_user 단일 인덱스 — 가장 단순한 first-cut
A (행동) CREATE INDEX + 마이그레이션 + 부하 테스트
R (결과) latency 800ms → 50ms (-94%), rows 100K → 23
```

> 본인 evidence/latency-comparison.md 그대로 옮겨 적기.

---

# AI 보조 — 잘 쓰는 법

- **잘하는 것**: 인덱스 _후보_ 추천, EXPLAIN 결과 해석
- **자주 hallucinate**: 옵티마이저 _예측_, 카디널리티 추측
- **검증 루프**:
  1. AI 답 받기
  2. 본인 데이터로 EXPLAIN _직접_
  3. 실측 latency 비교
  4. evidence 에 _차이_ 기록

> AI 가 추천한 인덱스가 _실제로_ 쓰이는지 EXPLAIN 으로.

---

# 다음 단계 — 미션 연결

- 미션 `05-week4-index` 통과 조건 = before/after EXPLAIN + latency 비교
- evidence/before-explain.txt 와 after-explain.txt 가 핵심
- latency-comparison.md 에 표 형식 비교

> 막히면 → `{cohort}-질문` 채널 + 오피스아워 (화·목 `21:00`)

---

<!-- _class: end -->

# Q&A

```text
이번 주 = "내 쿼리의 EXPLAIN 직접 보기"
다음 면접 = "인덱스 어떻게 추가?" 답할 수 있게
```

> 다음 격주 강의(Week 6): **프로파일링 / 측정 기반 최적화**.
