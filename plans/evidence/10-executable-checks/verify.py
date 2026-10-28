"""Run bounded fixture-sensitivity checks for the retained Java guidance.

For each prepared fixture pair, the clean ``base`` and the defective ``head``
are compiled into an isolated copy of the Maven module and examined by the
contract test declared in ``fixtures``. The head must fail the contract for
the expected reason; the base must pass. This proves the assertions separate
the variants; it measures no model review behaviour.
"""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
RESULTS = HERE / ".generated/results"
RESULTS.mkdir(parents=True, exist_ok=True)

CACHE = Path.home() / ".cache/cr-plan-10"
MVB = Path(os.environ.get("MVN_BIN", str(CACHE / "tools/apache-maven-3.9.9/bin/mvn")))
JAVA_HOME = Path(os.environ.get("JDK21_HOME", str(CACHE / "tools/jdk-21.0.13+9")))
REPO = ["-Dmaven.repo.local=" + os.environ.get("M2_REPO", str(CACHE / "m2")), "-o"]


def run(name, command, cwd, *, seconds, expect_failure=None):
    environment = dict(subprocess.os.environ)
    environment["JAVA_HOME"] = str(JAVA_HOME)
    environment["PATH"] = str(JAVA_HOME / "bin") + subprocess.os.pathsep + environment.get("PATH", "")
    try:
        result = subprocess.run(
            command, cwd=cwd, text=True, capture_output=True, timeout=seconds, env=environment)
    except subprocess.TimeoutExpired as timeout:
        (RESULTS / f"{name}.txt").write_text(
            (timeout.stdout or "") + (timeout.stderr or "") + "\n[verify harness process timeout]")
        raise RuntimeError(f"{name} exceeded the {seconds}s bound") from timeout
    output = (result.stdout or "") + (result.stderr or "")
    (RESULTS / f"{name}.txt").write_text(output)
    if expect_failure is None:
        if result.returncode:
            raise RuntimeError(f"{name} exited {result.returncode}:\n{output[-3000:]}")
        print(f"{name}: passed")
    else:
        if result.returncode == 0 or expect_failure not in output:
            raise RuntimeError(
                f"{name} did not fail for the expected reason ({expect_failure}):\n{output[-3000:]}")
        print(f"{name}: expected defect detected")


PAIRS = (
    {
        "name": "jpa-membership",
        "target": "fixture/ParentReader.java",
        "test_selection": "-Dtest=ParentReaderContractTest",
        "bound": 180,
        "expected_reason": "every requested parent must be preserved",
    },
    {
        "name": "failure-observability",
        "target": "fixture/BatchRunner.java",
        "test_selection": "-Dtest=BatchRunnerContractTest",
        "bound": 180,
        "expected_reason": "all three nightly jobs must publish an outcome",
    },
)


def copy_module(case: Path):
    (case / "src/test/java/invalid/example/package10").mkdir(parents=True)
    shutil.copy(HERE / "pom.xml", case / "pom.xml")
    for source in (HERE / "src/test/java/invalid/example/package10").glob("*.java"):
        shutil.copy(source, case / "src/test/java/invalid/example/package10")
    shutil.copytree(
        HERE / "src/test/java/invalid/example/package10/fixturesupport",
        case / "src/test/java/invalid/example/package10/fixturesupport",
    )


def main():
    if not MVB.exists():
        raise SystemExit(f"Maven not found at {MVB}")
    with tempfile.TemporaryDirectory(prefix="package-10-checks-") as work:
        for pair in PAIRS:
            for state in ("head", "base"):
                case = Path(work) / f"{pair['name']}-{state}"
                copy_module(case)
                target = case / "src/test/java/invalid/example/package10" / pair["target"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(HERE / f"fixtures/{pair['name']}/{state}/{Path(pair['target']).name}", target)
                run(
                    f"fixture-{pair['name']}-{state}",
                    [str(MVB), *REPO, "test", pair["test_selection"],
                     "-Dpackage10fixture=true", "-Dsurefire.exitOnFailure=false"],
                    case,
                    seconds=pair["bound"],
                    expect_failure=pair["expected_reason"] if state == "head" else None,
                )
    print("Both defective heads rejected; both clean bases passed. No model accuracy score.")


if __name__ == "__main__":
    main()
