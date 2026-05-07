---
marp: true
theme: rpg
paginate: true
title: 'Week 4 — 인덱스 / EXPLAIN'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week 4

## 인덱스 / EXPLAIN

2026-06-27 (토) · 미션 공개 + 주간 방향

---

# 쿼리 어디갔니

![w:500](../theme/assets/memes/w4.jpg)


---

# 지난 주 돌아보기 — Week 3 이력서

| 항목 | 결과 |
| --- | --- |
| **제출률** | {{N}}/{{M}} 명 |
| **잘된 점** | 본인 PR 수치를 _그대로 bullet_ 에 박은 학생 다수 |
| **아쉬운 점** | _서사_ 가 짧고 _감정_ 만 있는 케이스 |
| **이번 주 가져갈 것** | 수치는 _측정 도구_ 에서 오고, _본인이 측정_ 해야 함 |

---

<!-- _class: quest -->

# 05-week4-index

- **type**: `code`
- **마감**: 2026-07-03 (금) `23:59`
- **검증**: PR → mission-guard CI → AI 리뷰
- **통과 조건**: before/after EXPLAIN + latency 비교표 모두 제출

> "인덱스 = 책의 _목차_. 없으면 _전체_ 를 다 봐야 한다."

---

# 비유 — 전화번호부

![w:300](../theme/assets/images/phonebook.jpg)

- 이름 _없이_ 1만 명 중 "김철수" = **풀스캔** (10,000회)
- 이름 _가나다 정렬_ 책에서 찾기 = **인덱스 스캔** (~14회)

> 인덱스 = 미리 _정렬_ 해둔 빠른 길.

---

# 이번 주 학습 목표

1. **EXPLAIN 으로 쿼리 플랜 읽기** — `type` / `key` / `rows` 3 컬럼만
2. **인덱스 적용 전후 latency 측정** — 수치 1개 이상 (`hey` / `curl + time` / `k6`)
3. **before/after 비교표 작성** — 같은 쿼리·같은 데이터로

---

<!-- _class: lesson -->

## EXPLAIN 출력 — 3 컬럼만 보면 OK

```sql
EXPLAIN SELECT * FROM post WHERE user_id = 5;
```

| type | key | rows |
| --- | --- | --- |
| `ALL` | `null` | 100,000 |

→ 풀스캔. 인덱스 _없음_.

| type | key | rows |
| --- | --- | --- |
| `ref` | `idx_user` | 23 |

→ 인덱스 적중.

---

<!-- _class: lesson -->

## 인덱스 추가하기

```sql
CREATE INDEX idx_user ON post(user_id);
```

```text
✅ 같은 쿼리 → rows 100,000 → 23
✅ latency 800ms → 50ms (-94%)
```

```text
한 줄 명령. 마이그레이션 스크립트로 관리.
```

---

# 함정 — 인덱스가 _안 타는_ 케이스

- 컬럼 _가공_: `WHERE YEAR(created_at) = 2026` (인덱스 무시)
- _LIKE_ 앞쪽 와일드카드: `WHERE name LIKE '%kim'`
- _OR_ 조건: `WHERE a=1 OR b=2` (둘 다 인덱스 없으면 풀스캔)
- 데이터 _카디널리티_ 낮음: `WHERE deleted=0` (대부분 0)
- 옵티마이저 _판단_ 으로 풀스캔 선택 (소량 테이블)

> 인덱스가 _존재_ 한다 ≠ 인덱스가 _쓰인다_. EXPLAIN 으로 확인.

---

# 이번 주에 제출할 것

```
05-week4-index/
├── report.md
├── project/                       # Spring Boot baseline + 인덱스
└── evidence/
    ├── seed-data.sql              # 10만 row 시드
    ├── measure.sh                 # 측정 스크립트
    ├── before-explain.txt         # 인덱스 전 EXPLAIN
    ├── after-explain.txt          # 인덱스 후 EXPLAIN
    └── latency-comparison.md      # 표 형식 비교
```

---

# 평가 기준 (5축)

| 축 | 가중 | 핵심 |
| --- | --- | --- |
| 요구사항 충족 | ★★ | EXPLAIN before/after 모두 |
| 구조 | ★ | 인덱스 명명 / 마이그레이션 |
| 기술 적용 | ★★ | 인덱스 _선택 근거_ |
| 검증 근거 | ★★★ | _수치 비교표_ — p95 또는 평균 |
| 설명력 | ★★ | EXPLAIN 결과를 _말로 설명_ |

> Week 4 부터 _검증 근거 품질_ 가중 ↑↑. before/after 표 + 재현 명령 없으면 5점 불가.

---

# 측정 도구 — 본인 선택

각 도구 trade-off:

| 도구 | 장점 | 단점 |
| --- | --- | --- |
| `curl + time` | 가장 단순 | 1 회 측정만 |
| `hey` | 동시 요청 + 분포 | 추가 설치 |
| `k6` | 시나리오 + p95/p99 | 학습 곡선 |
| JMeter | GUI / 무거운 시나리오 | 설치 + 무거움 |

> sample 은 `hey` 사용. 본인이 다른 도구 골라도 OK — 선택 _근거_ 만 evidence 에.

---

# 운영 안내

- **제출 마감**: 2026-07-03 (금) `23:59`
- **토 15:00–16:30**: 격주 **강의** — 인덱스 / EXPLAIN 깊게
- **오피스아워**: 화·목 `21:00` `{cohort}-질문` 스레드
- **PR 알림**: `{cohort}-리뷰` 채널 자동

---

<!-- _class: end -->

# Q&A

```text
이번 주 = "본인 코드의 SQL 을 _직접_ 측정"
다음 면접 답변 = "p95 800ms → 50ms (-94%)"
```

> 오늘 15:00 — 슬로우 쿼리 사례 5선 (퀴즈 형식).
