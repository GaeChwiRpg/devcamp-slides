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
    npx marp --pdf  -I "$d" -o "dist/$d"
    npx marp --html -I "$d" -o "dist/$d"
  else
    echo "==> Skip $d (no .md)"
  fi
done

echo "Done. Output: dist/"
ls -la dist/ 2>/dev/null || true
