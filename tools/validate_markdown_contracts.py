#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REGISTRY_PATH = ROOT / "prompts" / "lens-registry.md"
OUTPUT_TEMPLATE_PATH = ROOT / "prompts" / "output-template.md"
COLLISION_PATH = ROOT / "engines" / "collision.md"
SYNTHESIS_PATH = ROOT / "engines" / "synthesis.md"
EXEC_REVIEW_PATH = ROOT / "skills" / "polylens-executive-review.md"
PRE_FIGHT_PATH = ROOT / "skills" / "polylens-pre-fight.md"
SKILLS_DIR = ROOT / "skills"


LENS_REQUIRED_FIELDS = [
    "Verdict:",
    "Decision context impact:",
    "Lens domain impact:",
    "Decision framing:",
    "- Scope:",
    "- Timeline:",
    "- Resource:",
    "- Risk:",
    "- Success Criteria:",
    "- Assumptions / Unknowns:",
    "Key concerns:",
    "Key endorsements:",
    "Non-negotiables:",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def parse_registry(text: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    headings = list(
        re.finditer(r"^###\s+([A-Z][A-Za-z]*)\s+—\s+.+$", text, flags=re.MULTILINE)
    )
    order: list[str] = []
    entries: dict[str, dict[str, str]] = {}

    for index, match in enumerate(headings):
        name = match.group(1)
        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[start:end]
        fields = {}
        for key in [
            "focus",
            "domains",
            "triggers",
            "pairs_with",
            "default",
            "active",
            "bias",
            "verdict_style",
        ]:
            field_match = re.search(rf"- \*\*{re.escape(key)}:\*\*\s*(.+)", block)
            if field_match:
                fields[key] = field_match.group(1).strip()
        order.append(name)
        entries[name] = fields

    return order, entries


def validate_registry(errors: list[str]) -> list[str]:
    text = read_text(REGISTRY_PATH)
    order, entries = parse_registry(text)

    require(bool(order), f"{REGISTRY_PATH.relative_to(ROOT)}: no lens entries found", errors)
    require(
        "Selection should be deterministic." in text,
        f"{REGISTRY_PATH.relative_to(ROOT)}: missing deterministic selection guidance",
        errors,
    )
    require(
        "Break ties deterministically" in text,
        f"{REGISTRY_PATH.relative_to(ROOT)}: missing tie-break rules",
        errors,
    )

    for lens_name in order:
        fields = entries[lens_name]
        for required_field in [
            "focus",
            "domains",
            "triggers",
            "pairs_with",
            "default",
            "active",
            "bias",
            "verdict_style",
        ]:
            require(
                required_field in fields,
                f"{REGISTRY_PATH.relative_to(ROOT)}: lens {lens_name} is missing field '{required_field}'",
                errors,
            )

    known_lenses = set(order)
    for lens_name, fields in entries.items():
        pairs = [item.strip() for item in fields.get("pairs_with", "").split(",") if item.strip()]
        for pair in pairs:
            require(
                pair in known_lenses,
                f"{REGISTRY_PATH.relative_to(ROOT)}: lens {lens_name} references unknown pairs_with lens '{pair}'",
                errors,
            )

    active_lenses = [name for name, fields in entries.items() if fields.get("active") == "true"]
    return active_lenses


def validate_lens_skill(lens_name: str, errors: list[str]) -> None:
    skill_path = SKILLS_DIR / f"lens-{lens_name.lower()}" / "SKILL.md"
    require(skill_path.exists(), f"missing lens skill: {skill_path.relative_to(ROOT)}", errors)
    if not skill_path.exists():
        return

    text = read_text(skill_path)
    require(
        f"---BEGIN {lens_name} POSITION---" in text,
        f"{skill_path.relative_to(ROOT)}: missing BEGIN position marker for {lens_name}",
        errors,
    )
    require(
        f"---END {lens_name} POSITION---" in text,
        f"{skill_path.relative_to(ROOT)}: missing END position marker for {lens_name}",
        errors,
    )

    for required_field in LENS_REQUIRED_FIELDS:
        require(
            required_field in text,
            f"{skill_path.relative_to(ROOT)}: missing '{required_field}' in lens output contract",
            errors,
        )


def validate_skill_inventory(active_lenses: list[str], errors: list[str]) -> None:
    lens_dirs = sorted(
        path.name for path in SKILLS_DIR.iterdir() if path.is_dir() and path.name.startswith("lens-")
    )
    expected_dirs = sorted(f"lens-{name.lower()}" for name in active_lenses)
    require(
        lens_dirs == expected_dirs,
        (
            f"skills inventory mismatch: expected {expected_dirs}, found {lens_dirs}. "
            "Update prompts/lens-registry.md or skills/lens-*/SKILL.md to restore parity."
        ),
        errors,
    )


def validate_output_template(errors: list[str]) -> None:
    text = read_text(OUTPUT_TEMPLATE_PATH)
    for required_text in [
        "Decision framing:",
        "- Scope:",
        "- Timeline:",
        "- Resource:",
        "- Risk:",
        "- Success Criteria:",
        "- Assumptions / Unknowns:",
        "ASSUMPTIONS / UNKNOWNS",
        "DECISION SPLIT (AWAITING USER INPUT)",
        "Use only the columns needed for the selected 2-4 lenses.",
        "Use this section only when the brief is complete and no user decision is still pending.",
    ]:
        require(
            required_text in text,
            f"{OUTPUT_TEMPLATE_PATH.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )


def validate_collision(errors: list[str]) -> None:
    text = read_text(COLLISION_PATH)
    for required_text in [
        "decision framing for Scope/Timeline/Resource/Risk/Success Criteria",
        "### Step 4: Deduplicate Conflicts",
        "CANONICAL CONFLICT LIST",
        "Near-match wording",
        "Alignment: [UNANIMOUS / SPLIT / ALL DISAGREE]",
    ]:
        require(
            required_text in text,
            f"{COLLISION_PATH.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )


def validate_synthesis(errors: list[str]) -> None:
    text = read_text(SYNTHESIS_PATH)
    for required_text in [
        "Use the structured decision-framing fields as the primary synthesis input.",
        "DECISION SPLIT (AWAITING USER INPUT)",
        "stop before producing a completed Section 5 dashboard",
        "ASSUMPTIONS / UNKNOWNS",
        "For 2-4 lenses, include one row per selected lens only.",
    ]:
        require(
            required_text in text,
            f"{SYNTHESIS_PATH.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )


def validate_orchestrators(errors: list[str]) -> None:
    exec_text = read_text(EXEC_REVIEW_PATH)
    for required_text in [
        "skills/lens-<name>/SKILL.md",
        "Break ties deterministically",
        "Deduplicate conflicts that describe the same underlying disagreement",
        "DECISION SPLIT (AWAITING USER INPUT)",
        "stop after the partial brief and wait for input",
    ]:
        require(
            required_text in exec_text,
            f"{EXEC_REVIEW_PATH.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )

    pre_fight_text = read_text(PRE_FIGHT_PATH)
    for required_text in [
        "skills/lens-<name>/SKILL.md",
        "Select at most 3 disagreements total across the whole review",
        "POSITION CHANGES AFTER CRITIQUE",
        "Critique only the strongest disagreements; do not run all-to-all commentary",
        "Keep the report compact; prioritize signal over completeness",
    ]:
        require(
            required_text in pre_fight_text,
            f"{PRE_FIGHT_PATH.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )


def main() -> int:
    errors: list[str] = []

    for required_path in [
        REGISTRY_PATH,
        OUTPUT_TEMPLATE_PATH,
        COLLISION_PATH,
        SYNTHESIS_PATH,
        EXEC_REVIEW_PATH,
        PRE_FIGHT_PATH,
    ]:
        require(required_path.exists(), f"missing required file: {required_path.relative_to(ROOT)}", errors)

    if errors:
        print("PolyLens markdown contract validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    active_lenses = validate_registry(errors)
    validate_skill_inventory(active_lenses, errors)
    for lens_name in active_lenses:
        validate_lens_skill(lens_name, errors)
    validate_output_template(errors)
    validate_collision(errors)
    validate_synthesis(errors)
    validate_orchestrators(errors)

    if errors:
        print("PolyLens markdown contract validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("PolyLens markdown contract validation passed.")
    print(f"Validated {len(active_lenses)} active lens contracts and shared orchestrator/engine templates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())