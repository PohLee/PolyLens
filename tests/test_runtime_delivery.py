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
import runtime_bundle
from runtime_bundle import build_bundle, verify_bundle
from install_bundle import install, MARKER, OWNERSHIP
from unittest.mock import patch


class RuntimeDeliveryTests(unittest.TestCase):
    def test_direct_build_rejects_stale_projections_before_touching_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "checkout"
            for name in ("tools", "prompts", "lenses", "engines", "skills", "orchestrators", "hooks", "harness"):
                shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            registry = root / "prompts/lens-registry.md"
            registry.write_text(registry.read_text(encoding="utf-8").replace("database choice", "database selection"), encoding="utf-8")
            for nested in (False, True):
                output = Path(directory) / str(nested)
                output.mkdir()
                note = output / "previous.txt"
                note.write_text("previous build", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "stale generated"):
                    build_bundle(output, nested, root)
                self.assertEqual(note.read_text(encoding="utf-8"), "previous build")
            self.assertNotIn("database selection", (root / "orchestrators/polylens-pre-fight.md").read_text(encoding="utf-8"))

    def test_captured_release_verification_needs_no_live_source_and_rejects_content_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            for nested in (False, True):
                output = Path(directory) / str(nested)
                release = build_bundle(output, nested)
                with patch("runtime_bundle.runtime_files", side_effect=AssertionError("must not re-read source")):
                    release.verify(output)
                    shared = output / "polylens/shared" if nested else output / "shared"
                    path = shared / "prompts/lens-registry.md"
                    path.write_text(path.read_text(encoding="utf-8").replace("database choice", "database selection"), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "content.*lens-registry"):
                        release.verify(output)

    def test_projection_freshness_is_checked_against_captured_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "checkout"
            for name in ("tools", "prompts", "lenses", "engines", "skills", "orchestrators", "hooks", "harness"):
                shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            registry = root / "prompts/lens-registry.md"
            original = registry.read_text(encoding="utf-8")
            capture = runtime_bundle.runtime_files

            def change_at_capture(source):
                registry.write_text(original.replace("database choice", "database selection"), encoding="utf-8")
                return capture(source)

            for nested in (False, True):
                registry.write_text(original, encoding="utf-8")
                with patch.object(runtime_bundle, "runtime_files", side_effect=change_at_capture):
                    with self.assertRaisesRegex(ValueError, "stale generated"):
                        build_bundle(Path(directory) / str(nested), nested, root)

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
