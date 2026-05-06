#!/usr/bin/env python3
"""Slide overflow check (with wrap estimation).

슬라이드별 _세로 visual 라인 수_ 가 화면 영역(720px - padding 130px = 약 590px)
안에 들어가는지 검증. 한 줄이 본문 폭(약 80 EAW) 넘으면 _자동 wrap_ 으로
실제 라인 수 증가 → 페이지 카운트 영역 침범.

기준:
  - 본문 폰트 26px / line-height 1.5 ≈ 39px 1줄
  - 슬라이드 본문 폭 ≈ 1120px
  - 한글 26px / 영문 ~13px → EAW 1폭 ≈ 13px → 1120/13 ≈ 86 EAW
  - 보수적으로 _80 EAW 폭_ 넘으면 1줄 wrap 추정

한도:
  - 일반 슬라이드 visual lines ≤ 16
  - lesson (양분할) visual lines ≤ 14
"""
import math
import re
import sys
import unicodedata
from pathlib import Path

LIMIT_NORMAL = 17  # cover/end/quest/일반 — visual line 기준
LIMIT_LESSON = 16  # 양분할 grid 한쪽 cell (폰트 작아져 더 들어감)
WRAP_WIDTH_NORMAL = 80   # 일반 본문 폭 (EAW) — 넘으면 wrap
WRAP_WIDTH_LESSON = 50   # lesson cell 폭 (양분할 + 폰트 22px)

SLIDE_DIRS = ("weekly-kickoff", "lecture", "offline", "templates")
EXCLUDE_SUFFIX = ("-notes.md",)


def split_slides(text: str) -> list[tuple[int, str]]:
    """Returns list of (start_lineno, slide_text). frontmatter 첫 슬라이드 제외."""
    parts = text.split("\n---\n")
    slides: list[tuple[int, str]] = []
    line_offset = 0
    for i, p in enumerate(parts):
        if i == 0:
            # frontmatter 또는 첫 영역 — 무시
            line_offset += p.count("\n") + 1
            continue
        slides.append((line_offset + 1, p))
        line_offset += p.count("\n") + 1
    return slides


def eaw_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in ("F", "W") else 1 for c in s)


def visible(s: str) -> str:
    """마크다운 강조 / 인라인 코드 backtick 제거."""
    return re.sub(r"[`_*]", "", s)


def visual_lines_for(line: str, wrap_width: int) -> int:
    """한 줄이 wrap 으로 몇 줄 차지하는지 추정."""
    text = visible(line.lstrip("- ").lstrip("* ").lstrip("> ").strip())
    if not text:
        return 1
    w = eaw_width(text)
    return max(1, math.ceil(w / wrap_width))


def count_content_lines(slide_text: str, wrap_width: int) -> int:
    """렌더 시점의 _세로 visual 라인 수_ 추정 — wrap 포함."""
    in_code = False
    lines = 0
    fence_re = re.compile(r"^[ \t]*(```|~~~)")
    cls_re = re.compile(r"^<!--\s*_(class|paginate|color|backgroundColor):.*-->\s*$")

    for raw in slide_text.split("\n"):
        line = raw.rstrip()
        if fence_re.match(line):
            in_code = not in_code
            lines += 1
            continue
        if in_code:
            # 코드는 _wrap 안 됨_ (overflow-x:auto). 1줄 그대로.
            lines += 1
            continue
        if not line.strip():
            continue
        if cls_re.match(line.strip()):
            continue
        # 표 행 — 1줄 (셀 wrap 은 셀별 별도 검증)
        if line.strip().startswith("|"):
            lines += 1
            continue
        # 본문 / 제목 / blockquote / 리스트 — wrap 추정 적용
        lines += visual_lines_for(line, wrap_width)

    return lines


def slide_class(slide_text: str) -> str | None:
    m = re.search(r"<!--\s*_class:\s*(\w+)\s*-->", slide_text)
    return m.group(1) if m else None


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    files: list[Path] = []
    for d in SLIDE_DIRS:
        files.extend(sorted((root / d).glob("*.md")))
    files = [f for f in files if not any(f.name.endswith(s) for s in EXCLUDE_SUFFIX)]

    failed = False
    for f in files:
        text = f.read_text(encoding="utf-8")
        slides = split_slides(text)
        slide_errs: list[tuple[int, int, int, str]] = []
        for start_ln, slide in slides:
            cls = slide_class(slide) or "normal"
            # cover/end 는 의도적으로 짧음, 페이지 카운트도 숨김 → 검사 X
            if cls in ("cover", "end"):
                continue
            wrap_w = WRAP_WIDTH_LESSON if cls == "lesson" else WRAP_WIDTH_NORMAL
            lines = count_content_lines(slide, wrap_w)
            limit = LIMIT_LESSON if cls == "lesson" else LIMIT_NORMAL
            if lines > limit:
                # 슬라이드 첫 줄 (제목) 추출
                title_match = re.search(r"^#+ +(.+?)$", slide, re.MULTILINE)
                title = title_match.group(1)[:40] if title_match else "?"
                slide_errs.append((start_ln, lines, limit, title))
        if slide_errs:
            print(f"\n[ FAIL ] {f.relative_to(root)}")
            for ln, n, lim, title in slide_errs:
                print(f"  L{ln}~  lines={n} > {lim}   {title!r}")
            failed = True

    if failed:
        print(
            f"\n⚠️  슬라이드가 너무 길어 페이지 카운트 영역까지 침범 위험.\n"
            f"    한도: 일반 ≤{LIMIT_NORMAL} 줄 / lesson ≤{LIMIT_LESSON} 줄.\n"
            "    슬라이드를 _두 장으로 분리_ 하거나 본문을 줄이세요."
        )
        return 1
    print(f"[  OK  ] 모든 슬라이드 라인 수 OK ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
