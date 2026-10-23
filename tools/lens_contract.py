"""Generate mode-specific projections from the authoritative Markdown lens registry."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("focus", "domains", "triggers", "owns_decisions", "veto_on", "pairs_with", "default", "active", "bias", "verdict_style")


def parse_registry(text: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    headings = list(re.finditer(r"^###\s+([A-Z][A-Za-z]*)\s+—\s+.+$", text, re.MULTILINE))
    order, entries = [], {}
    for index, match in enumerate(headings):
        name = match.group(1)
        block = text[match.end():headings[index + 1].start() if index + 1 < len(headings) else len(text)]
        fields = {}
        for key in FIELDS:
            value = re.search(rf"- \*\*{key}:\*\*\s*(.+)", block)
            if value:
                fields[key] = value.group(1).strip()
        order.append(name)
        entries[name] = fields
    return order, entries


def projected_documents(root: Path = ROOT) -> dict[Path, str]:
    registry = (root / "prompts/lens-registry.md").read_text(encoding="utf-8")
    algorithm = registry.split("## Selection Algorithm (for orchestrator reference)\n", 1)[1].split("Example guidance:", 1)[0].strip()
    block = "<!-- BEGIN GENERATED SELECTION -->\n" + algorithm + "\n<!-- END GENERATED SELECTION -->"
    documents = {}
    for relative in ("orchestrators/polylens-executive-review.md", "orchestrators/polylens-pre-fight.md", "skills/polylens-lens-review/SKILL.md"):
        path = root / relative
        text = path.read_text(encoding="utf-8")
        if "<!-- BEGIN GENERATED SELECTION -->" in text:
            text, count = re.subn(r"<!-- BEGIN GENERATED SELECTION -->.*?<!-- END GENERATED SELECTION -->", lambda _: block, text, flags=re.DOTALL)
        else:
            pattern = r"(?<=\*\*If no lens was specified:\*\* )Select exactly one lens using this algorithm:\n.*?(?=\n\nAnnounce)" if "polylens-lens-review" in relative else r"(?<=\*\*If no lenses specified:\*\* )Run the selection algorithm:\n.*?(?=\n\nPricing guidance:)"
            text, count = re.subn(pattern, lambda _: "Apply the authoritative selection contract:\n\n" + block, text, flags=re.DOTALL)
        if count != 1:
            raise ValueError(f"Expected one generated selection section in {relative}")
        if "pre-fight" in relative:
            context = (root / "prompts/project-context.md").read_text(encoding="utf-8").strip()
            text, context_count = re.subn(r"<!-- BEGIN GENERATED CONTEXT -->.*?<!-- END GENERATED CONTEXT -->", lambda _: "<!-- BEGIN GENERATED CONTEXT -->\n" + context + "\n<!-- END GENERATED CONTEXT -->", text, flags=re.DOTALL)
            if context_count != 1:
                raise ValueError("Expected one embedded project context protocol in pre-fight")
            order, entries = parse_registry(registry)
            metadata = [f"- {name}: " + "; ".join(f"{key}: {entries[name][key]}" for key in FIELDS if key != "verdict_style") for name in order]
            briefs = [f"- {name} brief: {entries[name]['verdict_style']}. Bias: {entries[name]['bias']}." for name in order]
            text = text.split("### Selection Metadata", 1)[0] + "### Selection Metadata\n\n<!-- Generated from prompts/lens-registry.md; edit the source, then sync. -->\n" + "\n".join(metadata) + "\n\n### Lens Briefs\n\n" + "\n".join(briefs) + "\n"
        documents[path] = text
    return documents


def projection_errors(root: Path = ROOT) -> list[str]:
    return [f"stale generated lens contract: {path.relative_to(root).as_posix()} (run tools/sync_playbooks.py)" for path, expected in projected_documents(root).items() if path.read_text(encoding="utf-8") != expected]


def sync_projections(root: Path = ROOT) -> None:
    for path, expected in projected_documents(root).items():
        path.write_text(expected, encoding="utf-8", newline="\n")
