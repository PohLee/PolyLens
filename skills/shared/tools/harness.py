#!/usr/bin/env python3
"""PolyLens plan generator and format validator; the host agent executes the plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from brief_contract import parse_brief

ROOT = Path(__file__).resolve().parents[1]
HOOKS_DIR = ROOT / "hooks"
HARNESS_DIR = ROOT / "harness"
HOOK_STAGES = ("pre-analysis", "lens-select", "review", "collision", "synthesis", "post-analysis")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


# ─── Frontmatter Parsing ─────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Read JSON frontmatter or legacy flat hook metadata, without a YAML dependency.

    Nested YAML is deliberately rejected: indentation must never be silently lost.
    """
    text = text.replace("\r\n", "\n")
    match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    raw = match.group(1)
    if raw.lstrip().startswith("{"):
        metadata = json.loads(raw, object_pairs_hook=_unique_object)
        if not isinstance(metadata, dict):
            raise ValueError("Frontmatter must be a JSON object")
        return metadata, match.group(2).strip()
    metadata = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace() or ":" not in line or line.startswith("-"):
            raise ValueError("Nested YAML is unsupported; use JSON frontmatter for Harness configuration")
        key, _, value = line.partition(":")
        key = key.strip()
        if not value.strip() or key in metadata:
            raise ValueError("Empty or duplicate metadata key; use JSON frontmatter for nested configuration")
        metadata[key.strip()] = _parse_value(value.strip())

    return metadata, match.group(2).strip()


def _parse_value(value: str) -> Any:
    """Parse a frontmatter value string into appropriate type."""
    if value.startswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
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
                registry.hooks.append(cls.load_file(hook_file))

        return registry

    @classmethod
    def load_file(cls, file_path: Path) -> HookDef:
        """Load a single hook from a markdown file."""
        text = file_path.read_text(encoding="utf-8")

        metadata, content = parse_frontmatter(text)

        stage = metadata.get("hook")
        name = metadata.get("name")
        if not stage or not name:
            raise ValueError(f"{file_path}: hook and name are required")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            raise ValueError(f"{file_path}: invalid hook name")

        hook_type = metadata.get("type", "markdown")
        if stage not in HOOK_STAGES or stage != file_path.parent.name or hook_type not in ("markdown", "script"):
            raise ValueError(f"{file_path}: invalid hook stage or type")
        if type(metadata.get("enabled", False)) is not bool or type(metadata.get("order", 99)) is not int:
            raise ValueError(f"{file_path}: enabled must be boolean and order must be integer")
        script_path = None
        if hook_type == "script":
            script_val = metadata.get("script")
            if script_val:
                script_path = Path(script_val)

        return HookDef(
            stage=str(stage),
            name=str(name),
            order=int(metadata.get("order", 99)),
            enabled=metadata.get("enabled", False),
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
                new = f"enabled: {str(enabled).lower()}"
                match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
                if not match:
                    raise ValueError("Hook must contain frontmatter")
                raw, content = match.groups()
                if raw.lstrip().startswith("{"):
                    metadata, _ = parse_frontmatter(text)
                    metadata["enabled"] = enabled
                    raw = json.dumps(metadata, indent=2)
                else:
                    raw, count = re.subn(r"^enabled[ \t]*:[^\n]*$", new, raw, count=1, flags=re.MULTILINE)
                    if not count:
                        raw += "\n" + new
                text = "---\n" + raw + "\n---\n" + content
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
    contract: bool = False
    quality_gate: bool = False
    consistency: bool = False
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


def _object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    unknown = set(value) - keys
    if unknown:
        raise ValueError(f"Unknown {label} fields: {sorted(unknown)}")
    return value


def _strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        raise ValueError(f"{label} must be a list of nonempty strings")
    return value


def _config(path: Path | None, filename: str) -> dict[str, Any]:
    if path is None:
        path = HARNESS_DIR / filename
        if not path.exists():
            return {}
    metadata, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
    if not metadata:
        raise ValueError(f"{path}: missing configuration frontmatter")
    return metadata


def _reasoning(value: Any) -> ReasoningConfig:
    r = _object(value, {"depth", "min_lenses", "max_lenses", "constraints", "output"}, "reasoning")
    output = _object(r.get("output", {}), {"format", "include_sections", "custom_template"}, "output")
    config = ReasoningConfig(
        depth=r.get("depth", "standard"), min_lenses=r.get("min_lenses", 2), max_lenses=r.get("max_lenses", 4),
        constraints=_strings(r.get("constraints", []), "constraints"), output_format=output.get("format", "full"),
        include_sections=_strings(output.get("include_sections", ["all"]), "include_sections"),
        custom_template=output.get("custom_template"),
    )
    if config.depth not in ("surface", "standard", "deep"):
        raise ValueError("Invalid reasoning depth")
    if type(config.min_lenses) is not int or type(config.max_lenses) is not int or not 2 <= config.min_lenses <= config.max_lenses <= 4:
        raise ValueError("Require 2 <= min_lenses <= max_lenses <= 4")
    if config.output_format not in ("full", "concise", "dashboard-only"):
        raise ValueError("Invalid output format")
    if config.custom_template is not None and not isinstance(config.custom_template, str):
        raise ValueError("custom_template must be a path string or null")
    return config


def load_orchestration_config(path: Path | None = None) -> OrchestrationConfig:
    data = _object(_config(path, "orchestration.md"), {"mode", "instances"}, "orchestration")
    config = OrchestrationConfig(mode=data.get("mode", "sequential"))
    if config.mode not in ("sequential", "parallel", "conditional"):
        raise ValueError("Invalid orchestration mode")
    instances = data.get("instances", [])
    if not isinstance(instances, list):
        raise ValueError("instances must be a list")
    for value in instances:
        inst = _object(value, {"name", "lenses", "depends_on", "condition", "reasoning", "hooks"}, "instance")
        name = inst.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Each instance requires a nonempty name")
        for key in ("depends_on", "condition"):
            if inst.get(key) is not None and (not isinstance(inst[key], str) or not inst[key].strip()):
                raise ValueError(f"{key} must be a nonempty string or null")
        hooks = _object(inst.get("hooks", {}), set(HOOK_STAGES), "hooks")
        for stage, names in hooks.items():
            _strings(names, f"hooks.{stage}")
        config.instances.append(InstanceConfig(name=name, lenses=_strings(inst.get("lenses", []), "lenses"),
            depends_on=inst.get("depends_on"), condition=inst.get("condition"), reasoning=_reasoning(inst.get("reasoning", {})), hooks=hooks))
    names = [i.name for i in config.instances]
    if len(set(names)) != len(names):
        raise ValueError("Instance names must be unique")
    dependencies = {i.name: i.depends_on for i in config.instances}
    for instance in config.instances:
        seen = {instance.name}
        dependency = instance.depends_on
        while dependency is not None:
            if dependency not in dependencies or dependency in seen:
                raise ValueError("Unknown or cyclic instance dependency")
            seen.add(dependency)
            dependency = dependencies[dependency]
        if config.mode == "sequential" and instance.depends_on and names.index(instance.depends_on) >= names.index(instance.name):
            raise ValueError("Sequential dependencies must appear before their dependents")
    return config


def load_reasoning_config(path: Path | None = None) -> ReasoningConfig:
    data = _object(_config(path, "reasoning.md"), {"reasoning"}, "configuration")
    return _reasoning(data.get("reasoning", {}))


def load_validation_config(path: Path | None = None) -> ValidationConfig:
    data = _object(_config(path, "validation.md"), {"validation"}, "configuration")
    values = _object(data.get("validation", {}), {"contract", "quality_gate", "consistency", "regression", "baseline_file"}, "validation")
    for key in ("contract", "quality_gate", "consistency", "regression"):
        if key in values and type(values[key]) is not bool:
            raise ValueError(f"validation.{key} must be a boolean")
    baseline = values.get("baseline_file")
    if baseline is not None and (not isinstance(baseline, str) or not baseline.strip()):
        raise ValueError("baseline_file must be a nonempty path string or null")
    if baseline:
        base = path.parent if path else HARNESS_DIR
        values["baseline_file"] = str((base / baseline).resolve())
    return ValidationConfig(**values)


def load_project_context(project_root: Path) -> dict[str, Any]:
    """Read only explicitly indexed project memory; never guess the newest revision."""
    root = project_root.resolve(strict=True)
    memory = root / "docs/polylens/memory"
    index = memory / "index.json"
    classes = {"project-context", "project-preferences", "decision-history"}
    sources = {}
    if index.exists():
        if not index.resolve().is_relative_to(root):
            raise ValueError("Memory index must stay inside the target project")
        data = _object(json.loads(index.read_text(encoding="utf-8"), object_pairs_hook=_unique_object), classes, "memory index")
        for name, value in data.items():
            if not isinstance(value, str) or not value.strip() or Path(value).is_absolute():
                raise ValueError("Memory references must be relative Markdown paths")
            path = (memory / value).resolve(strict=True)
            if not path.is_relative_to(memory.resolve()) or not path.is_relative_to(root) or path.suffix.lower() != ".md":
                raise ValueError("Memory reference must stay inside the project's memory directory")
            sources[name] = {"path": path.relative_to(root).as_posix(), "content": path.read_text(encoding="utf-8")}
    return {"project_root": str(root), "status": "loaded" if index.exists() else "absent", "sources": sources, "missing_classes": sorted(classes - sources.keys())}


# ─── CLI Interface ───────────────────────────────────────────────────

def cmd_hooks(args: list[str]) -> int:
    """Handle hooks subcommand."""
    if not args:
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
    """Validate structure only; never claim that a well-formed recommendation is correct."""
    if brief_path is None:
        return {"passed": False, "note": "No brief file provided"}

    try:
        text = brief_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"passed": False, "note": f"Cannot read file: {e}"}

    return parse_brief(text).contract()


def validate_quality_gate(brief_path: Path) -> dict[str, Any]:
    """Legacy configuration key: advisory format hints, never a quality score."""
    try:
        text = brief_path.read_text(encoding="utf-8")
    except Exception:
        return {"passed": False, "note": "Cannot read file"}
    return {"advisory": True, "note": "Format hints only; reasoning quality is not measured", "word_count": len(text.split()), "lens_count": len(parse_brief(text).positions)}


def validate_consistency(brief_path: Path) -> dict[str, Any]:
    """Check for obvious inconsistencies in the brief."""
    try:
        text = brief_path.read_text(encoding="utf-8")
    except Exception:
        return {"passed": False, "note": "Cannot read file"}

    return parse_brief(text).consistency()


def validate_regression(brief_path: Path, baseline_path: Path) -> dict[str, Any]:
    """Compare brief against baseline for drift."""
    try:
        text = brief_path.read_text(encoding="utf-8")
        baseline = baseline_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"passed": False, "note": f"Cannot read files: {e}"}

    return parse_brief(text).regression(parse_brief(baseline))


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
            for issue in result.get("issues", []):
                print(f"  - {issue}")

        elif check == "quality_gate":
            print(f"Format hints (not a quality score): {result.get('note')}")

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
                status = "PASS" if result.get("passed") else "FAIL"
                print(f"Regression: {status} (sections: {'changed' if delta.get('sections_changed') else 'same'}, verdicts: {'changed' if delta.get('verdicts_changed') else 'same'}, content: {'changed' if delta.get('content_changed') else 'same'})")

    print()


# ─── Main ────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Generate a plan for the host agent; does not invoke models or scripts")
    run.add_argument("problem")
    for option in ("orchestration", "reasoning", "validation"):
        run.add_argument(f"--{option}", type=Path)
    run.add_argument("--depth", choices=("surface", "standard", "deep"))
    run.add_argument("--json", action="store_true")
    validate = commands.add_parser("validate", help="Check a standard multi-lens brief (not model quality)")
    validate.add_argument("brief", type=Path)
    validate.add_argument("--config", type=Path)
    validate.add_argument("--json", action="store_true")
    hooks = commands.add_parser("hooks")
    hooks.add_argument("action", choices=("list", "enable", "disable"))
    hooks.add_argument("target", nargs="?")
    context = commands.add_parser("context", help="Read a target project's indexed memory as an attributed snapshot")
    context.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "context":
            print(json.dumps(load_project_context(args.project_root), indent=2, ensure_ascii=False))
            return 0
        if args.command == "hooks":
            return cmd_hooks([args.action] + ([args.target] if args.target else []))
        if args.command == "validate":
            config = load_validation_config(args.config) if args.config else ValidationConfig(contract=True)
            results = run_validation(args.brief, config)
            if args.json:
                print(json.dumps(results, indent=2))
            else:
                print_validation_report(results)
            return 0 if all(r.get("passed", True) for r in results.values()) else 1
        registry = HookRegistry.load()
        orchestration = load_orchestration_config(args.orchestration)
        reasoning = load_reasoning_config(args.reasoning)
        validation = load_validation_config(args.validation)
        if args.depth:
            reasoning.depth = args.depth
        output = {
            "problem": args.problem, "execution": "host-agent",
            "orchestration": asdict(orchestration), "reasoning": asdict(reasoning), "validation": asdict(validation),
            "hooks": {stage: [h.name for h in registry.get_for_stage(stage)] for stage in HOOK_STAGES},
        }
        if not args.json:
            print("Plan only: the host agent executes reviews and hooks with user-authorized tools.\n--- HARNESS CONFIG (JSON) ---")
        print(json.dumps(output, indent=2))
        if not args.json:
            print("--- END HARNESS CONFIG ---")
        return 0
    except (OSError, ValueError, TypeError) as error:
        print(f"Harness error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
