#!/usr/bin/env python3
"""Slide title width check.

Marp 슬라이드의 # / ## / ### 제목이 1280px 슬라이드에서 줄바꿈되지 않도록
East Asian Width 기반 폭을 검증한다. 한글 1자 = 2, 영문/숫자/기호 1자 = 1.

임계치 (보수적 — quest 클래스의 ::before "⚔ QUEST " prefix 도 고려):
  - H1 (cover/quest/일반 60-80px): 32 EAW (한글 16자)
  - H2 (40-44px):                  48 EAW (한글 24자)
  - H3 (28-32px):                  56 EAW (한글 28자)

폭 초과 시 exit 1 — build.sh 가 호출하면 빌드 중단된다.
"""
import re
import sys
import unicodedata
from pathlib import Path

LIMITS = {1: 32, 2: 48, 3: 56}
# cover/boss 클래스의 H1 은 80px 폰트 → 본문 폭 좁아 더 짧게
COVER_BOSS_H1_LIMIT = 24

# 검사 대상 디렉토리 (다른 마크다운은 건드리지 않음)
SLIDE_DIRS = ("weekly-kickoff", "lecture", "offline", "templates")
# 발표 노트 등 빌드되지 않는 파일은 제외
EXCLUDE_SUFFIX = ("-notes.md",)


def eaw_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in ("F", "W") else 1 for c in s)


def visible_title(raw: str) -> str:
    # 마크다운 강조 / 인라인 코드 backtick 제거 (시각 폭에는 영향 거의 없음)
    return re.sub(r"[`_*]", "", raw).strip()


def check_file(path: Path) -> list[tuple[int, int, int, str, int]]:
    """Returns list of (lineno, level, width, title, limit) for failures."""
    errs: list[tuple[int, int, int, str, int]] = []
    in_code_block = False
    current_class: str | None = None
    cls_re = re.compile(r"^<!--\s*_class:\s*(\w+)\s*-->\s*$")
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        # 슬라이드 구분자 (frontmatter 가 아닌 ---) → 새 슬라이드 → class 리셋
        if line.strip() == "---" and lineno > 1:
            current_class = None
            continue
        # ``` / ~~~ 코드 블록 토글
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # class 마커 추적
        m_cls = cls_re.match(line.strip())
        if m_cls:
            current_class = m_cls.group(1)
            continue
        # 제목
        m = re.match(r"^(#{1,3}) +(.+?)\s*$", line)
        if not m:
            continue
        level = len(m.group(1))
        title = visible_title(m.group(2))
        w = eaw_width(title)
        limit = LIMITS.get(level, 60)
        # quest 슬라이드의 H1 은 ::before "⚔ QUEST " (8폭) prefix 추가됨 → 한도 더 짧게
        if level == 1 and current_class == "quest":
            limit -= 8
        # cover / boss 클래스의 H1 은 80px 폰트 → 더 짧아야
        elif level == 1 and current_class in ("cover", "boss"):
            limit = COVER_BOSS_H1_LIMIT
        if w > limit:
            errs.append((lineno, level, w, title, limit))
    return errs


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    files: list[Path] = []
    for d in SLIDE_DIRS:
        files.extend(sorted((root / d).glob("*.md")))
    files = [f for f in files if not any(f.name.endswith(s) for s in EXCLUDE_SUFFIX)]

    failed = False
    for f in files:
        errs = check_file(f)
        if errs:
            rel = f.relative_to(root)
            print(f"\n[ FAIL ] {rel}")
            for ln, lv, w, t, lim in errs:
                print(f"  L{ln}  H{lv}  width={w} > {lim}   {t!r}")
            failed = True

    if failed:
        print(
            "\n⚠️  슬라이드 제목이 1줄에 안 들어갈 위험. "
            f"한도: H1≤{LIMITS[1]} / H2≤{LIMITS[2]} / H3≤{LIMITS[3]} (한글 1자=2폭). "
            "quest 클래스의 H1 은 추가로 -8 (⚔ QUEST prefix)."
        )
        return 1
    print(f"[  OK  ] 모든 슬라이드 제목 폭 OK ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
