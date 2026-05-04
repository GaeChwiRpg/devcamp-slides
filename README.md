# 딩코딩코 부트캠프 발표 슬라이드

> DEVELOPER RPG 톤의 Marp 슬라이드 모음. 매주 토요일 라이브 + 첫·마지막 오프라인 모임용.

## 무엇이 들어있나

| 디렉토리 | 용도 | 발표자 |
| --- | --- | --- |
| `weekly-kickoff/` | 매주 토 14:00–15:00 미션 공개·주간 방향 (10세트) | 총괄 |
| `lecture/` | 격주 토 15:00–16:30 강의 (2/4/6/8주차, 4세트) | 총괄 직접 |
| `offline/` | 첫·마지막 오프라인 모임 OT/피날레 | 총괄 |
| `templates/` | 위 3종 표준 템플릿 (복제해서 채워넣기) | — |
| `theme/` | DEVELOPER RPG Marp 테마 + 로고/픽셀 아이콘 | — |

학생 발표(3·5·7·9주차 내부 발표, 9·10주차 팀 발표)는 별도 — 운영 가이드는 [bootcamp-admin/docs/bootcamp/presentations.md](https://github.com/dingcodingco/bootcamp-admin/blob/main/docs/bootcamp/presentations.md) 참고.

## 빠르게 보기

PDF 산출물은 GitHub Pages 에서 바로 열람:

- 사이트: https://gaechwirpg.github.io/devcamp-slides/
- Release artifact: [Releases](https://github.com/GaeChwiRpg/devcamp-slides/releases)

## 로컬 빌드

```bash
# 처음 1회
npm install

# 전체 빌드 (PDF + HTML)
npm run build

# 단일 파일 빌드
npm run build:one weekly-kickoff/week01.md

# 라이브 미리보기 (편집하면서 자동 새로고침)
npm run watch
```

## 새 슬라이드 만들기 (매주 30분 워크플로우)

1. 템플릿 복제
   ```bash
   cp templates/_kickoff-template.md weekly-kickoff/weekNN.md
   ```
2. 표지의 `Week N` / `mission_id` 채우기 (`bootcamp-admin/src/lib/mission-catalog.ts` 참조)
3. 학습 목표 3가지 (`bootcamp-admin/docs/bootcamp/curriculum.md` 그대로 복사)
4. 핵심 개념 카드 5–7장
5. evidence 체크리스트 (`devcamp-submission-sample/<missionId>/README.md` "이번 주에 제출할 것" 그대로)
6. 푸시 → CI 가 PDF 빌드 → 발표

## 디자인 톤 — DEVELOPER RPG

- 컬러: 딥 네이비 `#0d1138` + 골드 `#f4c84b`
- 매주 = 퀘스트 / W10 = FINAL BOSS
- 폰트: Galmuri11 (한글 픽셀, OFL) + Pretendard (본문)

테마 상세는 [`theme/rpg.css`](theme/rpg.css) 참고.

## 주차별 PDF 인덱스

> CI 빌드 후 자동 갱신. 진행에 따라 채워짐.

| 주차 | 미션 | 매주 슬롯 | 강의 | 비고 |
| --- | --- | --- | --- | --- |
| 1 | `02-week1-spring-boot` | TBD | — | 5/30 OT 동시 |
| 2 | `03-week2-jpa` | TBD | TBD | JPA 연관관계 |
| 3 | `04-week3-backend-resume` | TBD | — | 학생 내부 발표 |
| 4 | `05-week4-index` | TBD | TBD | 인덱스/EXPLAIN |
| 5 | `06-week5-concurrency` | TBD | — | 학생 내부 발표 |
| 6 | `07-week6-profiling` | TBD | TBD | 프로파일링 |
| 7 | `08-week7-redis` | TBD | — | 학생 내부 발표 |
| 8 | `09-week8-ai-native` | TBD | TBD | AI Native |
| 9 | `week9-team-project` | TBD | — | 학생 팀 발표 |
| 10 | `10-week10-interview` | — | — | 8/8 피날레 |

## 라이선스

- 슬라이드 본문: 부트캠프 운영 자산. 외부 활용 시 출처 표기.
- Marp 테마(`theme/rpg.css`): MIT 자유 활용.
- 폰트: Galmuri11(OFL), Pretendard(OFL).
