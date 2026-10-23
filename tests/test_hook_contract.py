"""The same Hook input has the same meaning in runtime and repository checks."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from harness import HookRegistry
import validate_markdown_contracts as contracts


class HookContractTests(unittest.TestCase):
    def test_json_and_flat_hooks_share_defaults_in_both_consumers(self):
        metadata = {"hook": "pre-analysis", "name": "sample"}
        for frontmatter in (json.dumps(metadata), "hook: pre-analysis\nname: sample"):
            with self.subTest(frontmatter=frontmatter), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                path = root / "hooks/pre-analysis/sample.md"
                path.parent.mkdir(parents=True)
                path.write_text("---\n" + frontmatter + "\n---\nBody\n", encoding="utf-8")
                hook = HookRegistry.load(root / "hooks").hooks[0]
                self.assertEqual((hook.order, hook.enabled, hook.hook_type), (99, False, "markdown"))
                errors = []
                with patch.object(contracts, "ROOT", root):
                    contracts.validate_hook_frontmatter(path, errors)
                self.assertEqual(errors, [])

    def test_invalid_metadata_cannot_be_supplied_by_the_body(self):
        cases = [
            ({"hook": "pre-analysis"}, "name: sample"),
            ({"hook": "review", "name": "sample"}, "hook: pre-analysis"),
            ({"hook": "pre-analysis", "name": "sample", "enabled": "false"}, "enabled: false"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "hooks/pre-analysis/sample.md"
            path.parent.mkdir(parents=True)
            for metadata, body in cases:
                path.write_text("---\n" + json.dumps(metadata) + "\n---\n" + body, encoding="utf-8")
                with self.assertRaises(ValueError):
                    HookRegistry.load(root / "hooks")
                errors = []
                with patch.object(contracts, "ROOT", root):
                    contracts.validate_hook_frontmatter(path, errors)
                self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
