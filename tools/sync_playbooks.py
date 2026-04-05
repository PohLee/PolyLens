#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PLAYBOOKS_DIR = ROOT / "prompts" / "playbooks"
BUNDLED_PLAYBOOKS_DIR = ROOT / "skills" / "shared" / "playbooks"
SOURCE_INDEX_PATH = ROOT / "prompts" / "shared-playbooks.md"
BUNDLED_INDEX_PATH = ROOT / "skills" / "shared" / "prompts" / "shared-playbooks.md"

HOOKS_DIR = ROOT / "skills" / "shared" / "hooks"
HARNESS_DIR = ROOT / "skills" / "shared" / "harness"

HOOK_SYNC_PAIRS = [
    (ROOT / "hooks" / "pre-analysis" / "inject-context.md", HOOKS_DIR / "pre-analysis" / "inject-context.md"),
    (ROOT / "hooks" / "pre-analysis" / "load-constraints.md", HOOKS_DIR / "pre-analysis" / "load-constraints.md"),
    (ROOT / "hooks" / "lens-select" / "force-lens.md", HOOKS_DIR / "lens-select" / "force-lens.md"),
    (ROOT / "hooks" / "review" / "add-framework.md", HOOKS_DIR / "review" / "add-framework.md"),
    (ROOT / "hooks" / "post-analysis" / "summarize.md", HOOKS_DIR / "post-analysis" / "summarize.md"),
]

HARNESS_SYNC_PAIRS = [
    (ROOT / "harness" / "orchestration.md", HARNESS_DIR / "orchestration.md"),
    (ROOT / "harness" / "reasoning.md", HARNESS_DIR / "reasoning.md"),
    (ROOT / "harness" / "validation.md", HARNESS_DIR / "validation.md"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def bundled_index_text() -> str:
    return read_text(SOURCE_INDEX_PATH).replace("prompts/playbooks/", "../playbooks/")


def sync_file_pairs(pairs: list[tuple[Path, Path]]) -> tuple[list[str], list[str], list[str]]:
    copied: list[str] = []
    removed: list[str] = []
    unchanged: list[str] = []

    source_files = {src.name: src for src, _ in pairs}
    bundled_files = {dst.name: dst for _, dst in pairs}

    for name, source_path in source_files.items():
        bundled_path = bundled_files[name]
        bundled_path.parent.mkdir(parents=True, exist_ok=True)
        if not bundled_path.exists() or source_path.read_bytes() != bundled_path.read_bytes():
            shutil.copyfile(source_path, bundled_path)
            copied.append(name)
        else:
            unchanged.append(name)

    for name, bundled_path in bundled_files.items():
        if name not in source_files:
            bundled_path.unlink()
            removed.append(name)

    return copied, removed, unchanged


def sync_playbooks() -> tuple[list[str], list[str], list[str], bool, list[str], list[str], list[str], list[str], list[str], list[str]]:
    copied: list[str] = []
    removed: list[str] = []
    unchanged: list[str] = []

    BUNDLED_PLAYBOOKS_DIR.mkdir(parents=True, exist_ok=True)
    BUNDLED_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    source_files = {path.name: path for path in sorted(SOURCE_PLAYBOOKS_DIR.glob("*.md"))}
    bundled_files = {path.name: path for path in sorted(BUNDLED_PLAYBOOKS_DIR.glob("*.md"))}

    for name, source_path in source_files.items():
        bundled_path = BUNDLED_PLAYBOOKS_DIR / name
        if not bundled_path.exists() or source_path.read_bytes() != bundled_path.read_bytes():
            shutil.copyfile(source_path, bundled_path)
            copied.append(name)
        else:
            unchanged.append(name)

    for name, bundled_path in bundled_files.items():
        if name not in source_files:
            bundled_path.unlink()
            removed.append(name)

    new_index_text = bundled_index_text()
    index_changed = not BUNDLED_INDEX_PATH.exists() or read_text(BUNDLED_INDEX_PATH) != new_index_text
    if index_changed:
        write_text(BUNDLED_INDEX_PATH, new_index_text)

    hook_copied, hook_removed, hook_unchanged = sync_file_pairs(HOOK_SYNC_PAIRS)
    harness_copied, harness_removed, harness_unchanged = sync_file_pairs(HARNESS_SYNC_PAIRS)

    return copied, removed, unchanged, index_changed, hook_copied, hook_removed, hook_unchanged, harness_copied, harness_removed, harness_unchanged


def check_playbooks() -> int:
    expected_index = bundled_index_text()
    errors: list[str] = []

    source_files = {path.name: path for path in sorted(SOURCE_PLAYBOOKS_DIR.glob("*.md"))}
    bundled_files = {path.name: path for path in sorted(BUNDLED_PLAYBOOKS_DIR.glob("*.md"))}

    if set(source_files) != set(bundled_files):
        missing = sorted(set(source_files) - set(bundled_files))
        extra = sorted(set(bundled_files) - set(source_files))
        if missing:
            errors.append(f"missing bundled playbooks: {', '.join(missing)}")
        if extra:
            errors.append(f"extra bundled playbooks: {', '.join(extra)}")

    for name, source_path in source_files.items():
        bundled_path = BUNDLED_PLAYBOOKS_DIR / name
        if bundled_path.exists() and source_path.read_bytes() != bundled_path.read_bytes():
            errors.append(f"bundled playbook differs: {name}")

    if not BUNDLED_INDEX_PATH.exists():
        errors.append(f"missing bundled index: {BUNDLED_INDEX_PATH.relative_to(ROOT)}")
    elif read_text(BUNDLED_INDEX_PATH) != expected_index:
        errors.append(f"bundled index differs: {BUNDLED_INDEX_PATH.relative_to(ROOT)}")

    if errors:
        print("Playbook bundle is out of sync:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print("Run `python3 tools/sync_playbooks.py` to fix it.", file=sys.stderr)
        return 1

    print("Playbook bundle is in sync.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync source playbooks into the bundled runtime tree."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero when bundled playbooks or the bundled playbook index are out of sync.",
    )
    args = parser.parse_args()

    if args.check:
        return check_playbooks()

    copied, removed, unchanged, index_changed, hook_copied, hook_removed, hook_unchanged, harness_copied, harness_removed, harness_unchanged = sync_playbooks()
    print(f"Synced {len(copied) + len(unchanged)} playbooks from {SOURCE_PLAYBOOKS_DIR.relative_to(ROOT)}.")
    if copied:
        print(f"Updated: {', '.join(copied)}")
    if removed:
        print(f"Removed stale bundled files: {', '.join(removed)}")
    if index_changed:
        print(f"Updated bundled index: {BUNDLED_INDEX_PATH.relative_to(ROOT)}")

    total_hooks = len(hook_copied) + len(hook_unchanged)
    print(f"Synced {total_hooks} hooks.")
    if hook_copied:
        print(f"Updated hooks: {', '.join(hook_copied)}")
    if hook_removed:
        print(f"Removed stale bundled hooks: {', '.join(hook_removed)}")

    total_harness = len(harness_copied) + len(harness_unchanged)
    print(f"Synced {total_harness} harness files.")
    if harness_copied:
        print(f"Updated harness: {', '.join(harness_copied)}")
    if harness_removed:
        print(f"Removed stale bundled harness: {', '.join(harness_removed)}")

    if not copied and not removed and not index_changed and not hook_copied and not hook_removed and not harness_copied and not harness_removed:
        print("No changes needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())