"""Harness behavior through its CLI, not through private parser helpers."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "tools/harness.py"
sys.path.insert(0, str(ROOT / "tools"))
from runtime_bundle import build_bundle


class HarnessCLITests(unittest.TestCase):
    def test_position_cannot_supply_completion_sections(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        text = text.replace("## CONFIDENCE LEVEL\nHigh", "").replace(
            "---END CTO POSITION---", "## CONFIDENCE LEVEL\nHigh\n---END CTO POSITION---", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            path.write_text(text, encoding="utf-8")
            result = self.run_cli("validate", path, "--json")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CONFIDENCE LEVEL", json.loads(result.stdout)["contract"]["missing_sections"])

    def test_duplicate_position_fields_are_ambiguous(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            path.write_text(text.replace("- Scope: HOLD", "- Scope: EXPAND\n- Scope: HOLD", 1), encoding="utf-8")
            result = self.run_cli("validate", path, "--json")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate position field", result.stdout)

    def test_alignment_is_read_only_from_the_alignment_section(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        text = text.replace("Key concerns:", "Alignment: SPLIT\nKey concerns:", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            path.write_text(text, encoding="utf-8")
            config = self.config(directory, "validation.md", {"validation": {"consistency": True}})
            result = self.run_cli("validate", path, "--config", config, "--json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            path.write_text(text.replace("Alignment: UNANIMOUS", "Alignment: UNANIMOUS\nAlignment: SPLIT"), encoding="utf-8")
            result = self.run_cli("validate", path, "--config", config, "--json")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(json.loads(result.stdout)["consistency"]["passed"])

    def test_duplicate_and_misowned_sections_are_rejected(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        variants = [text + "\n## CONFIDENCE LEVEL\nLow\n", text.replace(
            "## CONFIDENCE LEVEL\nHigh", "").replace("## ALIGNED PLAN", "## CONFIDENCE LEVEL\nHigh\n## ALIGNED PLAN"),
            text.replace("## CONFIDENCE LEVEL", "## APPENDIX\n## CONFIDENCE LEVEL")]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            for variant in variants:
                path.write_text(variant, encoding="utf-8")
                result = self.run_cli("validate", path, "--json")
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_pending_option_cannot_borrow_fields_from_the_split_footer(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        partial = text.split("## ALIGNED PLAN")[0] + """## DECISION SPLIT (AWAITING USER INPUT)
Decision needed: Choose a scope
Why escalation happened: Irreconcilable scope requirements
## OPTION A
Supported by: CTO
What changes: Online only
Upside: Simpler
Downside: No offline access
## OPTION B
Supported by: CEO
What changes: Offline support
Upside: More access
What the user should answer: Choose a scope
What remains blocked until then: Launch
Downside: More work
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            path.write_text(partial, encoding="utf-8")
            result = self.run_cli("validate", path, "--json")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("OPTION B requires", result.stdout)

    def test_hook_toggle_only_updates_metadata_for_json_and_flat_frontmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bundle"
            build_bundle(output, False)
            harness = output / "shared/tools/harness.py"
            hook = output / "shared/hooks/pre-analysis/toggle.md"
            cases = [
                '---\n\n{"hook":"pre-analysis","name":"toggle","enabled":false,"type":"markdown","order":3}\n---\nBody example:\nenabled: false\n',
                '---\nhook: pre-analysis\nname: toggle\ntype: markdown\norder: 3\n---\nBody example:\nenabled: false\n',
            ]
            cases += [cases[1].replace("order: 3\n", "order: 3\nenabled: False\n"), cases[1].replace("order: 3\n", "order: 3\nenabled : false\n")]
            for content in cases:
                hook.write_text(content, encoding="utf-8")
                result = subprocess.run([sys.executable, "-B", str(harness), "hooks", "enable", "pre-analysis/toggle"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Body example:\nenabled: false\n", hook.read_text(encoding="utf-8"))
                result = subprocess.run([sys.executable, "-B", str(harness), "run", "Hook check", "--json"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("toggle", json.loads(result.stdout)["hooks"]["pre-analysis"])

    def test_empty_pending_decision_is_not_a_valid_partial_brief(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "partial.md"
            path.write_text(text.split("## ALIGNED PLAN")[0] + "## DECISION SPLIT (AWAITING USER INPUT)\n", encoding="utf-8")
            result = self.run_cli("validate", path, "--json")
            self.assertNotEqual(result.returncode, 0)

    def test_context_rejects_traversal_and_absence_does_not_create_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_cli("context", "--project-root", root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "absent")
            self.assertEqual(list(root.iterdir()), [])
            memory = root / "docs/polylens/memory"
            memory.mkdir(parents=True)
            (root / "private.md").write_text("private", encoding="utf-8")
            (memory / "index.json").write_text(json.dumps({"project-context": "../../../private.md"}), encoding="utf-8")
            result = self.run_cli("context", "--project-root", root)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("private\"", result.stdout)

    def test_project_context_loads_only_the_indexed_current_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = Path(directory) / "docs/polylens/memory"
            memory.mkdir(parents=True)
            (memory / "index.json").write_text(json.dumps({"project-context": "261024_project-context_r2.md"}), encoding="utf-8")
            (memory / "261024_project-context_r2.md").write_text("Confirmed budget: 10K", encoding="utf-8")
            (memory / "261023_project-context_r1.md").write_text("Old budget: 20K", encoding="utf-8")
            result = self.run_cli("context", "--project-root", directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            snapshot = json.loads(result.stdout)
            self.assertEqual(snapshot["sources"]["project-context"]["content"], "Confirmed budget: 10K")
            self.assertIn("project-preferences", snapshot["missing_classes"])

    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, "-B", str(HARNESS), *map(str, arguments)], capture_output=True, text=True)

    def config(self, directory, name, data):
        path = Path(directory) / name
        path.write_text("---\n" + json.dumps(data, indent=2) + "\n---\n", encoding="utf-8")
        return path

    def test_nested_configuration_survives_plan_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            orchestration = self.config(directory, "orchestration.md", {"mode": "sequential", "instances": [
                {"name": "technical", "lenses": ["CTO", "CISO"], "reasoning": {"depth": "deep"}},
                {"name": "business", "depends_on": "technical", "lenses": ["CEO", "CFO"]},
            ]})
            reasoning = self.config(directory, "reasoning.md", {"reasoning": {"depth": "deep", "min_lenses": 3, "max_lenses": 4, "constraints": ["no network"], "output": {"format": "concise"}}})
            validation = self.config(directory, "validation.md", {"validation": {"contract": False, "quality_gate": False, "consistency": False, "regression": True, "baseline_file": "baseline.md"}})
            result = self.run_cli("run", "Migration", "--orchestration", orchestration, "--reasoning", reasoning, "--validation", validation, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            self.assertEqual([i["name"] for i in plan["orchestration"]["instances"]], ["technical", "business"])
            self.assertEqual(plan["orchestration"]["instances"][0]["reasoning"]["depth"], "deep")
            self.assertEqual(plan["reasoning"]["constraints"], ["no network"])
            self.assertEqual(plan["reasoning"]["output_format"], "concise")
            self.assertFalse(plan["validation"]["contract"])
            self.assertTrue(plan["validation"]["regression"])

    def test_invalid_configuration_is_rejected_instead_of_silently_defaulted(self):
        cases = [
            ("--reasoning", {"reasoning": {"depth": "turbo"}}),
            ("--reasoning", {"reasoning": {"min_lenses": 4, "max_lenses": 2}}),
            ("--reasoning", {"reasoning": {"constraints": "no network"}}),
            ("--validation", {"validation": {"contract": "false"}}),
            ("--reasoning", {"reasoning": {"typo": True}}),
            ("--orchestration", {"instances": [{"name": "a", "depends_on": "b"}, {"name": "b", "depends_on": "a"}]}),
            ("--orchestration", {"instances": [{"name": "a"}, {"name": "a"}]}),
        ]
        with tempfile.TemporaryDirectory() as directory:
            for option, data in cases:
                with self.subTest(data=data):
                    path = self.config(directory, "invalid.md", data)
                    result = self.run_cli("run", "test", option, path, "--json")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Harness error:", result.stderr)
            path = Path(directory) / "nested-yaml.md"
            path.write_text("---\nreasoning:\n  depth: deep\n---\n", encoding="utf-8")
            result = self.run_cli("run", "test", "--reasoning", path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("JSON frontmatter", result.stderr)

    def test_validation_failure_returns_nonzero_status(self):
        result = self.run_cli("validate", ROOT / "Readme.md", "--json")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)["contract"]["passed"])

    def test_full_and_pending_decision_briefs_have_distinct_valid_contracts(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            partial = text.split("## ALIGNED PLAN")[0] + """## DECISION SPLIT (AWAITING USER INPUT)
Decision needed: Choose the launch approach
Why escalation happened: Non-negotiable scope requirements conflict
## OPTION A
Supported by: CTO
What changes: Narrow to online editing
Upside: Lower implementation effort
Downside: No offline access
## OPTION B
Supported by: CEO
What changes: Include offline editing
Upside: Wider access
Downside: More implementation effort
What the user should answer: Choose online-only or offline support
What remains blocked until then: Launch scope
"""
            for brief in (text, partial):
                path.write_text(brief, encoding="utf-8")
                result = self.run_cli("validate", path, "--json")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(json.loads(result.stdout)["contract"]["passed"])
            path.write_text(text.replace("Verdict: GO", "Verdict: MAYBE", 1), encoding="utf-8")
            result = self.run_cli("validate", path, "--json")
            self.assertNotEqual(result.returncode, 0)

    def test_regression_detects_changed_verdicts_without_treating_timelines_as_conflicts(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            baseline = Path(directory) / "baseline.md"
            baseline.write_text(text, encoding="utf-8")
            current = Path(directory) / "current.md"
            current.write_text(text, encoding="utf-8")
            config = self.config(directory, "validation.md", {"validation": {"contract": True, "consistency": True, "regression": True, "baseline_file": "baseline.md"}})
            result = self.run_cli("validate", current, "--config", config, "--json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            current.write_text(text.replace("Verdict: GO", "Verdict: MODIFY", 1), encoding="utf-8")
            result = self.run_cli("validate", current, "--config", config, "--json")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(json.loads(result.stdout)["regression"]["passed"])

    def test_regression_detects_a_changed_recommendation_with_identical_headings_and_verdicts(self):
        text = (ROOT / "tests/fixtures/brief-valid.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "baseline.md").write_text(text, encoding="utf-8")
            current = Path(directory) / "current.md"
            current.write_text(text.replace("Proceed with the reversible pilot.", "Cancel the pilot."), encoding="utf-8")
            config = self.config(directory, "validation.md", {"validation": {"regression": True, "baseline_file": "baseline.md"}})
            result = self.run_cli("validate", current, "--config", config, "--json")
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(json.loads(result.stdout)["regression"]["delta"]["content_changed"])


if __name__ == "__main__":
    unittest.main()
