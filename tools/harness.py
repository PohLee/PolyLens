#!/usr/bin/env python3
"""PolyLens Harness Engine — Hook registry, orchestration, reasoning control, validation."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HOOKS_DIR = ROOT / "hooks"
HARNESS_DIR = ROOT / "harness"
SHARED_HOOKS_DIR = ROOT / "skills" / "shared" / "hooks"
SHARED_HARNESS_DIR = ROOT / "skills" / "shared" / "harness"


# ─── Frontmatter Parsing ─────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML-like frontmatter from markdown file.

    Returns (metadata_dict, content_body).
    Uses simple key: value parsing — no external YAML dependency.
    """
    match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    metadata = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            metadata[key] = _parse_value(value)

    return metadata, match.group(2).strip()


def _parse_value(value: str) -> Any:
    """Parse a frontmatter value string into appropriate type."""
    if value.startswith("[") and value.endswith("]"):
        items = value[1:-1].split(",")
        return [item.strip() for item in items if item.strip()]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() == "null" or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


# ─── Hook Registry ───────────────────────────────────────────────────

@dataclass
class HookDef:
    """A hook definition loaded from a markdown file."""
    stage: str
    name: str
    order: int
    enabled: bool
    hook_type: str  # "markdown" or "script"
    content: str
    file_path: Path
    script_path: Path | None = None


@dataclass
class HookRegistry:
    """Discovers, loads, and manages hooks."""
    hooks: list[HookDef] = field(default_factory=list)

    @classmethod
    def load(cls, hooks_dir: Path = HOOKS_DIR) -> HookRegistry:
        """Scan hooks directory and load all hook definitions."""
        registry = cls()
        if not hooks_dir.exists():
            return registry

        for stage_dir in sorted(hooks_dir.iterdir()):
            if not stage_dir.is_dir():
                continue
            for hook_file in sorted(stage_dir.glob("*.md")):
                hook = cls._load_hook(hook_file)
                if hook:
                    registry.hooks.append(hook)

        return registry

    @classmethod
    def _load_hook(cls, file_path: Path) -> HookDef | None:
        """Load a single hook from a markdown file."""
        try:
            text = file_path.read_text(encoding="utf-8")
        except Exception:
            return None

        metadata, content = parse_frontmatter(text)

        stage = metadata.get("hook")
        name = metadata.get("name")
        if not stage or not name:
            return None

        hook_type = metadata.get("type", "markdown")
        script_path = None
        if hook_type == "script":
            script_val = metadata.get("script")
            if script_val:
                script_path = Path(script_val)

        return HookDef(
            stage=str(stage),
            name=str(name),
            order=int(metadata.get("order", 99)),
            enabled=bool(metadata.get("enabled", True)),
            hook_type=str(hook_type),
            content=content,
            file_path=file_path,
            script_path=script_path,
        )

    def get_for_stage(self, stage: str) -> list[HookDef]:
        """Get all enabled hooks for a stage, sorted by order."""
        return sorted(
            [h for h in self.hooks if h.stage == stage and h.enabled],
            key=lambda h: h.order,
        )

    def list_all(self) -> list[dict[str, str]]:
        """List all hooks with their status."""
        return [
            {
                "stage": h.stage,
                "name": h.name,
                "order": str(h.order),
                "enabled": str(h.enabled),
                "type": h.hook_type,
                "file": str(h.file_path.relative_to(ROOT)),
            }
            for h in self.hooks
        ]

    def set_enabled(self, stage: str, name: str, enabled: bool) -> bool:
        """Enable or disable a hook by updating its markdown file."""
        for h in self.hooks:
            if h.stage == stage and h.name == name:
                text = h.file_path.read_text(encoding="utf-8")
                old = f"enabled: {str(h.enabled).lower()}"
                new = f"enabled: {str(enabled).lower()}"
                text = text.replace(old, new, 1)
                h.file_path.write_text(text, encoding="utf-8")
                h.enabled = enabled
                return True
        return False


# ─── Harness Config Loading ──────────────────────────────────────────

@dataclass
class ReasoningConfig:
    depth: str = "standard"
    min_lenses: int = 2
    max_lenses: int = 4
    constraints: list[str] = field(default_factory=list)
    output_format: str = "full"
    include_sections: list[str] = field(default_factory=lambda: ["all"])
    custom_template: str | None = None


@dataclass
class ValidationConfig:
    contract: bool = True
    quality_gate: bool = True
    consistency: bool = True
    regression: bool = False
    baseline_file: str | None = None


@dataclass
class InstanceConfig:
    name: str
    lenses: list[str] = field(default_factory=list)
    depends_on: str | None = None
    condition: str | None = None
    reasoning: ReasoningConfig = field(default_factory=ReasoningConfig)
    hooks: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class OrchestrationConfig:
    mode: str = "sequential"
    instances: list[InstanceConfig] = field(default_factory=list)


def load_orchestration_config(path: Path | None = None) -> OrchestrationConfig:
    """Load orchestration config from markdown file."""
    if path is None:
        path = HARNESS_DIR / "orchestration.md"
    if not path.exists():
        return OrchestrationConfig()

    text = path.read_text(encoding="utf-8")
    metadata, _ = parse_frontmatter(text)

    config = OrchestrationConfig(mode=str(metadata.get("mode", "sequential")))

    instances_data = metadata.get("instances", [])
    if isinstance(instances_data, list):
        for inst in instances_data:
            if isinstance(inst, dict):
                reasoning = ReasoningConfig()
                if "reasoning" in inst and isinstance(inst["reasoning"], dict):
                    r = inst["reasoning"]
                    reasoning = ReasoningConfig(
                        depth=str(r.get("depth", "standard")),
                        min_lenses=int(r.get("min_lenses", 2)),
                        max_lenses=int(r.get("max_lenses", 4)),
                        constraints=r.get("constraints", []) or [],
                    )
                config.instances.append(InstanceConfig(
                    name=str(inst.get("name", "unnamed")),
                    lenses=inst.get("lenses", []) or [],
                    depends_on=inst.get("depends_on"),
                    condition=inst.get("condition"),
                    reasoning=reasoning,
                    hooks=inst.get("hooks", {}) or {},
                ))

    return config


def load_reasoning_config(path: Path | None = None) -> ReasoningConfig:
    """Load reasoning config from markdown file."""
    if path is None:
        path = HARNESS_DIR / "reasoning.md"
    if not path.exists():
        return ReasoningConfig()

    text = path.read_text(encoding="utf-8")
    metadata, _ = parse_frontmatter(text)

    reasoning = metadata.get("reasoning", {})
    if not isinstance(reasoning, dict):
        return ReasoningConfig()

    output = reasoning.get("output", {})
    if not isinstance(output, dict):
        output = {}

    return ReasoningConfig(
        depth=str(reasoning.get("depth", "standard")),
        min_lenses=int(reasoning.get("min_lenses", 2)),
        max_lenses=int(reasoning.get("max_lenses", 4)),
        constraints=reasoning.get("constraints", []) or [],
        output_format=str(output.get("format", "full")),
        include_sections=output.get("include_sections", ["all"]) or ["all"],
        custom_template=output.get("custom_template"),
    )


def load_validation_config(path: Path | None = None) -> ValidationConfig:
    """Load validation config from markdown file."""
    if path is None:
        path = HARNESS_DIR / "validation.md"
    if not path.exists():
        return ValidationConfig()

    text = path.read_text(encoding="utf-8")
    metadata, _ = parse_frontmatter(text)

    validation = metadata.get("validation", {})
    if not isinstance(validation, dict):
        return ValidationConfig()

    return ValidationConfig(
        contract=bool(validation.get("contract", True)),
        quality_gate=bool(validation.get("quality_gate", True)),
        consistency=bool(validation.get("consistency", True)),
        regression=bool(validation.get("regression", False)),
        baseline_file=validation.get("baseline_file"),
    )


# ─── CLI Interface ───────────────────────────────────────────────────

def print_usage() -> None:
    """Print CLI usage information."""
    print("""PolyLens Harness Engine

Usage:
  python3 tools/harness.py run "problem" [--orchestration path] [--depth level]
  python3 tools/harness.py validate [brief_path]
  python3 tools/harness.py hooks list
  python3 tools/harness.py hooks enable <stage>/<name>
  python3 tools/harness.py hooks disable <stage>/<name>

Commands:
  run       Run PolyLens analysis with harness (invokes AI agent)
  validate  Validate an existing decision brief
  hooks     Manage hook registry

Options:
  --orchestration   Path to orchestration config
  --depth           Analysis depth: surface, standard, deep
  --help            Show this help message""")


def cmd_hooks(args: list[str]) -> int:
    """Handle hooks subcommand."""
    if not args:
        print_usage()
        return 1

    action = args[0]
    registry = HookRegistry.load()

    if action == "list":
        hooks = registry.list_all()
        if not hooks:
            print("No hooks found.")
            return 0
        print(f"{'Stage':<16} {'Name':<20} {'Order':<6} {'Enabled':<8} {'Type':<10} File")
        print("-" * 90)
        for h in hooks:
            print(f"{h['stage']:<16} {h['name']:<20} {h['order']:<6} {h['enabled']:<8} {h['type']:<10} {h['file']}")
        return 0

    if action in ("enable", "disable"):
        if len(args) < 2:
            print(f"Usage: python3 tools/harness.py hooks {action} <stage>/<name>")
            return 1
        target = args[1]
        if "/" not in target:
            print(f"Error: expected format stage/name, got '{target}'")
            return 1
        stage, name = target.rsplit("/", 1)
        enabled = action == "enable"
        if registry.set_enabled(stage, name, enabled):
            print(f"Hook {stage}/{name} {'enabled' if enabled else 'disabled'}")
        else:
            print(f"Hook {stage}/{name} not found")
            return 1
        return 0

    print(f"Unknown hooks action: {action}")
    return 1


def cmd_validate(args: list[str]) -> int:
    """Handle validate subcommand."""
    brief_path = None
    if args:
        brief_path = Path(args[0])
        if not brief_path.exists():
            print(f"Error: file not found: {brief_path}")
            return 1

    config = load_validation_config()
    results = run_validation(brief_path, config)
    print_validation_report(results)
    return 0


def run_validation(brief_path: Path | None, config: ValidationConfig) -> dict[str, Any]:
    """Run validation checks on a brief file."""
    results: dict[str, Any] = {}

    if config.contract:
        results["contract"] = validate_contract(brief_path)

    if config.quality_gate and brief_path:
        results["quality_gate"] = validate_quality_gate(brief_path)

    if config.consistency and brief_path:
        results["consistency"] = validate_consistency(brief_path)

    if config.regression and config.baseline_file and brief_path:
        results["regression"] = validate_regression(brief_path, Path(config.baseline_file))
    elif config.regression:
        results["regression"] = {"passed": False, "note": "No baseline file configured"}

    return results


def validate_contract(brief_path: Path | None) -> dict[str, Any]:
    """Validate that a brief has all required sections."""
    if brief_path is None:
        return {"passed": False, "note": "No brief file provided"}

    try:
        text = brief_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"passed": False, "note": f"Cannot read file: {e}"}

    required_sections = [
        "VERDICT ALIGNMENT",
        "CONFLICT MAP",
        "FINAL DECISION",
        "FINAL SUMMARY DASHBOARD",
    ]

    missing = [s for s in required_sections if s not in text]
    has_verdicts = any(v in text for v in ["GO", "MODIFY", "BLOCK"])

    return {
        "passed": len(missing) == 0 and has_verdicts,
        "missing_sections": missing,
        "has_verdicts": has_verdicts,
    }


def validate_quality_gate(brief_path: Path) -> dict[str, Any]:
    """Score analysis quality (heuristic)."""
    try:
        text = brief_path.read_text(encoding="utf-8")
    except Exception:
        return {"passed": False, "score": 0, "note": "Cannot read file"}

    score = 0
    max_score = 10

    # Length indicates depth (rough heuristic)
    word_count = len(text.split())
    if word_count > 500:
        score += 2
    elif word_count > 200:
        score += 1

    # Has structured sections
    if "VERDICT ALIGNMENT" in text:
        score += 2
    if "CONFLICT MAP" in text:
        score += 2
    if "FINAL DECISION" in text:
        score += 2

    # Has multiple lens positions
    lens_count = text.count("---BEGIN")
    if lens_count >= 2:
        score += 2
    elif lens_count >= 1:
        score += 1

    # Has risk analysis
    if "Risk:" in text or "risk" in text.lower():
        score += 2

    return {
        "passed": score >= 6,
        "score": min(score, max_score),
        "max_score": max_score,
        "word_count": word_count,
        "lens_count": lens_count,
    }


def validate_consistency(brief_path: Path) -> dict[str, Any]:
    """Check for obvious inconsistencies in the brief."""
    try:
        text = brief_path.read_text(encoding="utf-8")
    except Exception:
        return {"passed": False, "note": "Cannot read file"}

    issues = []

    # Check for contradictory verdict language
    if "GO" in text and "BLOCK" in text:
        if "SPLIT" in text:
            pass  # Expected
        else:
            issues.append("Mixed GO and BLOCK verdicts without SPLIT alignment noted")

    # Check for timeline contradictions (crude check)
    timeline_mentions = re.findall(r"(\d+)[\s-]*(month|week|quarter|year)s?", text, re.IGNORECASE)
    if len(timeline_mentions) > 1:
        unique_timelines = set(timeline_mentions)
        if len(unique_timelines) > 1:
            issues.append(f"Multiple timeline references: {unique_timelines}")

    return {
        "passed": len(issues) == 0,
        "issues": issues,
    }


def validate_regression(brief_path: Path, baseline_path: Path) -> dict[str, Any]:
    """Compare brief against baseline for drift."""
    try:
        text = brief_path.read_text(encoding="utf-8")
        baseline = baseline_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"passed": False, "note": f"Cannot read files: {e}"}

    current_sections = len(re.findall(r"^[A-Z][A-Z ]+$", text, re.MULTILINE))
    baseline_sections = len(re.findall(r"^[A-Z][A-Z ]+$", baseline, re.MULTILINE))

    current_verdicts = len(re.findall(r"(?:GO|MODIFY|BLOCK)", text))
    baseline_verdicts = len(re.findall(r"(?:GO|MODIFY|BLOCK)", baseline))

    return {
        "passed": True,
        "delta": {
            "sections_changed": current_sections != baseline_sections,
            "verdicts_changed": current_verdicts != baseline_verdicts,
        },
    }


def print_validation_report(results: dict[str, Any]) -> None:
    """Print a human-readable validation report."""
    print("\nVALIDATION REPORT")
    print("=" * 40)

    for check, result in results.items():
        if check == "contract":
            status = "PASS" if result.get("passed") else "FAIL"
            print(f"Contract: {status}")
            if result.get("missing_sections"):
                print(f"  Missing sections: {result['missing_sections']}")

        elif check == "quality_gate":
            score = result.get("score", 0)
            max_score = result.get("max_score", 10)
            status = "PASS" if result.get("passed") else "WARN"
            print(f"Quality Gate: {status} ({score}/{max_score})")

        elif check == "consistency":
            status = "PASS" if result.get("passed") else "ISSUES"
            print(f"Consistency: {status}")
            for issue in result.get("issues", []):
                print(f"  - {issue}")

        elif check == "regression":
            if "note" in result:
                print(f"Regression: {result['note']}")
            else:
                delta = result.get("delta", {})
                print(f"Regression: PASS (sections: {'changed' if delta.get('sections_changed') else 'same'}, verdicts: {'changed' if delta.get('verdicts_changed') else 'same'})")

    print()


# ─── Main ────────────────────────────────────────────────────────────

def main() -> int:
    """Main entry point."""
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print_usage()
        return 0

    command = args[0]
    rest = args[1:]

    if command == "hooks":
        return cmd_hooks(rest)
    elif command == "validate":
        return cmd_validate(rest)
    elif command == "run":
        problem = None
        orchestration_path = None
        depth = None

        i = 0
        while i < len(rest):
            if rest[i] == "--orchestration" and i + 1 < len(rest):
                orchestration_path = Path(rest[i + 1])
                i += 2
            elif rest[i] == "--depth" and i + 1 < len(rest):
                depth = rest[i + 1]
                i += 2
            elif rest[i] == "--":
                problem = " ".join(rest[i + 1:])
                break
            else:
                if problem is None:
                    problem = rest[i]
                i += 1

        if not problem:
            print("Error: no problem specified")
            print_usage()
            return 1

        registry = HookRegistry.load()
        orch_config = load_orchestration_config(orchestration_path)
        reasoning_config = load_reasoning_config()
        validation_config = load_validation_config()

        if depth:
            reasoning_config.depth = depth

        print(f"Problem: {problem}")
        print(f"Orchestration: {orch_config.mode}")
        print(f"Reasoning depth: {reasoning_config.depth}")
        print(f"Active hooks: {len([h for h in registry.hooks if h.enabled])}")
        print(f"Validation: contract={validation_config.contract}, quality={validation_config.quality_gate}, consistency={validation_config.consistency}")

        output = {
            "problem": problem,
            "orchestration": {
                "mode": orch_config.mode,
                "instances": [
                    {
                        "name": inst.name,
                        "lenses": inst.lenses,
                        "depends_on": inst.depends_on,
                        "condition": inst.condition,
                        "depth": inst.reasoning.depth,
                    }
                    for inst in orch_config.instances
                ],
            },
            "reasoning": {
                "depth": reasoning_config.depth,
                "min_lenses": reasoning_config.min_lenses,
                "max_lenses": reasoning_config.max_lenses,
                "constraints": reasoning_config.constraints,
                "output_format": reasoning_config.output_format,
            },
            "validation": {
                "contract": validation_config.contract,
                "quality_gate": validation_config.quality_gate,
                "consistency": validation_config.consistency,
                "regression": validation_config.regression,
            },
            "hooks": {
                stage: [h.name for h in registry.get_for_stage(stage)]
                for stage in ["pre-analysis", "lens-select", "review", "collision", "synthesis", "post-analysis"]
            },
        }

        print("\n--- HARNESS CONFIG (JSON) ---")
        print(json.dumps(output, indent=2))
        print("--- END HARNESS CONFIG ---")

        print("\nHarness config ready. AI agent should now execute the analysis.")
        return 0
    else:
        print(f"Unknown command: {command}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
