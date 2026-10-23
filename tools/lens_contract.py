"""Generate mode-specific projections from the authoritative Markdown lens registry."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("focus", "domains", "triggers", "owns_decisions", "veto_on", "pairs_with", "default", "active", "bias", "verdict_style")
PROJECTION_TARGETS = ("orchestrators/polylens-executive-review.md", "orchestrators/polylens-pre-fight.md", "skills/polylens-lens-review/SKILL.md")
PROJECTION_SOURCES = ("prompts/lens-registry.md", "prompts/project-context.md", *PROJECTION_TARGETS)


def parse_registry(text: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    """Return only a valid Registry; authoring errors never reach a generator."""
    sections = list(re.finditer(r"^##[ \t]+Lenses[ \t]*$", text, re.MULTILINE))
    if len(sections) != 1:
        raise ValueError("Expected one Lenses section heading")
    text = text[sections[0].end():]
    end = re.search(r"^##[ \t]+", text, re.MULTILINE)
    text = text[:end.start()] if end else text
    headings = list(re.finditer(r"^#{3,6}[^\n]*$", text, re.MULTILINE))
    if not headings:
        raise ValueError("Registry contains no lens entries")
    order, entries = [], {}
    names = []
    for heading in headings:
        match = re.fullmatch(r"###[ \t]+([A-Z][A-Za-z]*)[ \t]+—[ \t]+\S[^\n]*", heading.group())
        if match is None:
            raise ValueError(f"Malformed lens heading: {heading.group()}")
        names.append(match.group(1))
    for index, heading in enumerate(headings):
        name = names[index]
        if name in entries:
            raise ValueError(f"Duplicate lens ID: {name}")
        block = text[heading.end():headings[index + 1].start() if index + 1 < len(headings) else len(text)]
        fields = {}
        for key in FIELDS:
            values = re.findall(rf"^- \*\*{key}:\*\*[ \t]*([^\n]*)$", block, re.MULTILINE)
            if len(values) != 1 or not values[0].strip():
                raise ValueError(f"{name}: require one nonempty {key} field")
            fields[key] = values[0].strip()
        for key in ("active", "default"):
            if fields[key] not in ("true", "false"):
                raise ValueError(f"{name}: {key} must be true or false")
        order.append(name)
        entries[name] = fields
    for name, fields in entries.items():
        for pair in fields["pairs_with"].split(","):
            if pair.strip() not in entries:
                raise ValueError(f"{name}: unknown pairs_with lens '{pair.strip()}'")
    return order, entries


def _region(text: str, name: str) -> tuple[int, int]:
    begin, end = f"<!-- BEGIN {name} -->", f"<!-- END {name} -->"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ValueError(f"Expected one paired {name} region")
    start, stop = text.index(begin) + len(begin), text.index(end)
    if start > stop:
        raise ValueError(f"Reversed {name} region")
    return start, stop


def _replace_region(text: str, name: str, content: str) -> str:
    start, stop = _region(text, name)
    return text[:start] + "\n" + content.strip() + "\n" + text[stop:]


def project_documents(sources: Mapping[str, str]) -> dict[str, str]:
    """Project captured source texts; filesystem and release callers share this contract."""
    registry = sources["prompts/lens-registry.md"]
    order, entries = parse_registry(registry)
    start, stop = _region(registry, "SELECTION CONTRACT")
    algorithm = registry[start:stop].strip()
    if not algorithm:
        raise ValueError("Empty SELECTION CONTRACT region")
    documents = {}
    for relative in PROJECTION_TARGETS:
        text = sources[relative]
        text = _replace_region(text, "GENERATED SELECTION", algorithm)
        if "pre-fight" in relative:
            context = sources["prompts/project-context.md"].strip()
            text = _replace_region(text, "GENERATED CONTEXT", context)
            metadata = [f"- {name}: " + "; ".join(f"{key}: {entries[name][key]}" for key in FIELDS if key != "verdict_style") for name in order]
            briefs = [f"- {name} brief: {entries[name]['verdict_style']}. Bias: {entries[name]['bias']}." for name in order]
            content = "### Selection Metadata\n\n<!-- Generated from prompts/lens-registry.md; edit the source, then sync. -->\n" + "\n".join(metadata) + "\n\n### Lens Briefs\n\n" + "\n".join(briefs)
            text = _replace_region(text, "GENERATED LENSES", content)
        documents[relative] = text
    return documents


def projected_documents(root: Path = ROOT) -> dict[Path, str]:
    sources = {relative: (root / relative).read_text(encoding="utf-8") for relative in PROJECTION_SOURCES}
    return {root / relative: text for relative, text in project_documents(sources).items()}


def projection_errors(root: Path = ROOT) -> list[str]:
    return [f"stale generated lens contract: {path.relative_to(root).as_posix()} (run tools/sync_playbooks.py)" for path, expected in projected_documents(root).items() if path.read_text(encoding="utf-8") != expected]


def sync_projections(root: Path = ROOT) -> None:
    for path, expected in projected_documents(root).items():
        path.write_text(expected, encoding="utf-8", newline="\n")
