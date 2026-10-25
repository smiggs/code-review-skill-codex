"""Checks synthetic fixture integrity and answer-key premises, not review quality."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent
CASES = tuple(f"case-{number:02}" for number in range(1, 11))
ENV = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
       "GIT_TERMINAL_PROMPT": "0", "PYTHONDONTWRITEBYTECODE": "1"}


class FixtureChecks(unittest.TestCase):
    def observe(self, case, version, code, expected):
        with tempfile.TemporaryDirectory(prefix="review-premise-") as directory:
            shutil.copytree(ROOT / "fixtures" / case / version, directory, dirs_exist_ok=True)
            result = subprocess.run([sys.executable, "-B", "-c", code], cwd=directory,
                                    env=ENV, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), expected)

    def test_patches_reproduce_heads_without_changing_sources(self):
        for case in CASES:
            with self.subTest(case=case), tempfile.TemporaryDirectory(prefix="review-patch-") as directory:
                fixture = ROOT / "fixtures" / case
                shutil.copytree(fixture / "base", directory, dirs_exist_ok=True)
                patch = fixture / "change.diff"
                result = subprocess.run(["git", "apply", str(patch)], cwd=directory,
                                        env=ENV, capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                actual = {p.relative_to(directory).as_posix(): p.read_bytes()
                          for p in Path(directory).rglob("*") if p.is_file()}
                expected = {p.relative_to(fixture / "head").as_posix(): p.read_bytes()
                            for p in (fixture / "head").rglob("*") if p.is_file()}
                self.assertEqual(actual, expected)

    def test_zero_timeout(self):
        code = "from wait import resolve_timeout; print(resolve_timeout(0), resolve_timeout(None))"
        self.observe("case-01", "base", code, "0 30")
        self.observe("case-01", "head", code, "30 30")

    def test_failed_recovery_preserves_only_copy(self):
        code = """from pathlib import Path
from recovery import recover
source = Path('backup.txt')
source.write_text('only copy', encoding='utf-8')
try:
    recover(source, Path('missing') / 'restored.txt')
except FileNotFoundError:
    pass
print(source.exists())
"""
        self.observe("case-02", "base", code, "True")
        self.observe("case-02", "head", code, "False")

    def test_target_specific_contract_and_clean_counterpart(self):
        code = "from retention import retention_days; print(retention_days(0))"
        self.observe("case-03", "base", code, "0")
        self.observe("case-03", "head", code, "7")
        supported = "from retention import retention_days; print([retention_days(v) for v in (None, 1, 7, 30)])"
        for version in ("base", "head"):
            self.observe("case-10", version, supported, "[7, 1, 7, 30]")

    def test_unchanged_caller(self):
        code = """from caller import render
try:
    print(render())
except TypeError as error:
    print(type(error).__name__)
"""
        self.observe("case-04", "base", code, "ready")
        self.observe("case-04", "head", code, "TypeError")

    def test_clean_refactor(self):
        code = "from total import total; print(total([]), total([1, -2, 3]))"
        for version in ("base", "head"):
            self.observe("case-05", version, code, "0 2")

    def test_existing_defect_and_unrelated_change(self):
        code = """from stats import mean, total
try:
    mean([])
except ZeroDivisionError:
    print('existing', total([1, 2]))
"""
        for version in ("base", "head"):
            self.observe("case-09", version, code, "existing 3")


if __name__ == "__main__":
    unittest.main(verbosity=2)
