#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path
from lens_contract import parse_registry, projection_errors
from runtime_bundle import check_runtime
from harness import HookRegistry, load_orchestration_config, load_reasoning_config, load_validation_config


ROOT = Path(__file__).resolve().parents[1]

REGISTRY_PATH = ROOT / "prompts" / "lens-registry.md"
OUTPUT_TEMPLATE_PATH = ROOT / "prompts" / "output-template.md"
COLLISION_PATH = ROOT / "engines" / "collision.md"
SYNTHESIS_PATH = ROOT / "engines" / "synthesis.md"
ROUTER_PATH = ROOT / "skills" / "polylens" / "SKILL.md"
LENS_REVIEW_PATH = ROOT / "skills" / "polylens-lens-review" / "SKILL.md"
ORCHESTRATORS_DIR = ROOT / "orchestrators"
EXEC_REVIEW_PATH = ORCHESTRATORS_DIR / "polylens-executive-review.md"
PRE_FIGHT_PATH = ORCHESTRATORS_DIR / "polylens-pre-fight.md"
SKILLS_DIR = ROOT / "skills"
SHARED_DIR = SKILLS_DIR / "shared"
LENSES_DIR = ROOT / "lenses"
BUNDLED_PROMPTS_DIR = SHARED_DIR / "prompts"
BUNDLED_ENGINES_DIR = SHARED_DIR / "engines"
BUNDLED_LENSES_DIR = SHARED_DIR / "lenses"
BUNDLED_ORCHESTRATORS_DIR = SHARED_DIR / "orchestrators"
HOOKS_DIR = ROOT / "hooks"
HARNESS_DIR = ROOT / "harness"
BUNDLED_HOOKS_DIR = SHARED_DIR / "hooks"
BUNDLED_HARNESS_DIR = SHARED_DIR / "harness"

HOOK_STAGES = ["pre-analysis", "lens-select", "review", "collision", "synthesis", "post-analysis"]


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


def normalize_bundled_shared_refs(text: str) -> str:
    return (
        text.replace("../prompts/", "prompts/")
        .replace("../shared/prompts/", "prompts/")
        .replace("../shared/engines/", "engines/")
    )


def normalize_bundled_prompt_refs(text: str) -> str:
    return (
        text.replace("../playbooks/", "prompts/playbooks/")
        .replace("../prompts/", "prompts/")
        .replace("../shared/prompts/", "prompts/")
    )


def validate_lens_projections(errors: list[str]) -> None:
    try:
        errors.extend(projection_errors(ROOT))
    except (ValueError, KeyError, IndexError) as error:
        errors.append(f"Cannot generate lens projections: {error}")


def validate_registry(errors: list[str]) -> list[str]:
    text = read_text(REGISTRY_PATH)
    order, entries = parse_registry(text)

    require(bool(order), f"{REGISTRY_PATH.relative_to(ROOT)}: no lens entries found", errors)
    require(len(order) == len(set(order)), "duplicate lens IDs in registry", errors)
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
        for boolean in ("active", "default"):
            require(fields.get(boolean) in ("true", "false"), f"{lens_name}: {boolean} must be true or false", errors)
        for required_field in [
            "focus",
            "domains",
            "triggers",
            "owns_decisions",
            "veto_on",
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


def validate_lens_brief(lens_name: str, errors: list[str]) -> None:
    lens_path = LENSES_DIR / f"lens-{lens_name.lower()}.md"
    require(lens_path.exists(), f"missing lens brief: {lens_path.relative_to(ROOT)}", errors)
    if not lens_path.exists():
        return

    text = read_text(lens_path)
    require(
        f"---BEGIN {lens_name} POSITION---" in text,
        f"{lens_path.relative_to(ROOT)}: missing BEGIN position marker for {lens_name}",
        errors,
    )
    require(
        f"---END {lens_name} POSITION---" in text,
        f"{lens_path.relative_to(ROOT)}: missing END position marker for {lens_name}",
        errors,
    )

    position = re.search(rf"---BEGIN {re.escape(lens_name)} POSITION---(.*?)---END {re.escape(lens_name)} POSITION---", text, re.DOTALL)
    for required_field in LENS_REQUIRED_FIELDS:
        require(
            position is not None and required_field in position.group(1),
            f"{lens_path.relative_to(ROOT)}: missing '{required_field}' in lens output contract",
            errors,
        )

    for required_text in [
        "Available tools when they materially improve judgment:",
    ]:
        require(
            required_text in text,
            f"{lens_path.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )


def validate_bundled_shared_docs(errors: list[str]) -> None:
    bundled_paths = [
        BUNDLED_PROMPTS_DIR / "lens-registry.md",
        BUNDLED_PROMPTS_DIR / "lens-capabilities.md",
        BUNDLED_PROMPTS_DIR / "shared-playbooks.md",
        BUNDLED_PROMPTS_DIR / "conflict-types.md",
        BUNDLED_PROMPTS_DIR / "output-template.md",
        BUNDLED_ENGINES_DIR / "collision.md",
        BUNDLED_ENGINES_DIR / "synthesis.md",
        BUNDLED_ORCHESTRATORS_DIR / "polylens-executive-review.md",
        BUNDLED_ORCHESTRATORS_DIR / "polylens-pre-fight.md",
    ]

    for bundled_path in bundled_paths:
        require(bundled_path.exists(), f"missing bundled shared file: {bundled_path.relative_to(ROOT)}", errors)

    prompt_pairs = [
        (REGISTRY_PATH, BUNDLED_PROMPTS_DIR / "lens-registry.md"),
        (ROOT / "prompts" / "lens-capabilities.md", BUNDLED_PROMPTS_DIR / "lens-capabilities.md"),
        (ROOT / "prompts" / "shared-playbooks.md", BUNDLED_PROMPTS_DIR / "shared-playbooks.md"),
        (ROOT / "prompts" / "conflict-types.md", BUNDLED_PROMPTS_DIR / "conflict-types.md"),
        (OUTPUT_TEMPLATE_PATH, BUNDLED_PROMPTS_DIR / "output-template.md"),
    ]
    for source_path, bundled_path in prompt_pairs:
        if source_path.exists() and bundled_path.exists():
            require(
                read_text(source_path) == normalize_bundled_prompt_refs(read_text(bundled_path)),
                (
                    f"bundled prompt mismatch: {bundled_path.relative_to(ROOT)} must match "
                    f"{source_path.relative_to(ROOT)}. Run `python3 tools/sync_playbooks.py` when the "
                    "playbook bundle drifts."
                ),
                errors,
            )

    for playbook_path in sorted((ROOT / "prompts" / "playbooks").glob("*.md")):
        bundled_path = SHARED_DIR / "playbooks" / playbook_path.name
        require(
            bundled_path.exists(),
            f"missing bundled playbook: {bundled_path.relative_to(ROOT)}",
            errors,
        )
        if bundled_path.exists():
            require(
                read_text(playbook_path) == read_text(bundled_path),
                (
                    f"bundled playbook mismatch: {bundled_path.relative_to(ROOT)} must match "
                    f"{playbook_path.relative_to(ROOT)}. Run `python3 tools/sync_playbooks.py` to resync."
                ),
                errors,
            )

    engine_pairs = [
        (COLLISION_PATH, BUNDLED_ENGINES_DIR / "collision.md"),
        (SYNTHESIS_PATH, BUNDLED_ENGINES_DIR / "synthesis.md"),
    ]
    for source_path, bundled_path in engine_pairs:
        if source_path.exists() and bundled_path.exists():
            require(
                read_text(source_path) == normalize_bundled_shared_refs(read_text(bundled_path)),
                (
                    f"bundled engine mismatch: {bundled_path.relative_to(ROOT)} must stay in sync with "
                    f"{source_path.relative_to(ROOT)} aside from shared/ path prefixes"
                ),
                errors,
            )

    orchestrator_pairs = [
        (EXEC_REVIEW_PATH, BUNDLED_ORCHESTRATORS_DIR / "polylens-executive-review.md"),
        (PRE_FIGHT_PATH, BUNDLED_ORCHESTRATORS_DIR / "polylens-pre-fight.md"),
    ]
    for source_path, bundled_path in orchestrator_pairs:
        if source_path.exists() and bundled_path.exists():
            require(
                read_text(source_path) == read_text(bundled_path),
                (
                    f"bundled orchestrator mismatch: {bundled_path.relative_to(ROOT)} must match "
                    f"{source_path.relative_to(ROOT)}"
                ),
                errors,
            )

    for lens_path in sorted(LENSES_DIR.glob("lens-*.md")):
        bundled_path = BUNDLED_LENSES_DIR / lens_path.name
        require(
            bundled_path.exists(),
            f"missing bundled lens brief: {bundled_path.relative_to(ROOT)}",
            errors,
        )
        if bundled_path.exists():
            require(
                read_text(lens_path) == read_text(bundled_path),
                (
                    f"bundled lens mismatch: {bundled_path.relative_to(ROOT)} must match "
                    f"{lens_path.relative_to(ROOT)}"
                ),
                errors,
            )


def validate_skill_inventory(active_lenses: list[str], errors: list[str]) -> None:
    public_skill_dirs = sorted(
        path.name
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name != "shared"
    )
    expected_dirs = sorted([
        "polylens",
        "polylens-lens-review",
    ])
    require(
        public_skill_dirs == expected_dirs,
        (
            f"skills inventory mismatch: expected public skills {expected_dirs}, found {public_skill_dirs}. "
            "Keep only the public router/orchestrator skills at the top level and move lens briefs into shared docs."
        ),
        errors,
    )

    expected_lens_briefs = sorted(f"lens-{name.lower()}.md" for name in active_lenses)
    actual_lens_briefs = sorted(path.name for path in LENSES_DIR.glob("lens-*.md"))
    require(
        actual_lens_briefs == expected_lens_briefs,
        (
            f"lens brief inventory mismatch: expected {expected_lens_briefs}, found {actual_lens_briefs}. "
            "Update prompts/lens-registry.md or lenses/lens-*.md to restore parity."
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
        "Prefer the stacked layout below over wide markdown tables.",
        "Use short labeled lines and bullets; do not use ASCII box borders.",
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
    router_text = read_text(ROUTER_PATH)
    for required_text in [
        "Standard review mode",
        "Pre-fight mode",
        "../shared/orchestrators/polylens-executive-review.md",
        "../shared/orchestrators/polylens-pre-fight.md",
        "Default to **standard review mode**",
    ]:
        require(
            required_text in router_text,
            f"{ROUTER_PATH.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )

    exec_text = read_text(EXEC_REVIEW_PATH)
    for required_text in [
        "../shared/prompts/lens-registry.md",
        "../shared/lenses/lens-<name>.md",
        "../shared/engines/collision.md",
        "../shared/engines/synthesis.md",
        "../shared/prompts/output-template.md",
        "docs/polylens/reviews/",
        "YYMMDD_slug_rN.md",
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

    lens_review_text = read_text(LENS_REVIEW_PATH)
    for required_text in [
        "../shared/prompts/lens-registry.md",
        "../shared/lenses/lens-<name>.md",
        "../shared/prompts/lens-capabilities.md",
        "../shared/prompts/shared-playbooks.md",
        "Select exactly one lens",
        "Do not run collision or synthesis for a single-lens review",
    ]:
        require(
            required_text in lens_review_text,
            f"{LENS_REVIEW_PATH.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )

    pre_fight_text = read_text(PRE_FIGHT_PATH)
    for required_text in [
        "Use the embedded lens registry in this skill.",
        "use the embedded lens brief in this skill",
        "Embedded Lens Registry And Briefs",
        "docs/polylens/pre-fight/",
        "YYMMDD_slug_rN.md",
        "Select at most 3 disagreements total across the whole review",
        "Default to `interactive` mode",
        "AUTOMATIC ARBITRATION",
        "Mode: [INTERACTIVE / AUTOMATIC]",
        "POSITION CHANGES AFTER CRITIQUE",
        "Critique only the strongest disagreements; do not run all-to-all commentary",
        "Keep the report compact; prioritize signal over completeness",
    ]:
        require(
            required_text in pre_fight_text,
            f"{PRE_FIGHT_PATH.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )

    for required_path in [
        ROOT / "docs" / "polylens" / "README.md",
    ]:
        require(
            required_path.exists(),
            f"missing docs artifact path: {required_path.relative_to(ROOT)}",
            errors,
        )


def validate_pr_crisis_recovery(errors: list[str]) -> None:
    """Check PR instructions and coverage, not the quality of generated advice."""
    playbook_path = ROOT / "prompts" / "playbooks" / "pr-crisis-recovery.md"
    fixtures_path = ROOT / "tests" / "fixtures" / "pr-crisis-recovery.md"
    for path in [playbook_path, fixtures_path]:
        require(path.exists(), f"missing PR contract file: {path.relative_to(ROOT)}", errors)
    if not playbook_path.exists() or not fixtures_path.exists():
        return

    text = read_text(playbook_path)
    for required_text in [
        "### 1. Evidence Ledger",
        "SUPPORTED FACT",
        "USER-REPORTED",
        "INFERENCE / FORECAST",
        "UNKNOWN / DISPUTED",
        "### 2. Decision and Accountability Gate",
        "### 3. Coupled-Signal and Stakeholder Test",
        "Admission signal",
        "Historical-neglect signal",
        "Displacement signal",
        "Amplification and sequence",
        "### 4. Compare Options and Select Posture",
        "### 5. Build and Check the Message",
        "### 6. Monitor Outcomes and Update Without Taking Sides",
        "When web research is prohibited",
        "A user's disagreement alone is not new factual evidence",
        "UPDATE BASIS",
    ]:
        require(
            required_text in text,
            f"{playbook_path.relative_to(ROOT)}: missing '{required_text}'",
            errors,
        )

    for path in [EXEC_REVIEW_PATH, PRE_FIGHT_PATH, LENS_REVIEW_PATH]:
        text = read_text(path)
        pointer = "../shared/playbooks/pr-crisis-recovery.md"
        pointer_offset = text.find(pointer)
        selection_offset = text.find("### Step 1:")
        require(
            0 <= pointer_offset < selection_offset
            and "Its gates are mandatory even when research is disabled." in text,
            f"{path.relative_to(ROOT)}: PR playbook must be mandatory before lens selection",
            errors,
        )

    fixtures = read_text(fixtures_path)
    for number in range(1, 11):
        require(
            f"## PR-{number:02d} —" in fixtures,
            f"{fixtures_path.relative_to(ROOT)}: missing regression PR-{number:02d}",
            errors,
        )


def validate_decision_protocol(errors: list[str]) -> None:
    """Guard protocol invariants; actual model behavior is evaluated separately."""
    rules = {
        COLLISION_PATH: ["UNANIMOUS describes verdict alignment only", "Always compare decision framing and non-negotiables"],
        SYNTHESIS_PATH: ["canonical conflict count is zero", "Retain compatible required modifications", "A unanimous BLOCK still blocks execution", "gap > 2x → escalate to user", "no execution blocker or user decision is pending"],
        OUTPUT_TEMPLATE_PATH: ["UNANIMOUS describes verdict alignment only", "including Type 4 resource escalation or Type 5"],
        PRE_FIGHT_PATH: ["Resource evidence gate:", "Interactive mode escalates", "HOLD an irreversible commitment", "This gate takes precedence"],
    }
    for path, required in rules.items():
        text = read_text(path)
        for rule in required:
            require(rule in text, f"{path.relative_to(ROOT)}: missing decision invariant '{rule}'", errors)
    text = read_text(SYNTHESIS_PATH)
    require("split the difference with milestones" not in text, "synthesis contradicts Type 4 escalation threshold", errors)
    require("Set Confidence Level: High" not in text, "synthesis must not assign High solely from consensus", errors)


def validate_hook_frontmatter(hook_path: Path, errors: list[str]) -> None:
    """Validate that a hook file has correct frontmatter."""
    try:
        text = hook_path.read_text(encoding="utf-8")
    except Exception:
        errors.append(f"Cannot read hook file: {hook_path.relative_to(ROOT)}")
        return

    if not text.startswith("---"):
        errors.append(f"{hook_path.relative_to(ROOT)}: missing frontmatter")
        return

    required_fields = ["hook:", "name:", "order:", "enabled:", "type:"]
    for field_name in required_fields:
        if field_name not in text:
            errors.append(f"{hook_path.relative_to(ROOT)}: missing field '{field_name.rstrip(':')}'")

    # Validate hook stage matches directory
    match = re.search(r"hook:\s*(\S+)", text)
    if match:
        stage = match.group(1)
        parent_dir = hook_path.parent.name
        if stage != parent_dir:
            errors.append(f"{hook_path.relative_to(ROOT)}: hook stage '{stage}' doesn't match directory '{parent_dir}'")

    # Validate type is markdown or script
    match = re.search(r"type:\s*(\S+)", text)
    if match:
        hook_type = match.group(1)
        if hook_type not in ("markdown", "script"):
            errors.append(f"{hook_path.relative_to(ROOT)}: invalid type '{hook_type}', must be 'markdown' or 'script'")


def validate_harness_config(config_path: Path, errors: list[str]) -> None:
    """Validate that a harness config file has correct frontmatter."""
    try:
        text = config_path.read_text(encoding="utf-8")
    except Exception:
        errors.append(f"Cannot read harness config: {config_path.relative_to(ROOT)}")
        return

    if not text.startswith("---"):
        errors.append(f"{config_path.relative_to(ROOT)}: missing frontmatter")
        return
    loaders = {"orchestration.md": load_orchestration_config, "reasoning.md": load_reasoning_config, "validation.md": load_validation_config}
    try:
        loaders[config_path.name](config_path)
    except (KeyError, ValueError, TypeError, OSError) as error:
        errors.append(f"{config_path.relative_to(ROOT)}: {error}")


def validate_hooks(errors: list[str]) -> None:
    """Validate all hook files."""
    if not HOOKS_DIR.exists():
        return
    try:
        HookRegistry.load(HOOKS_DIR)
    except (ValueError, TypeError, OSError) as error:
        errors.append(f"Invalid hook registry: {error}")

    for stage in HOOK_STAGES:
        stage_dir = HOOKS_DIR / stage
        if not stage_dir.exists():
            continue
        for hook_file in sorted(stage_dir.glob("*.md")):
            validate_hook_frontmatter(hook_file, errors)

    # Check bundled hooks match source hooks
    if BUNDLED_HOOKS_DIR.exists():
        for stage in HOOK_STAGES:
            source_stage = HOOKS_DIR / stage
            bundled_stage = BUNDLED_HOOKS_DIR / stage
            if source_stage.exists() and bundled_stage.exists():
                for source_file in sorted(source_stage.glob("*.md")):
                    bundled_file = bundled_stage / source_file.name
                    if not bundled_file.exists():
                        errors.append(f"missing bundled hook: {bundled_file.relative_to(ROOT)}")
                    elif read_text(source_file) != read_text(bundled_file):
                        errors.append(f"bundled hook mismatch: {bundled_file.relative_to(ROOT)} must match {source_file.relative_to(ROOT)}")


def validate_harness(errors: list[str]) -> None:
    """Validate harness config files."""
    if not HARNESS_DIR.exists():
        return

    for config_file in sorted(HARNESS_DIR.glob("*.md")):
        validate_harness_config(config_file, errors)

    # Check bundled harness configs match source
    if BUNDLED_HARNESS_DIR.exists():
        for source_file in sorted(HARNESS_DIR.glob("*.md")):
            bundled_file = BUNDLED_HARNESS_DIR / source_file.name
            if not bundled_file.exists():
                errors.append(f"missing bundled harness config: {bundled_file.relative_to(ROOT)}")
            elif read_text(source_file) != read_text(bundled_file):
                errors.append(f"bundled harness mismatch: {bundled_file.relative_to(ROOT)} must match {source_file.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []

    for required_path in [
        REGISTRY_PATH,
        OUTPUT_TEMPLATE_PATH,
        COLLISION_PATH,
        SYNTHESIS_PATH,
        ROUTER_PATH,
        ORCHESTRATORS_DIR,
        EXEC_REVIEW_PATH,
        LENS_REVIEW_PATH,
        PRE_FIGHT_PATH,
        LENSES_DIR,
    ]:
        require(required_path.exists(), f"missing required file: {required_path.relative_to(ROOT)}", errors)

    if errors:
        print("PolyLens markdown contract validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    active_lenses = validate_registry(errors)
    validate_lens_projections(errors)
    all_lenses, _ = parse_registry(read_text(REGISTRY_PATH))
    validate_skill_inventory(all_lenses, errors)
    for lens_name in all_lenses:
        validate_lens_brief(lens_name, errors)
    validate_output_template(errors)
    validate_bundled_shared_docs(errors)
    validate_collision(errors)
    validate_synthesis(errors)
    validate_decision_protocol(errors)
    validate_orchestrators(errors)
    validate_pr_crisis_recovery(errors)
    validate_hooks(errors)
    validate_harness(errors)
    errors.extend(check_runtime(SHARED_DIR, ROOT))
    scenarios_path = ROOT / "tests/fixtures/decision-behavior.md"
    if scenarios_path.is_file():
        scenarios = read_text(scenarios_path)
        for number in range(1, 11):
            require(f"## DB-{number:02d} —" in scenarios, f"missing behavior scenario DB-{number:02d}", errors)
    else:
        errors.append("missing decision behavior scenarios (these are not model execution results)")

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
