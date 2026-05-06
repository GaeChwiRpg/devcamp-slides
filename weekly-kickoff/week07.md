---
marp: true
theme: rpg
paginate: true
title: 'Week 7 — Redis 실전 활용'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week 7

## Redis 실전 활용

2026-07-11 (토) · 미션 공개 + 주간 방향

---

# 지난 주 돌아보기 — Week 6

| 항목 | 결과 |
| --- | --- |
| **제출률** | {{N}}/{{M}} 명 |
| **잘된 점** | 핫스팟 1 개 _수치_ 로 잡은 학생 다수 |
| **아쉬운 점** | 우선순위 _근거_ 가 약함 |
| **이번 주 가져갈 것** | _기억_ 으로 풀 수 있는 것은 캐시로 |

---

<!-- _class: quest -->

# 08-week7-redis

- **type**: `code`
- **마감**: 2026-07-17 (금) `23:59`
- **검증**: PR → mission-guard CI → AI 리뷰
- **통과 조건**: 캐시 hit rate 리포트 + 팀 프로젝트 설계 초안

> "DB 가 _계산기_ 라면, Redis 는 _포스트잇 메모_."

---

# 비유 — 카페 주문

매번 _레시피_ 보고 만들면 (= DB 조회) 시간 ↑↑.

자주 나가는 메뉴는 _미리 만들어 두고_ (= Redis 캐시) 손님에게 _즉시_.

- 너무 _많이_ 미리 만들면 → 식어버림 (= TTL 초과)
- _안 팔리는 메뉴_ 만들어두면 → 메모리 낭비
- 레시피 바뀌면 → _미리 만든 거_ 도 폐기 (= invalidation)

---

# 이번 주 학습 목표

1. **캐시 키 설계** — 무엇을 키로 잡고 TTL 얼마인지 _근거_
2. **hit rate 측정** — Spring Actuator `metrics/cache.gets` 또는 Redis `INFO stats`
3. **invalidation 전략** — 데이터 바뀌면 캐시 어떻게 비우는지

---

<!-- _class: lesson -->

## 캐시 hit rate — 무엇을 측정하나

```text
hit  = 캐시에서 가져옴 (DB 안 감)
miss = 캐시 없어서 DB 갔다 옴

hit rate = hits / (hits + misses) × 100
```

```text
hit rate 90%+  = 매우 좋음
hit rate 50%   = 캐시 무용지물
hit rate 10%   = 캐시 _빼는_ 게 나음
```

---

<!-- _class: lesson -->

## Spring 캐시 적용

```java
@Cacheable(value="post", key="#id")
public Post findById(Long id) { ... }

@CacheEvict(value="post", key="#post.id")
public void update(Post post) { ... }
```

| 어노테이션 | 동작 |
| --- | --- |
| `@Cacheable` | 결과 캐시 저장 |
| `@CacheEvict` | 캐시 제거 (수정) |

---

# invalidation — 캐시 폐기 전략

```text
1. TTL 만료 — 시간 지나면 자동 (가장 단순)
2. 변경 감지 — 데이터 수정 시 즉시 (@CacheEvict)
3. Write-Through — 캐시·DB 동시 갱신
4. Refresh-Ahead — TTL 끝나기 전 미리 갱신
```

> 첫 PR 은 _TTL + @CacheEvict_ 조합. 나머지는 _필요할 때_.

---

# 함정 — 흔한 실수

- ❌ TTL 너무 길게 → 데이터 _낡음_ (예: 24시간 — 사용자가 본 글 안 보임)
- ❌ TTL 너무 짧게 → 캐시 효과 X
- ❌ 키에 _가변 객체_ 사용 → 매번 다른 키 → miss
- ❌ DB 변경 시 _캐시 안 비움_ → stale 데이터
- ❌ hit rate 측정 _안 함_ → 캐시 효과 _감_ 으로

---

# 이번 주에 제출할 것

```
08-week7-redis/
├── report.md
├── project/                      # Spring Boot baseline + Redis
└── evidence/
    ├── cache-key-notes.md        # 키 설계 + TTL 근거
    ├── hit-rate-report.md        # 측정 결과
    ├── db-load-comparison.md     # DB 호출 수 before/after
    └── measure-cache.md          # 측정 명령 + Actuator 설정
```

---

# 팀 프로젝트 진입 — 설계 초안

이번 주는 _개인 미션_ + _팀 프로젝트 설계 초안_ 동시.

- 본인 팀 도메인 1 개 결정 (예: 재고 / 알림 / 검색)
- 6 공통 필수 기능 중 _이번 팀 PR_ 에서 다룰 것 매핑
- `evidence/team-project-draft.md` 1 장

> Week 8 에서 _팀 프로젝트 진입 점검_, Week 9 부터 _팀 본격 가동_.

---

# 평가 기준 (5축)

| 축 | 가중 | 핵심 |
| --- | --- | --- |
| 요구사항 충족 | ★★ | 캐시 + hit rate 모두 |
| 구조 | ★★ | 캐시 위치 / 책임 분리 |
| 기술 적용 | ★★ | TTL / invalidation _근거_ |
| 검증 근거 | ★★★ | hit rate + DB 호출 비교 |
| 설명력 | ★★ | 캐시 _전략_ 본인 말로 |

---

# 운영 안내

- **제출 마감**: 2026-07-17 (금) `23:59`
- **토 15:00–16:30**: 학생 내부 발표 (강의 슬롯 아님)
- **오피스아워**: 화·목 `21:00` `{cohort}-질문` 스레드
- **팀 매칭**: Week 8 종료 시점 _공식 발표_

---

<!-- _class: end -->

# Q&A

```text
이번 주 = "DB 한 번 → 100 번 응답 가능?"
다음 면접 = "캐시 hit rate 어떻게 측정?" 답할 수 있게
```

> 다음 주: **Week 8 — AI Native** + 격주 강의.
