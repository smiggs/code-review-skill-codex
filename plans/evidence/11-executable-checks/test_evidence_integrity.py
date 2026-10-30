"""Evidence-integrity regression for the package 11 harness.

Re-runs extraction and the C/C++ checks in an isolated checkout with a
local prose edit, then verifies that (a) the recorded evidence directory
was not touched and (b) the fresh output is byte-for-byte identical to the
recorded run. Run from the repository root after recording evidence.
"""
import filecmp
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SANDBOX = Path.home() / ".cache" / "cr-plan-11" / ".integrity-check"

recorded = HERE / "results" / "run-checks.txt"
if not recorded.exists():
    print("SKIP: no recorded evidence in results/ yet")
    sys.exit(0)

snapshot = {}
for path in sorted((HERE / "results").iterdir()):
    if path.is_file():
        snapshot[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()

if SANDBOX.exists():
    shutil.rmtree(SANDBOX)
SANDBOX.mkdir(parents=True)
for item in ROOT.iterdir():
    if item.name in (".git", ".generated", "plans"):
        continue
    if item.is_dir():
        shutil.copytree(item, SANDBOX / item.name)
    else:
        shutil.copyfile(item, SANDBOX / item.name)
shutil.copytree(HERE, SANDBOX / "plans" / "evidence" / "11-executable-checks",
                ignore=shutil.ignore_patterns(".generated"))

guide = SANDBOX / "reference" / "c.md"
text = guide.read_text()
assert text.rstrip().endswith("separate process.")
guide.write_text(text.rstrip() + " Integrity probe.\n")

env_out = subprocess.run(
    [sys.executable, str(SANDBOX / "plans" / "evidence" /
                         "11-executable-checks" / "extract.py")],
    capture_output=True, text=True)
if env_out.returncode != 0:
    print(env_out.stderr)
    sys.exit(1)
cmd = [sys.executable, str(SANDBOX / "plans" / "evidence" /
                           "11-executable-checks" / "run_checks.py")]
default_prefix = Path.home() / ".cache" / "cr-plan-11" / "prefix"
if (default_prefix / "lib" / "libQt6Core.so.6").exists():
    cmd += ["--qt-prefix", str(default_prefix)]
run_out = subprocess.run(cmd, capture_output=True, text=True)
if run_out.returncode != 0:
    print(run_out.stdout[-2000:])
    print(run_out.stderr[-2000:])
    sys.exit(1)

failures = 0
for name, digest in snapshot.items():
    current = hashlib.sha256((HERE / "results" / name).read_bytes()).hexdigest()
    if current != digest:
        print(f"RECORDED EVIDENCE MODIFIED: {name}")
        failures += 1
if not filecmp.cmp(recorded,
                   SANDBOX / "plans" / "evidence" / "11-executable-checks" /
                   ".generated" / "results" / "run-checks.txt", shallow=False):
    print("FRESH RUN OUTPUT DIFFERS FROM RECORDED run-checks.txt")
    failures += 1

if failures:
    sys.exit(1)
print(f"INTEGRITY-OK: {len(snapshot)} recorded files unchanged; "
      "fresh C/C++ run matches recorded output byte for byte")
