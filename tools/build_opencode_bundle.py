#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS_DIR = ROOT / "skills"
SOURCE_SHARED_DIR = SOURCE_SKILLS_DIR / "shared"
DIST_DIR = ROOT / "dist" / "opencode-polylens"
PUBLIC_SKILLS = ("polylens", "polylens-lens-review")
MARKDOWN_SUFFIXES = {".md", ".markdown"}

SKILL_REWRITES = {
    "../shared/": "shared/",
}

SHARED_REWRITES = {
    "../shared/prompts/": "../prompts/",
    "../shared/engines/": "../engines/",
    "../shared/lenses/": "../lenses/",
    "../shared/orchestrators/": "../orchestrators/",
    "../shared/playbooks/": "../playbooks/",
}


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_dir(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, dirs_exist_ok=True)


def rewrite_text(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def build_public_skill(skill_name: str) -> None:
    skill_source = SOURCE_SKILLS_DIR / skill_name
    skill_dist = DIST_DIR / skill_name
    shared_dist = skill_dist / "shared"

    copy_dir(skill_source, skill_dist)
    copy_dir(SOURCE_SHARED_DIR, shared_dist)

    rewrite_text(skill_dist / "SKILL.md", SKILL_REWRITES)

    for path in shared_dist.rglob("*"):
        if path.is_file() and path.suffix.lower() in MARKDOWN_SUFFIXES:
            rewrite_text(path, SHARED_REWRITES)


def verify_bundle() -> None:
    required_files = [
        DIST_DIR / "polylens" / "SKILL.md",
        DIST_DIR / "polylens" / "shared" / "orchestrators" / "polylens-pre-fight.md",
        DIST_DIR / "polylens" / "shared" / "orchestrators" / "polylens-executive-review.md",
        DIST_DIR / "polylens-lens-review" / "SKILL.md",
        DIST_DIR / "polylens-lens-review" / "shared" / "prompts" / "lens-registry.md",
    ]

    missing = [path for path in required_files if not path.exists()]
    if missing:
        missing_text = ", ".join(str(path.relative_to(ROOT)) for path in missing)
        raise FileNotFoundError(f"OpenCode bundle build incomplete: missing {missing_text}")


def main() -> int:
    reset_dir(DIST_DIR)
    for skill_name in PUBLIC_SKILLS:
        build_public_skill(skill_name)
    verify_bundle()
    print(f"Built OpenCode bundle at {DIST_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())