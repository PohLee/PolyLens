"""Structural regression tests; these do not execute or grade model responses."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import validate_markdown_contracts as contracts


class PRCrisisContractTests(unittest.TestCase):
    def test_current_pr_contract(self) -> None:
        errors: list[str] = []
        contracts.validate_pr_crisis_recovery(errors)
        self.assertEqual(errors, [])

    def test_missing_contract_parts_are_rejected(self) -> None:
        mutations = [
            ("evidence gate", "prompts/playbooks/pr-crisis-recovery.md", "### 1. Evidence Ledger"),
            ("coupled signals", "prompts/playbooks/pr-crisis-recovery.md", "Displacement signal"),
            (
                "update discipline",
                "prompts/playbooks/pr-crisis-recovery.md",
                "A user's disagreement alone is not new factual evidence",
            ),
            (
                "executive route",
                "orchestrators/polylens-executive-review.md",
                "../shared/playbooks/pr-crisis-recovery.md",
            ),
            (
                "pre-fight route",
                "orchestrators/polylens-pre-fight.md",
                "../shared/playbooks/pr-crisis-recovery.md",
            ),
            (
                "focused route",
                "skills/polylens-lens-review/SKILL.md",
                "../shared/playbooks/pr-crisis-recovery.md",
            ),
            ("fixture coverage", "tests/fixtures/pr-crisis-recovery.md", "## PR-10 \u2014"),
        ]
        original_read = contracts.read_text
        for name, relative, marker in mutations:
            with self.subTest(name=name):
                target = contracts.ROOT / relative
                self.assertIn(marker, original_read(target))

                def changed_read(path):
                    text = original_read(path)
                    return text.replace(marker, "removed-for-test") if path == target else text

                with patch.object(contracts, "read_text", changed_read):
                    errors: list[str] = []
                    contracts.validate_pr_crisis_recovery(errors)
                    self.assertTrue(errors, f"Missed removed {name}")

    def test_playbook_loaded_after_lens_selection_is_rejected(self) -> None:
        original_read = contracts.read_text
        pointer = "../shared/playbooks/pr-crisis-recovery.md"

        def changed_read(path):
            text = original_read(path)
            if path == contracts.EXEC_REVIEW_PATH:
                return text.replace(pointer, "removed-for-test") + "\n" + pointer
            return text

        with patch.object(contracts, "read_text", changed_read):
            errors: list[str] = []
            contracts.validate_pr_crisis_recovery(errors)
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
