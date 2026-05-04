<!--
TEMPLATE: 매주 토 14:00–15:00 미션 공개 + 주간 방향 (15-25장 / 30-45분)
사용법:
  cp templates/_kickoff-template.md weekly-kickoff/weekNN.md
  → {{...}} placeholder 모두 교체 → push → CI 가 PDF 빌드

채울 SoT:
- mission_id / title / week → bootcamp-admin/src/lib/mission-catalog.ts
- 학습 목표 / 평가 기준 → bootcamp-admin/docs/bootcamp/curriculum.md, review-rubric.md
- 제출 evidence → devcamp-submission-sample/<mission_id>/README.md
-->

---
marp: true
theme: rpg
paginate: true
title: 'Week {{NN}} — {{퀘스트 제목}}'
---

<!-- _class: cover -->
<!-- _paginate: false -->

![logo](../theme/assets/logo.png)

# Week {{NN}}

## {{퀘스트 제목}}

{{2026-MM-DD}} · 미션 공개 + 주간 방향

---

# 지난 주 돌아보기

- **제출률**: {{N/M}} 명, {{X%}}
- 잘된 점: {{한 줄}}
- 아쉬운 점: {{한 줄}}
- 이번 주에 가져갈 것: {{한 줄}}

---

<!-- _class: quest -->

# {{퀘스트 제목}}

- **mission_id**: `{{02-week1-spring-boot}}`
- **type**: `{{code | docs | team_pr}}`
- **마감**: {{2026-MM-DD 23:59}}
- **검증**: PR 생성 → mission-guard CI green → AI 리뷰 → 점수 업데이트

> "{{한 문장 미션 설명}}"

---

# 이번 주 학습 목표

1. **{{목표 1}}** — {{한 줄 설명}}
2. **{{목표 2}}** — {{한 줄 설명}}
3. **{{목표 3}}** — {{한 줄 설명}}

> _curriculum.md 의 통과 조건과 1:1 매칭_

---

<!-- _class: lesson -->

## 핵심 개념 1 — {{개념}}

{{개념 정의 / 비유 / 한국어 풀이}}

```
{{코드 또는 다이어그램 1줄}}
```

```text
{{핵심 키워드 또는 흐름}}
```

---

<!-- _class: lesson -->

## 핵심 개념 2 — {{개념}}

{{왼쪽: 개념}}

{{오른쪽: 코드/그림}}

---

<!-- _class: lesson -->

## 핵심 개념 3 — {{개념}}

{{왼쪽}}

{{오른쪽}}

---

# 함정 / 자주 하는 실수

- ❌ {{실수 1}} → ✅ {{교정}}
- ❌ {{실수 2}} → ✅ {{교정}}
- ❌ {{실수 3}} → ✅ {{교정}}

---

# 이번 주에 제출할 것

- [ ] `report.md` — {{필수 항목 1줄}}
- [ ] `evidence/{{파일1}}` — {{무엇을 보여주는지}}
- [ ] `evidence/{{파일2}}` — {{무엇을}}
- [ ] PR 본문: 기능 / 라이프사이클 / 검증 / API / AI

> 정확한 파일명은 `devcamp-submission-sample/{{mission_id}}/README.md` "이번 주에 제출할 것" 그대로

---

# 평가 기준 (5축)

| 축 | 1점 | 3점 | 5점 |
| --- | --- | --- | --- |
| 요구사항 충족 | 일부 누락 | 모두 충족 | 추가 케이스 |
| 구조 | 절차 나열 | 책임 분리 | 일관 패턴 |
| 기술 적용 | 동작만 | 의도 적용 | 다른 선택지 비교 |
| 검증 근거 | 텍스트만 | 수치 1개 | before/after + p95 |
| 설명력 | 정보 부족 | 의도 전달 | 팀원이 읽고 바로 이해 |

> 상세는 `bootcamp-admin/docs/bootcamp/review-rubric.md`

---

# 이번 주 운영 안내

- **제출 마감**: {{2026-MM-DD}} `23:59` (KST)
- **금 18:00**: 토요일 행사 1장 슬라이드 제출 마감 (해당 주차 발표자)
- **토 15:00–16:30**: {{강의 / 내부 발표}} — {{주제 또는 발표자}}
- **오피스아워**: 화·목 `21:00` `{cohort}-질문` 채널 스레드

---

<!-- _class: end -->

# Q&A

질문 환영 — 이번 주 mission-guard 가 막히면 즉시 `{cohort}-질문` 채널.

> 다음 주: **Week {{NN+1}} — {{다음 퀘스트 제목}}**
