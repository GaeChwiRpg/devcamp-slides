<!--
TEMPLATE: Week 9 학생 내부 발표 — 팀 프로젝트 본인 PR
운영: 토 15:00–16:30, 3분 발표 + 2분 피드백, 팀별 1명 로테이션
제출: 금 18:00 까지 `{cohort}-리뷰` 채널에 본인 사본 링크

작성 흐름 (15분):
  1. 팀 프로젝트에서 _본인이 담당한 PR 1건_ 고르기
  2. 라이프사이클 5단계 中 _본인이 한_ 단계 + 6 공통 필수 中 _본인이 다룬_ 영역 표시
  3. {{...}} placeholder 채우기
  4. 빌드 또는 Google Slides 로 변환
-->

---
marp: true
theme: rpg
paginate: true
title: 'Week 9 학생 발표 — 팀 PR'
---

<!-- _class: cover -->
<!-- _paginate: false -->

# {{본인 이름}}

## 팀 PR — 본인 영역 + 검증

Week 9 · {{팀명}} · {{2026-MM-DD}}

---

# 본인 PR + 좌표 🗺️

**팀 도메인**: {{도메인 1줄 — 예: 중고 거래 게시판}}
**본인 PR**: [{{PR 제목}}]({{PR URL}})

```text
[라이프사이클 단계]
□ 기획 (PRD)    □ 설계 (ARCH)
■ 구현 (PR)     □ 검증 (TEST)    □ 운영 (OBS)
                ↑ 본인이 한 단계 표시

[6 공통 필수 中 다룬 영역]
■ JPA 연관관계 / 인덱스
□ 동시성 / 락
□ 성능 / 캐시
□ AI 활용 흔적
```

> 팀 PR 中 _내 자리_ 명확히.

---

# 깬 문제 1개 — Before/After 📊

```text
[발견]
{{1줄 — 예: 거래글 목록 첫 화면 800ms, 사용자 이탈 관찰}}

[원인]
{{1줄 — 예: PostRepository.findAll() N+1 + 미인덱스}}

[조치]
{{1줄 — 예: fetch join + (region, status) 복합 인덱스}}

[결과]
{{p99 800ms → 95ms (-88%), SQL 41 → 1}}

evidence/{{본인-evidence-파일.md}}
```

> 수치 + evidence 파일명 _꼭_.

---

# 팀 협업 — 본인 결정 1건 🤝

```text
[충돌 / 결정 포인트]
{{1줄 — 예: 동시성 락 위치 — service vs repository}}

[고려한 옵션]
{{1줄 — 예: 1) 서비스 레이어 락, 2) repository 메서드 락}}

[본인 의견 + 근거]
{{1줄 — 예: repository — 트랜잭션 경계와 일치, 재사용 ↑}}

[결과]
{{1줄 — 예: 팀 합의 후 머지, 통합 테스트 통과}}
```

> 팀에서의 _본인 입장_ = 면접관이 보는 협업력.

---

# AI 활용 흔적 🤖

```text
[사용 케이스]
{{1줄 — 예: fetch join vs @EntityGraph 비교 — Claude Code}}

[hallucination 잡힌 사례]
{{1줄 — 예: AI 가 deprecated API 추천 → 공식 문서 확인 후 정정}}

[evidence]
{{evidence/prompt-log.md 또는 AI-decision-log.md}}
```

> AI _맹신_ 아니라 _검증_ — 차별화 포인트.

---

# P-O-D-A-R 카드 📇

```text
P (문제) {{1줄 — 예: 거래글 목록 p99 800ms}}
O (옵션) 인덱스 / fetch join / 캐시 / read replica
D (결정) {{1줄 — 예: fetch join + 복합 인덱스 (캐시는 W7 이후)}}
A (행동) {{1줄 — 예: PostRepository.findAllWithMember() 추가}}
R (결과) {{1줄 — 예: p99 95ms (-88%), SQL 41→1}}
```

> 면접에서 _그대로 말하기_ 좋도록.

---

<!-- _class: end -->

# 피드백 받기 ❓

**잘한 점 1줄 / 개선 1줄** 자유롭게 — 비판적이지만 _격려 톤_.

> 다음 주: Week 10 FINAL BOSS — 팀 최종 발표.
