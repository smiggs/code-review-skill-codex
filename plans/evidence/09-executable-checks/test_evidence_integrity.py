"""Checks that routine reproduction preserves recorded audit evidence."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


class EvidenceIntegrityTests(unittest.TestCase):
    def test_reproduction_keeps_recorded_results_unchanged(self):
        with tempfile.TemporaryDirectory(prefix="package-09-integrity-") as directory:
            root = Path(directory)
            harness = root / HERE.relative_to(ROOT)
            shutil.copytree(HERE, harness, ignore=shutil.ignore_patterns("__pycache__", ".generated", "target"))
            (root / "reference").mkdir()
            for language in ("go", "rust"):
                shutil.copy(ROOT / "reference" / f"{language}.md", root / "reference")
            # A local prose edit must not replace the previous audit's source identity.
            with (root / "reference/go.md").open("a") as source:
                source.write("\n")
            recorded = {p.relative_to(harness): p.read_bytes()
                        for p in (harness / "results").rglob("*") if p.is_file()}
            for script in ("extract.py", "verify.py"):
                result = subprocess.run([sys.executable, str(harness / script)],
                                        cwd=root, text=True, capture_output=True, timeout=180)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            after = {p.relative_to(harness): p.read_bytes()
                     for p in (harness / "results").rglob("*") if p.is_file()}
            changed = sorted(str(path) for path in recorded.keys() | after.keys()
                             if recorded.get(path) != after.get(path))
            self.assertEqual(changed, [], "Routine reproduction changed recorded evidence")
            self.assertTrue((harness / ".generated/results/source-identities.json").is_file())
            self.assertTrue((harness / ".generated/results/fixture-rust-head.txt").is_file())


if __name__ == "__main__":
    unittest.main()
