#!/usr/bin/env python3
"""Slide overflow check.

슬라이드별 _콘텐츠 라인 수_ 가 화면 영역(720px - 패딩 130px = 약 590px)
안에 들어가는지 검증. 페이지 카운트 영역까지 침범하면 잘림 발생.

본문 폰트 26px / line-height 1.5 ≈ 39px 1줄. 590px / 39px ≈ 15 줄.
보수적으로 16 줄 한도 (제목 + 콘텐츠).

코드 블록은 17px(lesson) ~ 20px 으로 더 빽빽 → 줄당 0.7 가중치.
표는 19~22px → 1.0 가중치.
빈 줄 / 주석 / class 마커는 카운트 X.
"""
import re
import sys
from pathlib import Path

LIMIT_NORMAL = 18  # cover/end/quest/일반
LIMIT_LESSON = 17  # 양분할 grid 한쪽 cell 기준

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


def count_content_lines(slide_text: str) -> int:
    """렌더 시점의 _세로 라인 수_ 추정."""
    in_code = False
    lines = 0
    fence_re = re.compile(r"^[ \t]*(```|~~~)")
    cls_re = re.compile(r"^<!--\s*_(class|paginate|color|backgroundColor):.*-->\s*$")

    for raw in slide_text.split("\n"):
        line = raw.rstrip()
        # 코드 블록 fence — fence 자체도 1줄로 보이긴 함, 무시
        if fence_re.match(line):
            in_code = not in_code
            lines += 1
            continue
        if in_code:
            # 코드는 1줄당 1줄 (폰트 작아서 가중치는 좀 낮지만 보수)
            lines += 1
            continue
        # 빈 줄 — 카운트 X (마크다운 렌더 시 무시 또는 문단 간격)
        if not line.strip():
            continue
        # marp 마커 — 카운트 X
        if cls_re.match(line.strip()):
            continue
        # 표 행 — 1줄
        if line.strip().startswith("|"):
            lines += 1
            continue
        # 본문 / 제목 / blockquote / 리스트 — 모두 1줄
        lines += 1

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
            lines = count_content_lines(slide)
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
