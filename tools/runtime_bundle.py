"""One resource manifest for development mirrors and both release layouts."""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from lens_contract import parse_registry


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SKILLS = ("polylens", "polylens-lens-review")
RESOURCE_TREES = {
    "prompts": "prompts",
    "prompts/playbooks": "playbooks",
    "engines": "engines",
    "lenses": "lenses",
    "orchestrators": "orchestrators",
    "harness": "harness",
    "hooks": "hooks",
}


def runtime_files(root: Path = ROOT) -> dict[Path, str]:
    """Return all generated runtime files, relative to shared/."""
    files = {}
    for source, destination in RESOURCE_TREES.items():
        source_dir = root / source
        paths = source_dir.rglob("*.md") if source == "hooks" else source_dir.glob("*.md")
        for path in sorted(paths):
            content = path.read_text(encoding="utf-8")
            if path.name == "shared-playbooks.md":
                content = content.replace("prompts/playbooks/", "../playbooks/")
            files[Path(destination) / path.relative_to(source_dir)] = content
    files[Path("tools/harness.py")] = (root / "tools/harness.py").read_text(encoding="utf-8")
    files[Path("LICENSE")] = (root / "LICENSE").read_text(encoding="utf-8")
    return files


def write_runtime(destination: Path, root: Path = ROOT) -> None:
    for relative, content in runtime_files(root).items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")


def check_runtime(destination: Path, root: Path = ROOT) -> list[str]:
    expected = runtime_files(root)
    errors = []
    for relative, content in expected.items():
        target = destination / relative
        if not target.is_file() or target.read_text(encoding="utf-8") != content:
            errors.append(f"runtime file missing or out of sync: {relative.as_posix()}")
    actual = {p.relative_to(destination) for p in destination.rglob("*") if p.is_file() and p.suffix in (".md", ".py")}
    for relative in sorted(actual - expected.keys()):
        errors.append(f"unexpected runtime file (remove explicitly if obsolete): {relative.as_posix()}")
    return errors


def verify_bundle(destination: Path, nested: bool, root: Path = ROOT) -> None:
    """Check the dependency closure from each installed public skill."""
    references = re.compile(r"(?:\.\./shared/|shared/|\.\./(?:prompts|engines|lenses|orchestrators|playbooks|tools|harness|hooks)/)[^\s`\)\],;]+")
    for skill in PUBLIC_SKILLS:
        skill_dir = destination / skill
        shared = skill_dir / "shared" if nested else destination / "shared"
        for required in (skill_dir / "SKILL.md", *(shared / relative for relative in runtime_files(root))):
            if not required.is_file():
                raise ValueError(f"missing release dependency: {required}")
        order, entries = parse_registry((shared / "prompts/lens-registry.md").read_text(encoding="utf-8"))
        if not order or len(order) != len(set(order)):
            raise ValueError("Release registry must contain unique lens IDs")
        for name in order:
            brief = shared / "lenses" / f"lens-{name.lower()}.md"
            if not brief.is_file():
                raise ValueError(f"missing release lens dependency: {brief}")
            if any(entries[name].get(key) not in ("true", "false") for key in ("active", "default")):
                raise ValueError(f"invalid release lens boolean: {name}")
        for document in [skill_dir / "SKILL.md", *shared.rglob("*.md")]:
            for match in references.finditer(document.read_text(encoding="utf-8")):
                reference = match.group().rstrip(".:")
                if any(marker in reference for marker in ("<", "*")):
                    continue  # Parameterized lens/hook paths; inventory is checked separately.
                base = skill_dir if reference.startswith(("../shared/", "shared/")) else document.parent
                target = (base / reference).resolve()
                if not target.is_relative_to(destination.resolve()) or not target.exists():
                    raise ValueError(f"unresolved release reference in {document}: {reference}")


def build_bundle(destination: Path, nested: bool, root: Path = ROOT) -> None:
    """Build in a caller-owned output directory, never a user skills directory."""
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for skill in PUBLIC_SKILLS:
        shutil.copytree(root / "skills" / skill, destination / skill)
        if nested:
            path = destination / skill / "SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace("../shared/", "shared/"), encoding="utf-8")
            write_runtime(destination / skill / "shared", root)
            for document in (destination / skill / "shared").rglob("*.md"):
                document.write_text(document.read_text(encoding="utf-8").replace("../shared/", "../"), encoding="utf-8")
    if not nested:
        write_runtime(destination / "shared", root)
    verify_bundle(destination, nested, root)
