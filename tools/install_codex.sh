#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${1:-${CODEX_SKILLS_DIR:-$HOME/.codex/skills}}"

bash "$ROOT_DIR/tools/install_personal_skills.sh" "$TARGET_DIR"

echo "Installed PolyLens for Codex into $TARGET_DIR"