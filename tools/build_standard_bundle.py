#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS_DIR = ROOT / "skills"
DIST_DIR = ROOT / "dist" / "standard-polylens"
PUBLIC_ENTRIES = ("polylens", "polylens-lens-review", "shared")


def main() -> int:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    for entry in PUBLIC_ENTRIES:
        shutil.copytree(SOURCE_SKILLS_DIR / entry, DIST_DIR / entry)

    print(f"Built standard bundle at {DIST_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())