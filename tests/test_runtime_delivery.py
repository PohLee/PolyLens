"""Exercise the validator and release bundles as a user would, without installing globally."""

import shutil
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_standard_bundle
import build_opencode_bundle
from runtime_bundle import build_bundle, verify_bundle
from install_bundle import install, MARKER, OWNERSHIP
from unittest.mock import patch


class RuntimeDeliveryTests(unittest.TestCase):
    @unittest.skipUnless(sys.platform == "win32", "Windows junction regression")
    def test_installer_refuses_junctions_without_path_is_junction_support(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "previous"
            source.mkdir()
            (source / MARKER).write_text(json.dumps(OWNERSHIP), encoding="utf-8")
            target = root / "skills"
            target.mkdir()
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(target / "shared"), str(source)], capture_output=True, text=True)
            if result.returncode:
                self.skipTest("Cannot create a temporary Windows junction")
            with patch.object(Path, "is_junction", lambda self: False, create=True):
                with self.assertRaisesRegex(ValueError, "linked"):
                    install(target, False)

    def test_release_verification_rejects_a_missing_lens_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            for nested in (False, True):
                output = Path(directory) / str(nested)
                build_bundle(output, nested)
                shared = output / "polylens/shared" if nested else output / "shared"
                (shared / "lenses/lens-cto.md").unlink()
                with self.assertRaisesRegex(ValueError, "lens-cto"):
                    verify_bundle(output, nested)

    def test_safe_reinstallation_preserves_previous_files_and_runs_outside_the_repo(self):
        with tempfile.TemporaryDirectory() as directory:
            for layout in ("standard", "opencode"):
                target = Path(directory) / layout
                command = [sys.executable, "-B", str(ROOT / "tools/install_bundle.py"), "--target", str(target), "--layout", layout]
                result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                (target / "polylens/custom-note.txt").write_text("my local notes", encoding="utf-8")
                result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                backups = list(target.glob(".polylens-backup-*/polylens/custom-note.txt"))
                self.assertEqual(len(backups), 1)
                self.assertEqual(backups[0].read_text(encoding="utf-8"), "my local notes")
                shared = target / "polylens/shared" if layout == "opencode" else target / "shared"
                result = subprocess.run([sys.executable, "-B", str(shared / "tools/harness.py"), "run", "Smoke test", "--json"], cwd=directory, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_installer_refuses_to_replace_an_unowned_shared_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skills"
            (target / "shared").mkdir(parents=True)
            note = target / "shared/other-project.txt"
            note.write_text("keep this", encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/install_bundle.py"), "--target", str(target)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unowned", result.stderr)
            self.assertEqual(note.read_text(encoding="utf-8"), "keep this")
            self.assertFalse((target / "polylens").exists())

    def test_each_release_bundle_contains_a_runnable_harness(self):
        with tempfile.TemporaryDirectory() as directory:
            for builder, nested in ((build_standard_bundle, False), (build_opencode_bundle, True)):
                with self.subTest(builder=builder.__name__):
                    output = Path(directory) / builder.__name__
                    with patch.object(builder, "DIST_DIR", output), patch.object(builder, "ROOT", Path(directory)), contextlib.redirect_stdout(io.StringIO()):
                        builder.main()
                    shared = output / "polylens" / "shared" if nested else output / "shared"
                    harness = shared / "tools" / "harness.py"
                    self.assertTrue(harness.is_file(), f"missing installed tool: {harness}")
                    result = subprocess.run([sys.executable, "-B", str(harness), "hooks", "list"], cwd=directory, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_contract_validation_does_not_require_generated_artifact_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            for name in ("tools", "prompts", "lenses", "engines", "skills", "orchestrators", "hooks", "harness", "tests"):
                shutil.copytree(ROOT / name, checkout / name, ignore=shutil.ignore_patterns("__pycache__"))
            (checkout / "docs" / "polylens").mkdir(parents=True)
            shutil.copyfile(ROOT / "docs" / "polylens" / "README.md", checkout / "docs" / "polylens" / "README.md")
            shutil.copyfile(ROOT / "LICENSE", checkout / "LICENSE")
            result = subprocess.run(
                [sys.executable, "-B", str(checkout / "tools" / "validate_markdown_contracts.py")],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
