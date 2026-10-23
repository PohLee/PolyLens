#!/usr/bin/env python3
"""Build the standard sibling-layout release from the authoritative resource manifest."""

from runtime_bundle import ROOT, build_bundle

DIST_DIR = ROOT / "dist/standard-polylens"


def main() -> int:
    build_bundle(DIST_DIR, nested=False)
    print(f"Built standard bundle at {DIST_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
