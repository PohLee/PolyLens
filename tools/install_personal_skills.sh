#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <skills-dir>" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$1"
BUNDLE_DIR="$ROOT_DIR/dist/standard-polylens"

python3 "$ROOT_DIR/tools/build_standard_bundle.py"

mkdir -p "$TARGET_DIR"
rm -rf "$TARGET_DIR/polylens" "$TARGET_DIR/polylens-lens-review" "$TARGET_DIR/shared"
cp -R "$BUNDLE_DIR/polylens" "$TARGET_DIR/"
cp -R "$BUNDLE_DIR/polylens-lens-review" "$TARGET_DIR/"
cp -R "$BUNDLE_DIR/shared" "$TARGET_DIR/"

test -f "$TARGET_DIR/polylens/SKILL.md"
test -f "$TARGET_DIR/polylens-lens-review/SKILL.md"
test -f "$TARGET_DIR/shared/orchestrators/polylens-pre-fight.md"
test -f "$TARGET_DIR/shared/prompts/lens-registry.md"

echo "Installed PolyLens bundle into $TARGET_DIR"
echo "Bundle source: $BUNDLE_DIR"
echo "Verified sibling runtime assets for polylens, polylens-lens-review, and shared"