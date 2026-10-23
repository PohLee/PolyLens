"""One resource manifest for development mirrors and both release layouts."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from lens_contract import parse_registry, project_documents


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
    for name in ("harness.py", "brief_contract.py"):
        files[Path("tools") / name] = (root / "tools" / name).read_text(encoding="utf-8")
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


@dataclass(frozen=True)
class BundleSnapshot:
    """One captured release, reused for writing, both layouts and post-move checks."""

    nested: bool
    _files: tuple[tuple[Path, bytes], ...]

    def verify(self, destination: Path) -> None:
        for relative, content in self._files:
            path = destination / relative
            if not path.is_file():
                raise ValueError(f"missing release dependency: {path}")
            if path.read_bytes() != content:
                raise ValueError(f"release content mismatch: {path}")
        _verify_dependencies(destination, self.nested)


def _capture_bundle(nested: bool, root: Path) -> BundleSnapshot:
    runtime = runtime_files(root)
    public_files = {}
    sources = {relative.as_posix(): text for relative, text in runtime.items()}
    for skill in PUBLIC_SKILLS:
        source = root / "skills" / skill
        for path in sorted(source.rglob("*")):
            if path.is_file():
                relative = Path(skill) / path.relative_to(source)
                public_files[relative] = path.read_bytes()
                if path.suffix == ".md":
                    sources[(Path("skills") / relative).as_posix()] = public_files[relative].decode("utf-8").replace("\r\n", "\n")
    # Freshness must be a property of this capture, not an earlier disk read.
    for relative, expected in project_documents(sources).items():
        if sources[relative] != expected:
            raise ValueError(f"stale generated lens contract: {relative} (run tools/sync_playbooks.py)")
    files = {}
    for relative, content in public_files.items():
        if nested and relative.suffix == ".md":
            content = content.replace(b"../shared/", b"shared/")
        files[relative] = content
    for skill in PUBLIC_SKILLS:
        shared = Path(skill) / "shared" if nested else Path("shared")
        for relative, text in runtime.items():
            if nested and relative.suffix == ".md":
                text = text.replace("../shared/", "../")
            files[shared / relative] = text.encode("utf-8")
    return BundleSnapshot(nested, tuple(files.items()))


def _verify_dependencies(destination: Path, nested: bool) -> None:
    """Check concrete references using only the captured release on disk."""
    references = re.compile(r"(?:\.\./shared/|shared/|\.\./(?:prompts|engines|lenses|orchestrators|playbooks|tools|harness|hooks)/)[^\s`\)\],;]+")
    for skill in PUBLIC_SKILLS:
        skill_dir = destination / skill
        shared = skill_dir / "shared" if nested else destination / "shared"
        if not (skill_dir / "SKILL.md").is_file():
            raise ValueError(f"missing release entrypoint: {skill_dir}")
        order, _ = parse_registry((shared / "prompts/lens-registry.md").read_text(encoding="utf-8"))
        for name in order:
            brief = shared / "lenses" / f"lens-{name.lower()}.md"
            if not brief.is_file():
                raise ValueError(f"missing release lens dependency: {brief}")
        for document in [skill_dir / "SKILL.md", *shared.rglob("*.md")]:
            for match in references.finditer(document.read_text(encoding="utf-8")):
                reference = match.group().rstrip(".:")
                if any(marker in reference for marker in ("<", "*")):
                    continue  # Parameterized lens/hook paths; inventory is checked separately.
                base = skill_dir if reference.startswith(("../shared/", "shared/")) else document.parent
                target = (base / reference).resolve()
                if not target.is_relative_to(destination.resolve()) or not target.exists():
                    raise ValueError(f"unresolved release reference in {document}: {reference}")


def verify_bundle(destination: Path, nested: bool, root: Path = ROOT) -> None:
    """Compare an existing release with current source; builds retain their own snapshot."""
    _capture_bundle(nested, root).verify(destination)


def build_bundle(destination: Path, nested: bool, root: Path = ROOT) -> BundleSnapshot:
    """Build in a caller-owned output directory, never a user skills directory."""
    snapshot = _capture_bundle(nested, root)
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for relative, content in snapshot._files:
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    snapshot.verify(destination)
    return snapshot
