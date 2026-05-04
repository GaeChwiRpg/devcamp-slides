#!/usr/bin/env python3
"""Slide content consistency check.

슬라이드 본문에 _금지 단어_ 또는 _옛 표기_ 가 남아있지 않은지 + 미션 ID 가
catalog 와 일치하는지 검증한다. build.sh 에서 호출되며 실패 시 빌드 중단.

검사:
  1. 금지 단어 — 진급 게이트 / 라이브 데모 / 라이브 시연 / 특강 / JDK 17 /
                fork + clone / 새 Spring Boot 프로젝트 생성 등
  2. 옛 Discord 채널 — `#help`, `#oh`, `#submissions`, `#env`, `#alumni`
  3. 미션 ID — 슬라이드에 등장하는 정식 missionId 패턴이 mission-catalog.ts 에 있는지
"""
import re
import sys
from pathlib import Path

SLIDE_DIRS = ("weekly-kickoff", "lecture", "offline", "templates")
EXCLUDE_SUFFIX = ("-notes.md",)

# (정규식, 사유, 권장 대체)
FORBIDDEN: list[tuple[str, str, str]] = [
    (r"진급\s*게이트", "단어 금지", "통과 조건 / 분기점 / 이번 주 목표"),
    (r"라이브\s*데모", "발표에 라이브 데모 없음", "제출 흐름 / 시스템 흐름 설명"),
    (r"라이브로\s*시연", "발표에 라이브 데모 없음", "텍스트 설명"),
    (r"(?<!본인이\s)(?<!소수\s)(?<!자기\s)특강", "외부 초청 의미 → 정규 강의", "강의"),
    (r"JDK\s*17", "Spring Boot 3.3.5 매칭 — JDK 21", "JDK 21"),
    (r"fork\s*\+\s*clone", "학생 레포는 부트스트랩됨", "clone 만"),
    (r"새\s*Spring\s*Boot\s*프로젝트\s*생성", "이미 부트스트랩된 폴더에 작성", "본인 레포 mission 폴더에 코드 시작"),
    (r"#\s*help\b", "옛 Discord 표기", "`{cohort}-질문`"),
    (r"#\s*oh\b", "옛 Discord 표기", "`{cohort}-질문` 채널 스레드"),
    (r"#\s*submissions\b", "옛 Discord 표기", "`{cohort}-리뷰`"),
    (r"#\s*env\b", "옛 Discord 표기", "`{cohort}-질문`"),
    (r"#\s*alumni\b", "옛 Discord 표기", "`졸업생-라운지`"),
]

# missionId 정규 표기 (catalog 와 1:1)
VALID_MISSION_IDS = {
    "00-onboarding-sql-db-basics",
    "01-onboarding-git-basics",
    "02-week1-spring-boot",
    "03-week2-jpa",
    "04-week3-backend-resume",
    "05-week4-index",
    "06-week5-concurrency",
    "07-week6-profiling",
    "08-week7-redis",
    "09-week8-ai-native",
    "week9-team-project",
    "10-week10-interview",
}

# missionId 같이 보이는 (digit-week-...) 패턴 추출
MISSION_PAT = re.compile(r"\b(\d{2}-week\d+-[a-z0-9-]+|week9-team-project|10-week10-interview|0[01]-onboarding-[a-z-]+)\b")


def scan_file(path: Path) -> list[tuple[int, str, str, str]]:
    """Returns list of (lineno, kind, matched, hint)."""
    errs: list[tuple[int, str, str, str]] = []
    in_code_block = False
    fence_re = re.compile(r"^[ \t]*(```|~~~)")

    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        if fence_re.match(line):
            in_code_block = not in_code_block
            continue
        # 검사 자체는 코드 블록 안에서도 하되, missionId 는 정확성을 위해 본문만
        for pat, why, hint in FORBIDDEN:
            for m in re.finditer(pat, line, re.IGNORECASE):
                # `진급 게이트` 라는 _단어를 설명하는_ 메타 컨텍스트 (예: SKILL.md 에서 "❌ 진급 게이트" 로 사용)
                # 는 슬라이드 디렉토리 검사 대상이 아니므로 신경 X
                errs.append((lineno, "forbidden", m.group(0), f"{why} → {hint}"))

        # 미션 ID 정합성 (코드 블록 밖에서만)
        if not in_code_block:
            for m in MISSION_PAT.finditer(line):
                mid = m.group(1)
                if mid not in VALID_MISSION_IDS:
                    errs.append((lineno, "mission_id", mid, f"catalog 에 없음 — 정확한 ID 사용"))

    return errs


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    files: list[Path] = []
    for d in SLIDE_DIRS:
        files.extend(sorted((root / d).glob("*.md")))
    files = [f for f in files if not any(f.name.endswith(s) for s in EXCLUDE_SUFFIX)]

    failed = False
    for f in files:
        errs = scan_file(f)
        if errs:
            print(f"\n[ FAIL ] {f.relative_to(root)}")
            for ln, kind, matched, hint in errs:
                print(f"  L{ln}  {kind:10s}  {matched!r:32s}  {hint}")
            failed = True

    if failed:
        print("\n⚠️  슬라이드 내용 검수 실패. 위 사유에 따라 수정하세요.")
        return 1
    print(f"[  OK  ] 슬라이드 내용 검수 OK ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
