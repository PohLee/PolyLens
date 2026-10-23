"""Authoring changes through the Registry and projection interfaces."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lens_contract import parse_registry, sync_projections, projection_errors


class LensContractTests(unittest.TestCase):
    def copy_sources(self, root):
        for name in ("prompts", "orchestrators", "skills/polylens-lens-review"):
            shutil.copytree(ROOT / name, root / name)

    def test_empty_field_cannot_consume_the_next_line(self):
        text = (ROOT / "prompts/lens-registry.md").read_text(encoding="utf-8")
        # Keep the rest of the real Registry so only the empty value is invalid.
        text = text.replace("- **focus:** Speed, growth, market direction, and competitive advantage", "- **focus:**")
        with self.assertRaisesRegex(ValueError, "CEO.*focus"):
            parse_registry(text)

    def test_invalid_registry_never_reaches_generation(self):
        text = (ROOT / "prompts/lens-registry.md").read_text(encoding="utf-8")
        variants = [
            text.replace("- **active:** true", "- **active:** maybe", 1),
            text.replace("- **active:** true", "- **active:** true\n- **active:** false", 1),
            text.replace("- **pairs_with:** CTO, CPO, YC, CFO, COO, CBDO, CHRO, CRO", "- **pairs_with:** UNKNOWN"),
            text.replace("### CTO —", "### CEO —", 1),
        ]
        for variant in variants:
            with self.subTest(variant=variant[:50]):
                with self.assertRaises(ValueError):
                    parse_registry(variant)

    def test_malformed_lens_headings_cannot_be_ignored_or_lend_fields(self):
        text = (ROOT / "prompts/lens-registry.md").read_text(encoding="utf-8")
        variants = [
            text.replace("### CTO — Technical & Infrastructure", "### CTO — Technical & Infrastructure\n\n### NEW-LENS — Invalid ID"),
            text.replace("## Selection Algorithm", "### NEW-LENS — Invalid ID\n\n## Selection Algorithm"),
            text.replace("### CTO —", "### cto —"),
        ]
        for variant in variants:
            with self.assertRaisesRegex(ValueError, "heading"):
                parse_registry(variant)

    def test_sync_preserves_handwritten_content_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_sources(root)
            path = root / "orchestrators/polylens-pre-fight.md"
            note = "\n## Author Notes\nKeep this handwritten instruction.\n"
            path.write_text(path.read_text(encoding="utf-8") + note, encoding="utf-8")
            sync_projections(root)
            once = path.read_text(encoding="utf-8")
            self.assertTrue(once.endswith(note))
            sync_projections(root)
            self.assertEqual(path.read_text(encoding="utf-8"), once)
            self.assertEqual(projection_errors(root), [])

    def test_invalid_generated_markers_fail_without_writing_any_documents(self):
        for change in ("missing", "duplicate", "reversed"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.copy_sources(root)
                path = root / "orchestrators/polylens-pre-fight.md"
                text = path.read_text(encoding="utf-8")
                begin, end = "<!-- BEGIN GENERATED LENSES -->", "<!-- END GENERATED LENSES -->"
                if change == "missing":
                    text = text.replace(end, "")
                elif change == "duplicate":
                    text += "\n" + begin
                else:
                    text = text.replace(begin, "SWAP").replace(end, begin).replace("SWAP", end)
                path.write_text(text, encoding="utf-8")
                before = {p: p.read_bytes() for p in root.rglob("*.md")}
                with self.assertRaises(ValueError):
                    sync_projections(root)
                self.assertEqual({p: p.read_bytes() for p in root.rglob("*.md")}, before)

    def test_selection_projections_do_not_depend_on_editorial_heading_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_sources(root)
            registry = root / "prompts/lens-registry.md"
            registry.write_text(registry.read_text(encoding="utf-8").replace(
                "## Selection Algorithm (for orchestrator reference)", "## Lens Selection").replace(
                "Example guidance:", "Examples:"), encoding="utf-8")
            sync_projections(root)
            self.assertEqual(projection_errors(root), [])


if __name__ == "__main__":
    unittest.main()
