#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${1:-${OPENCODE_SKILLS_DIR:-$HOME/.config/opencode/skills}}"
BUNDLE_DIR="$ROOT_DIR/dist/opencode-polylens"

python3 "$ROOT_DIR/tools/build_opencode_bundle.py"

mkdir -p "$TARGET_DIR"
rm -rf "$TARGET_DIR/polylens" "$TARGET_DIR/polylens-lens-review"
cp -R "$BUNDLE_DIR/polylens" "$TARGET_DIR/"
cp -R "$BUNDLE_DIR/polylens-lens-review" "$TARGET_DIR/"

test -f "$TARGET_DIR/polylens/shared/orchestrators/polylens-pre-fight.md"
test -f "$TARGET_DIR/polylens/shared/orchestrators/polylens-executive-review.md"
test -f "$TARGET_DIR/polylens-lens-review/shared/prompts/lens-registry.md"

echo "Installed PolyLens for OpenCode into $TARGET_DIR"
echo "Bundle source: $BUNDLE_DIR"
echo "Verified nested shared runtime assets for polylens and polylens-lens-review"