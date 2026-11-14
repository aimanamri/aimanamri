#!/usr/bin/env bash
# Rebuild the README's pixel art (../assets/*.gif and *-still.png) from the generators in this folder.
#
# Requirements: Node 20+, Python 3.9+ (standard library only), git when PIXELBOLT is unset.
#
#   bash art/build.sh                                              # fetches Pixelbolt into art/.pixelbolt
#   PIXELBOLT=/path/to/Pixelbolt/bin/pixelbolt.js bash art/build.sh   # or use a checkout you already have
#
# Each generator (hero, factory, data, kb, mech) writes a Pixelbolt recipe to art/out/ (gitignored); Pixelbolt then
# renders it to a looping GIF plus a still frame that the README shows when the reader prefers reduced motion.
set -euo pipefail
ART="$(cd "$(dirname "$0")" && pwd)"
ASSETS="$ART/../assets"
OUT="$ART/out"
PIXELBOLT_REPO="${PIXELBOLT_REPO:-https://github.com/skulitom/Pixelbolt}"
PIXELBOLT_COMMIT=04eac1904b1f3d6dfba1ee1f149f5d846392f002   # the Pixelbolt the art was made with

if [ -z "${PIXELBOLT:-}" ]; then
  dir="$ART/.pixelbolt"
  if [ ! -f "$dir/.git/HEAD" ] || [ "$(git -C "$dir" rev-parse HEAD 2>/dev/null)" != "$PIXELBOLT_COMMIT" ]; then
    echo "fetching Pixelbolt ${PIXELBOLT_COMMIT:0:7} into $dir"
    rm -rf "$dir"
    git init -q "$dir"
    git -C "$dir" remote add origin "$PIXELBOLT_REPO"
    git -C "$dir" fetch -q --depth 1 origin "$PIXELBOLT_COMMIT" || git -C "$dir" fetch -q origin
    git -C "$dir" -c advice.detachedHead=false checkout -q "$PIXELBOLT_COMMIT"
  fi
  PIXELBOLT="$dir/bin/pixelbolt.js"
fi

PY="${PYTHON:-python3}"
"$PY" "$ART/toolkit.py"   # toolkit pills -> assets/toolkit/*.svg
"$PY" "$ART/buttons.py"   # header buttons -> assets/buttons/*.svg
rm -rf "$OUT"; mkdir -p "$OUT" "$ASSETS"
export OUT

# name:scale  (logo is wide, so it gets a smaller scale)
for spec in hero:3 factory:4 data:4 kb:4 mech:4; do
  name="${spec%%:*}"; scale="${spec##*:}"
  (cd "$ART" && "$PY" "$name.py")
  node "$PIXELBOLT" gif "$OUT/$name.json" --out "$ASSETS/$name.gif" --scale "$scale" --force >/dev/null
  node "$PIXELBOLT" render "$OUT/$name.json" --out "$OUT/$name-render" --scale "$scale" >/dev/null
  cp "$OUT/$name-render/frames/f000.png" "$ASSETS/$name-still.png" 2>/dev/null ||
    cp "$(ls "$OUT/$name-render"/frames/*.png | head -1)" "$ASSETS/$name-still.png"
  echo "built $name"
done
