---
marp: true
theme: rpg
paginate: true
title: 'Week 2 강의 — JPA 영속성 + N+1'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week 2 강의

## JPA 영속성 + 연관관계 + N+1

Week 2 · 격주 강의 · 2026-06-06

---

<!-- _class: quest -->

# 왜 JPA 를 _깊게_ 보나

- 학습자가 가장 많이 _블랙박스_ 로 두는 영역
- "동작하는 코드 ≠ 좋은 코드" 가 가장 극명하게 드러남
- 면접 단골 질문 (영속성 / 연관관계 / N+1)
- Week 2 미션 통과 조건 = SQL 로그 before/after 비교

> "EntityManager 가 무슨 일을 하는지 _그림으로_ 설명할 수 있게."

---

# 오늘 다루는 것

1. 영속성 컨텍스트 4 기능
2. 엔티티 상태 (비영속 / 영속 / 준영속 / 삭제)
3. 연관관계 주인과 `mappedBy`
4. LAZY 기본 + N+1
5. 해결 3가지 — fetch join / `@EntityGraph` / batch size
6. 실수 사례 + Q&A

---

# 사전 지식 체크 (1분)

| 질문 | 답할 수 있나요? |
| --- | --- |
| 영속성 컨텍스트 한 줄 정의 | □ |
| 변경 감지가 발동하는 시점 | □ |
| LAZY 와 EAGER 의 차이 | □ |
| `mappedBy` 가 가리키는 것 | □ |
| `fetch join` 과 `@EntityGraph` 의 차이 | □ |

> 모르면 _이 강의를 들으면 답할 수 있게_ 됩니다. 끝나고 다시 체크.

---

<!-- _class: quest -->

# Part 1 — 영속성 컨텍스트

EntityManager 안의 _캐시 + 추적 메모_.

| 기능 | 효과 |
| --- | --- |
| 1차 캐시 | 같은 PK 재조회 SELECT 안 감 |
| 변경 감지 | 바뀐 필드만 UPDATE |
| 쓰기 지연 | INSERT/UPDATE 모아서 flush |
| 동일성 보장 | `==` 비교가 트랜잭션 내 동일 객체 |

> 이 4 기능을 _그림으로_ 설명할 수 있어야.

---

<!-- _class: lesson -->

## 1차 캐시

같은 트랜잭션 내 동일 PK → SELECT 안 감.

```java
@Transactional
public void firstLevelCache() {
  Post p1 = repo.findById(1L).get();  // SELECT 발생
  Post p2 = repo.findById(1L).get();  // SELECT 안 감
  System.out.println(p1 == p2);       // true
}
```

```text
🎯 동일성 보장 = 캐시의 부산물
```

---

<!-- _class: lesson -->

## 변경 감지 (Dirty Checking)

flush 시점에 _바뀐_ 필드만 UPDATE.

```java
@Transactional
public void update(Long id, String title) {
  Post p = repo.findById(id).get();
  p.changeTitle(title);
  // save() 호출 X
}
// 트랜잭션 종료 → flush → UPDATE post SET title = ?
```

```text
스냅샷 vs 현재 상태 비교 → 변경 필드만 SQL
```

---

<!-- _class: lesson -->

## 쓰기 지연

INSERT/UPDATE 를 모아서 flush 때 한 번.

```java
@Transactional
public void batchInsert() {
  for (int i = 0; i < 100; i++) {
    repo.save(new Post("title-" + i));
  }
  // 100개 INSERT 가 flush 시점에 한 번에
}
```

```text
JDBC 배치 + hibernate.jdbc.batch_size 로 더 최적화 가능
```

---

# 엔티티 상태 흐름

```
   new Post()        em.persist()
비영속 ──────────────▶ 영속
                       │ em.detach() / clear()
                       ▼
                     준영속
                       │ em.merge()
                       ▼
                     영속 ──────▶ 삭제 (em.remove)
```

> 면접에서 _상태 4개_ 를 흐름으로 그릴 수 있어야.

---

<!-- _class: quest -->

# Part 2 — 연관관계 주인

DB FK 는 _한 곳_ 에만 있다 — 양방향 매핑에서 누가 _주인_ 인지 결정.

- 주인 = FK 컬럼을 갖는 쪽 (보통 N 쪽)
- 거울 = `mappedBy` 로 주인을 가리킴
- _주인의 setter_ 만 DB 에 영향
- `@JoinColumn` / `mappedBy` / 편의 메서드 설계

> Week 2 evidence/association-owner-decision.md 의 핵심.

---

<!-- _class: lesson -->

## 양방향 매핑 — 누가 주인?

`Post 1 : N Comment` — FK 는 `comment.post_id`.

```java
@Entity
public class Comment {
  @ManyToOne(fetch = LAZY)
  @JoinColumn(name = "post_id")
  private Post post;  // 주인 = FK 가짐
}

@Entity
public class Post {
  @OneToMany(mappedBy = "post")
  private List<Comment> comments;  // 거울
}
```

```text
규칙:
- N 쪽이 보통 주인
- 거울 쪽에 mappedBy
- 주인 setter 만 DB 영향
```

---

# `CascadeType` 과 `orphanRemoval`

- `CascadeType.PERSIST` — 부모 저장 시 자식도
- `CascadeType.REMOVE` — 부모 삭제 시 자식도
- `orphanRemoval = true` — 컬렉션에서 빠지면 삭제

```java
@OneToMany(mappedBy = "post",
  cascade = CascadeType.ALL,
  orphanRemoval = true)
private List<Comment> comments;
```

> 무분별한 ALL + orphanRemoval 은 _연쇄 삭제_ 위험. 도메인 _합의_ 필요.

---

# 편의 메서드로 양쪽 동기화

```java
public class Post {
  public void addComment(Comment c) {
    this.comments.add(c);
    c.setPost(this);  // 양쪽 같이
  }
}
```

> "주인 쪽만 set 해도 DB 는 OK" 지만 _런타임 객체 그래프_ 까지 일관되게.

---

<!-- _class: quest -->

# Part 3 — N+1 해결

EAGER 가 _기본_ 이 아닌 이유 + 면접 단골.

- 기본은 LAZY — _필요한 시점_ 에만 SELECT
- N+1 = 컬렉션 순회 시 N 번 SELECT 추가 발생
- 해결 3가지: fetch join / `@EntityGraph` / batch size
- 함정: fetch join + paging — 메모리 페이징 위험

> Week 2 통과 조건 = SQL 로그 before/after 비교.

---

<!-- _class: lesson -->

## LAZY 동작

```java
@ManyToOne(fetch = LAZY)
private Post post;
```

`post.getTitle()` 호출 시점에 SELECT 발생.

```text
초기 SELECT — Comment 만
이후 .post.* 접근 시 — Post SELECT
```

---

<!-- _class: lesson -->

## N+1 발생

```java
List<Post> posts = postRepo.findAll();
for (Post p : posts) {
  p.getComments().size();  // 각각 SELECT
}
```

```sql
-- N+1 = 1 + N
SELECT * FROM post;
SELECT * FROM comment WHERE post_id = ?;  -- N 번
```

LAZY 가 _문제_ 가 아니라, _컬렉션 순회_ 가 문제.

---

# 해결 1 — fetch join (JPQL)

```java
@Query("SELECT p FROM Post p LEFT JOIN FETCH p.comments")
List<Post> findAllWithComments();
```

```sql
SELECT p.*, c.*
FROM post p
LEFT JOIN comment c ON c.post_id = p.id;
```

장점: SQL 1번. 단점: _페이징과 충돌_ (JPA 가 메모리에서 처리).

---

# 해결 2 — `@EntityGraph`

```java
@EntityGraph(attributePaths = {"comments"})
List<Post> findAll();
```

장점: 메서드별로 _다른 그래프_ 사용 가능. 페이징과 더 친화적.

```text
fetch join 의 어노테이션 버전
```

---

# 해결 3 — Batch Size

```yaml
spring:
  jpa:
    properties:
      hibernate:
        default_batch_fetch_size: 100
```

```sql
-- N+1 → 1+1
SELECT * FROM post;
SELECT * FROM comment WHERE post_id IN (?, ?, ..., 100);
```

장점: 코드 변경 없음. _대규모_ 에서 효과적.

---

# 실수 사례 — fetch join + paging

```java
@Query("SELECT p FROM Post p LEFT JOIN FETCH p.comments")
Page<Post> findAll(Pageable pageable);
```

⚠️ Hibernate 경고:
```
firstResult/maxResults specified with collection fetch;
applying in memory!
```

→ DB 가 아닌 _메모리_ 에서 페이징. OOM 위험.

해결: `@EntityGraph` + Slice / 또는 ToOne 만 fetch join.

---

# 실수 사례 — distinct 빠뜨리기

```java
@Query("SELECT p FROM Post p LEFT JOIN FETCH p.comments")
```

→ Comment 수만큼 _Post 중복_ 발생.

```java
@Query("SELECT DISTINCT p FROM Post p LEFT JOIN FETCH p.comments")
```

> Hibernate 6+ 부터는 자동 처리되지만 _명시_ 권장.

---

# AI 보조 — 잘 쓰는 법

- **잘하는 것**: JPQL 작성, fetch join 코드 생성, Entity 설계 1차안
- **자주 hallucinate**: `@OneToOne` 의 `mappedBy` 위치, Cascade 의 부작용
- **검증 루프**:
  1. AI 코드 받기
  2. _직접_ 실행 + SQL 로그 확인
  3. 의심 가는 부분 _공식 문서_ 로 교차 검증
  4. evidence 에 _차이_ 기록

> _AI 가 짠 코드의 SQL 을 본인 눈으로 확인_ 하는 습관.

---

# 도메인에서 — JPA 가 보이는 자리

이름은 달라도 _패턴은 같다_ — 1:N 컬렉션 조회 + 페이징 = N+1 함정.

| 도메인 | 패턴 | 위험 |
| --- | --- | --- |
| 게시판 + 댓글 | `Post.comments` 조회 | N+1 (오늘 다룬 사례) |
| 회원 + 주문 목록 | 마이페이지 | N+1 + paging 메모리 폭발 |
| 상품 + 옵션 + 카테고리 | 상세 페이지 ToOne 체인 | LAZY 초기화 시점 누락 |
| 검색 결과 + 첨부 | `Page<Post> + comments` | fetch join + paging 함정 |
| 관리자 지표 | OneToMany 집계 | 컬렉션 distinct 빠뜨림 |

> 학습자가 _개발자_ 가 되어가는 신호 = _다른 도메인_ 에서 _같은 패턴_ 을 본다.

---

# 이력서에서 — JPA 카드 sample

```text
[게시판 응답 지연 600ms 개선]
P (문제) /posts 평균 600ms, p99 1.2s — 게시글당 댓글 N+1
O (옵션) EAGER 전환 / fetch join / @EntityGraph / batch fetch size
D (결정) @EntityGraph 채택 — paging 친화적
A (행동) PostRepository.findAllWithComments() + 테스트 추가
R (결과) SQL 51 → 1, 평균 600ms → 90ms (-85%), p99 1.2s → 180ms
```

> 매 강의 끝 = 본인 레포 `evidence/interview-cards/jpa.md` 에 P-O-D-A-R 1세트.
> 10주 누적 = 면접 답변 카드 15개 → Week 10 피날레에서 그대로 답변.

---

# 다음 단계 — 이번 주 미션 연결

- 미션 `03-week2-jpa` 의 통과 조건 = _SQL 로그로 차이 설명_
- 학습 목표 2번(N+1 또는 fetch join 차이)이 오늘 강의와 1:1 매칭
- evidence 에 박을 것:
  - `n-plus-one-before.md` — show_sql 로그 N+1 캡처
  - `n-plus-one-after.md` — fetch join 또는 @EntityGraph 적용 후 캡처
  - `association-owner-decision.md` — 연관관계 주인 결정 근거

---

<!-- _class: end -->

# Q&A

질문은 강의 어디에서나. 화·목 21:00 오피스아워에서 이어가도 OK.

> 다음 격주 강의(Week 4): **인덱스 / EXPLAIN 으로 쿼리 플랜 읽기**.
