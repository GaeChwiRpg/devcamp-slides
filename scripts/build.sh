#!/usr/bin/env bash
# Build all slides → dist/<section>/ (PDF + HTML).
# 빈 디렉토리는 자동 skip.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

mkdir -p dist

for d in weekly-kickoff tech-talk offline; do
  if compgen -G "$d/*.md" > /dev/null; then
    echo "==> Building $d/"
    mkdir -p "dist/$d"
    npx marp --pdf  -I "$d" -o "dist/$d" -P 1
    npx marp --html -I "$d" -o "dist/$d" -P 1
  else
    echo "==> Skip $d (no .md)"
  fi
done

# 발표 노트(*-notes.md)는 운영자 전용 — Pages 에 노출 안 함
echo "==> Stripping presenter notes (*-notes.*)"
find dist -type f \( -name "*-notes.html" -o -name "*-notes.pdf" \) -delete

# HTML 슬라이드의 ../theme/assets/logo.png 경로 해석을 위해 theme/ 미러링
echo "==> Mirroring theme/ → dist/theme/"
rm -rf dist/theme
cp -R theme dist/theme

echo "Done. Output: dist/"
find dist -type f -name "*.pdf" -o -name "*.html" | sort 2>/dev/null || true
