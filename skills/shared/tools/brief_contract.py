"""Structure of standard multi-lens Decision Briefs, not a reasoning-quality judge.

Positions are isolated before sections are interpreted. Known section names define
logical ownership regardless of Markdown heading depth (plain headings also work).
This deliberately does not parse Pre-fight, concise, or arbitrary Markdown formats.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

POSITION_FIELDS = (
    "Verdict:", "Decision context impact:", "Lens domain impact:", "Decision framing:",
    "- Scope:", "- Timeline:", "- Resource:", "- Risk:", "- Success Criteria:",
    "- Assumptions / Unknowns:", "Key concerns:", "Key endorsements:", "Non-negotiables:",
)
SUMMARY = "EXECUTIVE ALIGNMENT REVIEW - COMPLETION SUMMARY"
SPLIT = "DECISION SPLIT (AWAITING USER INPUT)"
MAJOR = ("VERDICT ALIGNMENT", "CONFLICT MAP", "ALIGNED PLAN", "ASSUMPTIONS / UNKNOWNS", SUMMARY, SPLIT)
COMPLETION = ("FINAL DECISION", "KEY TRADEOFFS", "RISKS ACCEPTED", "MITIGATION PLAN", "DISSENTING OPINIONS", "CONFIDENCE LEVEL")
OPTIONS = ("OPTION A", "OPTION B")
SPLIT_CLOSING = ("What the user should answer", "What remains blocked until then")


def missing_position_fields(body: str) -> list[str]:
    """Shared by source Lens templates and actual positions; templates may use placeholders."""
    return [label for label in POSITION_FIELDS if not re.search(rf"^{re.escape(label)}", body, re.MULTILINE)]


def _values(body: str, label: str) -> list[str]:
    return re.findall(rf"^{re.escape(label)}:[ \t]*([^\n]*)$", body, re.MULTILINE)


@dataclass
class Position:
    name: str
    body: str

    @property
    def verdict(self) -> str | None:
        values = _values(self.body, "Verdict")
        return values[0].strip() if len(values) == 1 and values[0].strip() in ("GO", "MODIFY", "BLOCK") else None


@dataclass
class Section:
    name: str
    parent: str | None
    body: str = ""


@dataclass
class Brief:
    text: str
    positions: list[Position]
    sections: list[Section]
    issues: list[str]

    @property
    def headings(self) -> list[str]:
        return [section.name for section in self.sections]

    @property
    def verdicts(self) -> dict[str, str]:
        return {position.name: position.verdict for position in self.positions if position.verdict is not None}

    def _sections(self, name: str) -> list[Section]:
        return [section for section in self.sections if section.name == name]

    def contract(self) -> dict:
        headings = self.headings
        partial = SPLIT in headings
        required = ["VERDICT ALIGNMENT", "CONFLICT MAP", SPLIT] if partial else [
            "VERDICT ALIGNMENT", "CONFLICT MAP", "ALIGNED PLAN", "ASSUMPTIONS / UNKNOWNS", SUMMARY, *COMPLETION,
        ]
        missing = [name for name in required if name not in headings]
        issues = list(self.issues)
        names = [position.name for position in self.positions]
        if not 2 <= len(names) <= 4 or len(set(names)) != len(names):
            issues.append("Require 2-4 unique delimited lens positions")
        for position in self.positions:
            issues.extend(f"{position.name}: missing position field {label}" for label in missing_position_fields(position.body))
            for label in POSITION_FIELDS:
                if len(_values(position.body, label.rstrip(":"))) > 1:
                    issues.append(f"{position.name}: duplicate position field {label}")
            if position.verdict is None:
                issues.append(f"{position.name}: invalid or duplicate verdict")
        for name in set(headings):
            if len(self._sections(name)) > 1:
                issues.append(f"Duplicate section: {name}")
        for section in self.sections:
            if section.name in COMPLETION and section.parent != SUMMARY:
                issues.append(f"{section.name} must belong to {SUMMARY}")
            if section.name in OPTIONS and section.parent != SPLIT:
                issues.append(f"{section.name} must belong to {SPLIT}")
        if partial and any(name in headings for name in ("ALIGNED PLAN", SUMMARY, *COMPLETION)):
            issues.append("Pending decision must not present a completed brief")
        if partial:
            split_sections = self._sections(SPLIT)
            body = split_sections[0].body if len(split_sections) == 1 else ""
            for label in ("Decision needed", "Why escalation happened", *SPLIT_CLOSING):
                values = _values(body, label)
                if len(values) != 1 or not values[0].strip():
                    issues.append(f"Partial brief requires one nonempty {label}")
            for name in OPTIONS:
                options = [section for section in self._sections(name) if section.parent == SPLIT]
                for label in ("Supported by", "What changes", "Upside", "Downside"):
                    values = _values(options[0].body, label) if len(options) == 1 else []
                    if len(values) != 1 or not values[0].strip():
                        issues.append(f"{name} requires one nonempty {label}")
        return {"passed": not missing and not issues, "kind": "partial" if partial else "complete", "missing_sections": missing, "issues": issues}

    def consistency(self) -> dict:
        issues = list(self.issues)
        alignment_sections = self._sections("VERDICT ALIGNMENT")
        labels = _values(alignment_sections[0].body, "Alignment") if len(alignment_sections) == 1 else []
        verdicts = [position.verdict for position in self.positions]
        if not verdicts or None in verdicts or len(labels) != 1:
            issues.append("Missing, invalid or ambiguous lens verdicts or alignment label")
        else:
            expected = "UNANIMOUS" if len(set(verdicts)) == 1 else "ALL DISAGREE" if len(set(verdicts)) == len(verdicts) else "SPLIT"
            if labels[0].strip() != expected:
                issues.append(f"Initial verdicts require {expected} alignment")
        return {"passed": not issues, "issues": issues}

    def regression(self, baseline: Brief) -> dict:
        delta = {
            "sections_changed": [(s.name, s.parent) for s in self.sections] != [(s.name, s.parent) for s in baseline.sections],
            "verdicts_changed": self.verdicts != baseline.verdicts,
            "content_changed": " ".join(self.text.split()) != " ".join(baseline.text.split()),
        }
        return {"passed": not any(delta.values()) and not self.issues and not baseline.issues, "delta": delta}


def parse_brief(text: str) -> Brief:
    """Interpret one standard report. Ambiguous structure is reported, never guessed."""
    positions, sections, issues = [], [], []
    position = None
    current = None
    parent = None
    for line in text.splitlines():
        marker = re.fullmatch(r"---(BEGIN|END) ([A-Z][A-Za-z]*) POSITION---[ \t]*", line)
        if marker:
            kind, name = marker.groups()
            if kind == "BEGIN":
                if position is not None:
                    issues.append("Nested position delimiters")
                position = Position(name, "")
                positions.append(position)
                current = None
            elif position is None or position.name != name:
                issues.append("Unmatched position delimiters")
            else:
                position = None
            continue
        if line.startswith(("---BEGIN ", "---END ")):
            issues.append("Malformed position delimiter")
        if position is not None:
            position.body += line + "\n"
            continue
        if parent == SPLIT and current is not None and current.name in OPTIONS and any(
            line.startswith(label + ":") for label in SPLIT_CLOSING
        ):
            # Closing prompts end the option, so footer text cannot supply any
            # missing option fields. The template's footer belongs to the split.
            current = next(section for section in reversed(sections) if section.name == SPLIT)
        heading = re.fullmatch(r"(?:#{1,6}[ \t]+)?([A-Z][A-Z0-9 /()—-]+?)[ \t]*", line)
        name = heading.group(1) if heading else None
        if name in (*MAJOR, *COMPLETION, *OPTIONS):
            if name in MAJOR:
                parent = name
                owner = None
            else:
                owner = parent
            current = Section(name, owner)
            sections.append(current)
        elif re.match(r"^#{1,6}[ \t]+", line):
            current = None  # Unknown Markdown sections cannot lend their fields.
            parent = None
        elif current is not None:
            current.body += line + "\n"
    if position is not None:
        issues.append("Unmatched position delimiters")
    return Brief(text, positions, sections, issues)
