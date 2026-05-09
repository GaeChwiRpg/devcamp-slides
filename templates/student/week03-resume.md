<!--
TEMPLATE: Week 3 학생 내부 발표 — 이력서 차별화
운영: 토 15:00–16:30, 3분 발표 + 2분 피드백, 팀별 1명 로테이션
제출: 금 18:00 까지 `{cohort}-리뷰` 채널에 본인 사본 링크

작성 흐름 (15분):
  1. 본인 강한 PR 1건 고르기 (W1 또는 W2)
  2. {{...}} placeholder 채우기
  3. 빌드 또는 Google Slides 로 변환
  4. 사본 링크 채널 게시
-->

---
marp: true
theme: rpg
paginate: true
title: 'Week 3 학생 발표 — 이력서 차별화'
---

<!-- _class: cover -->
<!-- _paginate: false -->

# {{본인 이름}}

## 이력서 차별화 — bullet 1건 + 서사

Week 3 · {{팀명}} · {{2026-MM-DD}}

---

# 자랑할 PR 1건 ✨

**PR**: [{{PR 제목}}]({{PR URL}})
**미션**: `{{02-week1-spring-boot}}` (또는 `03-week2-jpa`)

```text
❌ 형용사 (Before)
"{{형용사로만 쓴 bullet — 예: Spring Boot 로 게시판 개발}}"

✅ 정량 (After)
"{{수치 + evidence — 예: 응답 600ms → 90ms (-85%), N+1 1건 fetch join, evidence/n-plus-one-after.md}}"
```

> 차이: 동작 → _수치 + 근거 파일_.

---

# 서사 1개 — 200자 이야기 📖

```text
{{문제 발견 1줄 — 예: 게시글 응답 600ms, 사용자 클레임 발생}}
{{원인 1줄 — 예: PostRepository.findAll() 후 댓글 N+1 발견}}
{{시도/결정 1줄 — 예: fetch join vs @EntityGraph 비교 후 후자 선택 (paging 친화)}}
{{결과 수치 1줄 — 예: 600ms → 90ms (-85%), SQL 51 → 1}}
{{배운 점 1줄 — 예: paging 시 fetch join 메모리 폭발 위험 학습}}
```

> 면접에서 _그대로 말하기_ 좋도록.

---

<!-- _class: end -->

# 피드백 받기 ❓

**잘한 점 1줄 / 개선 1줄** 자유롭게 — 비판적이지만 _격려 톤_.

> 다음 주: Week 4 인덱스 / EXPLAIN.
