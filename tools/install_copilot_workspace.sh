#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE_DIR="${1:-$PWD}"
TARGET_DIR="$WORKSPACE_DIR/.github/skills"

bash "$ROOT_DIR/tools/install_personal_skills.sh" "$TARGET_DIR"

echo "Installed PolyLens for GitHub Copilot into $TARGET_DIR"
echo "If your workspace uses a custom skills location, add the matching directory to chat.skillsLocations."