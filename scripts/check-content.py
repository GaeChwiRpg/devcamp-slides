#!/usr/bin/env python3
"""Slide code block + table cell width check.

Marp 슬라이드의 _wrap 안 되는_ 요소(코드 블록, 표 cell)가 슬라이드 폭에
들어가는지 검증한다. 한글 = 2 EAW, 영문 = 1 EAW.

검사 대상:
  - 코드 블록 (```...```)  내부 라인
  - 표 cell                 내용 (각 셀 내부, `|` 제거 후)

임계치 (1280px 본문 1120px / 모노스페이스 ~12px / 폰트 20px 기준):
  - 일반 슬라이드 코드:        ≤ 70 EAW
  - lesson class (양분할) 코드: ≤ 45 EAW
  - 일반 슬라이드 표 cell:      ≤ 60 EAW
  - lesson class 표 cell:       ≤ 36 EAW

폭 초과 시 exit 1 — build.sh 가 호출하면 빌드 중단.
"""
import re
import sys
import unicodedata
from pathlib import Path

LIMIT = {
    ("code", "normal"): 70,
    ("code", "lesson"): 52,   # 17px monospace × 약 52자
    ("table", "normal"): 60,
    ("table", "lesson"): 42,  # 19px × 약 42자
}

SLIDE_DIRS = ("weekly-kickoff", "lecture", "offline", "templates")
EXCLUDE_SUFFIX = ("-notes.md",)


def eaw_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in ("F", "W") else 1 for c in s)


def visible_cell(raw: str) -> str:
    # 마크다운 강조 제거 (시각 폭에 큰 영향 없음, backtick 은 코드 모노 표시 — 폭 비슷)
    return re.sub(r"[`_*]", "", raw).strip()


def check_file(path: Path) -> list[tuple[int, str, int, int, str, str]]:
    """Returns list of (lineno, kind, width, limit, class, content) for failures."""
    errs: list[tuple[int, str, int, int, str, str]] = []
    in_code_block = False
    current_class: str | None = None
    cls_re = re.compile(r"^<!--\s*_class:\s*(\w+)\s*-->\s*$")
    fence_re = re.compile(r"^[ \t]*(```|~~~)")

    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        # 슬라이드 구분자 → 새 슬라이드 → class / code block 리셋
        if line.strip() == "---" and lineno > 1 and not in_code_block:
            current_class = None
            continue

        # 코드 블록 토글
        if fence_re.match(line):
            in_code_block = not in_code_block
            continue

        # class 마커
        m_cls = cls_re.match(line.strip())
        if m_cls:
            current_class = m_cls.group(1)
            continue

        cls_key = "lesson" if current_class == "lesson" else "normal"

        # 코드 블록 내부
        if in_code_block:
            content = line.rstrip()
            w = eaw_width(content)
            limit = LIMIT[("code", cls_key)]
            if w > limit:
                errs.append((lineno, "code", w, limit, current_class or "normal", content))
            continue

        # 표 라인 — `|` 로 시작하고 끝
        s = line.strip()
        if s.startswith("|") and s.endswith("|") and not re.match(r"^\|[\s:|-]+\|$", s):
            # 셀 분리 (양 끝 | 제외)
            cells = [c.strip() for c in s[1:-1].split("|")]
            limit = LIMIT[("table", cls_key)]
            for cell in cells:
                w = eaw_width(visible_cell(cell))
                if w > limit:
                    errs.append((lineno, "table", w, limit, current_class or "normal", cell))

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
            print(f"\n[ FAIL ] {f.relative_to(root)}")
            for ln, kind, w, lim, cls, content in errs:
                short = content if len(content) <= 80 else content[:77] + "..."
                print(f"  L{ln}  {kind}  width={w} > {lim} ({cls})  {short!r}")
            failed = True

    if failed:
        print(
            f"\n⚠️  슬라이드 폭 초과 — 잘림 위험. 한도:\n"
            f"     코드 일반 ≤{LIMIT[('code','normal')]} / lesson ≤{LIMIT[('code','lesson')]}\n"
            f"     표 일반 ≤{LIMIT[('table','normal')]} / lesson ≤{LIMIT[('table','lesson')]}\n"
            "    한글 1자=2폭. 코드는 줄바꿈 또는 단축, 표는 셀 분리."
        )
        return 1
    print(f"[  OK  ] 모든 코드/표 폭 OK ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
