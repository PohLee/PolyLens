#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${1:-${OPENCODE_SKILLS_DIR:-$HOME/.config/opencode/skills}}"
python3 "$ROOT_DIR/tools/install_bundle.py" --target "$TARGET_DIR" --layout opencode
