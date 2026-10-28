"""Run bounded compiler checks and fixture sensitivity checks, without model reviews."""
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
RESULTS = HERE / ".generated/results"
RESULTS.mkdir(parents=True, exist_ok=True)
if (HERE / "go/examples.go").read_bytes() != (HERE / "fixtures/go-worker/base/pool.go").read_bytes():
    raise ValueError("Go fixture base no longer matches extracted guide")

def run(name, command, cwd, *, failure=None):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=90)
    output = result.stdout + result.stderr
    (RESULTS / f"{name}.txt").write_text(output)
    if failure is None:
        if result.returncode:
            raise RuntimeError(f"{name} exited {result.returncode}: {output}")
    elif result.returncode == 0 or failure not in output:
        raise RuntimeError(f"{name} did not fail for the expected reason: {output}")
    print(f"{name}: {'expected defect detected' if failure else 'passed'}")

with tempfile.TemporaryDirectory(prefix="package-09-checks-") as directory:
    work = Path(directory)
    for version, expected in (("1.21", "[3 3 3]"), ("1.22", "[1 2 3]")):
        case = work / version
        case.mkdir()
        (case / "go.mod").write_text(f"module example.invalid/loop\n\ngo {version}\n")
        (case / "main.go").write_text('''package main
import "fmt"
func main() {
    declared := []func() int{}
    for _, value := range []int{1,2,3} {
        declared = append(declared,func() int {return value})
    }
    var value int
    assigned := []func() int{}
    for _, value = range []int{1,2,3} {
        assigned = append(assigned,func() int {return value})
    }
    a,b := []int{},[]int{}
    for i:=range declared {a=append(a,declared[i]());b=append(b,assigned[i]())}
    fmt.Println(a,b)
}
''')
        run(f"loop-{version}", ["go", "run", "."], case)
        actual=(RESULTS / f"loop-{version}.txt").read_text().strip()
        if actual != f"{expected} [3 3 3]":
            raise AssertionError(f"module {version}: {actual}")
    for state in ("head", "base"):
        case = work / f"go-{state}"
        case.mkdir()
        shutil.copy(HERE / "go/go.mod", case)
        for path in (HERE / "go").glob("*_test.go"):
            shutil.copy(path, case)
        shutil.copy(HERE / f"fixtures/go-worker/{state}/pool.go", case / "examples.go")
        run(f"fixture-go-{state}", ["go", "test", "-count=1", "-v", "-timeout", "15s", "-run",
            "TestNonpositiveNonemptyTerminates|TestCancellationAndBound", "."], case,
            failure="operation did not terminate" if state == "head" else None)
    case = work / "rust-2024"
    (case / "src").mkdir(parents=True)
    for filename in ("Cargo.lock", "tests.rs"):
        shutil.copy(HERE / f"rust/{filename}", case)
    manifest = (HERE / "rust/Cargo.toml").read_text().replace('edition = "2021"', 'edition = "2024"')
    (case / "Cargo.toml").write_text(manifest)
    shutil.copy(HERE / "rust/src/lib.rs", case / "src/lib.rs")
    run("rust-edition-2024", ["cargo", "test", "--locked", "--offline"], case)
    clean = (HERE / "fixtures/rust-reader/base/reader.rs").read_text()
    head = (HERE / "fixtures/rust-reader/head/reader.rs").read_text()
    for state in ("head", "base"):
        case = work / f"rust-{state}"
        (case / "src").mkdir(parents=True)
        for filename in ("Cargo.toml", "Cargo.lock", "tests.rs"):
            shutil.copy(HERE / f"rust/{filename}", case)
        code=(HERE / "rust/src/lib.rs").read_text()
        if clean not in code:
            raise ValueError("Rust fixture base no longer matches extracted guide")
        if state == "head":
            code=code.replace(clean,head)
        (case / "src/lib.rs").write_text(code)
        run(f"fixture-rust-{state}", ["cargo", "test", "--locked", "--offline",
            "partial_frame_survives_cancellation", "--", "--nocapture"], case,
            failure="assertion `left == right` failed" if state == "head" else None)
print("Two defect fixtures rejected; both clean controls passed. No model accuracy score.")
