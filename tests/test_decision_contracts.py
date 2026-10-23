"""Static protocol invariants, not a claim that a model follows them."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_markdown_contracts as contracts


class DecisionContractTests(unittest.TestCase):
    def test_all_modes_have_current_generated_lens_contracts(self):
        errors = []
        contracts.validate_lens_projections(errors)
        self.assertEqual(errors, [])

    def test_missing_decision_gate_is_rejected(self):
        original = contracts.read_text
        def without_gate(path):
            return original(path).replace("canonical conflict count is zero", "UNANIMOUS")
        errors = []
        with patch.object(contracts, "read_text", side_effect=without_gate):
            contracts.validate_decision_protocol(errors)
        self.assertTrue(any("canonical conflict count" in e for e in errors))

    def test_decision_protocol_has_independent_alignment_and_conflict_states(self):
        errors = []
        contracts.validate_decision_protocol(errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
