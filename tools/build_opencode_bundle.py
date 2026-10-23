#!/usr/bin/env python3
"""Build self-contained public skills without traversing outside the active skill."""

from runtime_bundle import ROOT, build_bundle

DIST_DIR = ROOT / "dist/opencode-polylens"


def main() -> int:
    build_bundle(DIST_DIR, nested=True)
    print(f"Built OpenCode bundle at {DIST_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
