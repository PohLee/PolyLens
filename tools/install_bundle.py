#!/usr/bin/env python3
"""Install a verified bundle; never overwrite unowned directories or discard an old install."""

import argparse
import json
import shutil
import stat
import sys
import tempfile
import uuid
from pathlib import Path

from runtime_bundle import PUBLIC_SKILLS, build_bundle

MARKER = ".polylens-install.json"
OWNERSHIP = {"owner": "polylens", "schema": 1}


def install(target: Path, nested: bool) -> None:
    target = target.expanduser().absolute()
    entries = PUBLIC_SKILLS if nested else (*PUBLIC_SKILLS, "shared")
    for name in entries:
        path = target / name
        try:
            attributes = getattr(path.lstat(), "st_file_attributes", 0)
        except FileNotFoundError:
            attributes = 0
        if path.is_symlink() or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            raise ValueError(f"Refusing linked directory: {path}; inspect and move it manually first")
        if path.exists():
            try:
                owner = json.loads((path / MARKER).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                owner = None
            if owner != OWNERSHIP:
                raise ValueError(f"Refusing to replace unowned path: {path}; inspect and move the old directory first")

    target.mkdir(parents=True, exist_ok=True)
    backup = target / f".polylens-backup-{uuid.uuid4().hex}"
    moved = []
    installed = []
    with tempfile.TemporaryDirectory(prefix=".polylens-stage-", dir=target) as directory:
        stage = Path(directory)
        bundle = stage / "bundle"
        snapshot = build_bundle(bundle, nested)
        for name in entries:
            (bundle / name / MARKER).write_text(json.dumps(OWNERSHIP), encoding="utf-8")
        try:
            for name in entries:
                destination = target / name
                if destination.exists():
                    backup.mkdir(exist_ok=True)
                    destination.rename(backup / name)
                    moved.append(name)
                (bundle / name).rename(destination)
                installed.append(name)
            snapshot.verify(target)
        except Exception:
            for name in reversed(installed):
                shutil.rmtree(target / name)  # Only paths just installed by this invocation.
            for name in reversed(moved):
                (backup / name).rename(target / name)
            raise
    print(f"Installed verified PolyLens bundle into {target}")
    if moved:
        print(f"Previous files preserved at {backup}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--layout", choices=("standard", "opencode"), default="standard")
    args = parser.parse_args()
    try:
        install(args.target, args.layout == "opencode")
    except (OSError, ValueError) as error:
        print(f"Install failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
