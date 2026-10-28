# Package 09 executable checks

This development-only harness extracts every Go and Rust code fence from the
retained guides. Generated source files are ignored; tests compile those exact
bodies with a Rust test-module adapter. It does not invoke a model reviewer.

## Reproduction

Use Linux/x86_64, Go 1.22.12, Rust/Cargo 1.85.0, Python 3.10+, and a working C
compiler/linker. The exercised C driver was GCC 12.5.0. Put `go`, `cargo`, and
`rustc` on PATH. Set `CC` for Go race checks and `RUSTFLAGS` with `-C linker=PATH`
if the compiler driver is not the default `cc`. Isolated `GOCACHE`, `CARGO_HOME`,
and `CARGO_TARGET_DIR` values can keep generated files outside the checkout.
Fetch public dependencies once, then use the checked-in lockfile offline.
No system installation or repository CI change is required.

From the repository root:

```bash
python3 plans/evidence/09-executable-checks/extract.py
cargo fetch --manifest-path plans/evidence/09-executable-checks/rust/Cargo.toml --locked
go test -C plans/evidence/09-executable-checks/go -race -v -timeout 20s ./...
cargo test --manifest-path plans/evidence/09-executable-checks/rust/Cargo.toml --locked --offline
cargo test --manifest-path plans/evidence/09-executable-checks/rust/Cargo.toml --locked --offline --release
python3 plans/evidence/09-executable-checks/verify.py
python3 -B plans/evidence/09-executable-checks/test_evidence_integrity.py
```

Routine extraction and verification write fresh identities and outputs under
ignored `.generated/results/`; they preserve recorded `results/` and its
candidate manifest. The integrity regression executes both scripts in an
isolated checkout with a local guide edit and compares every recorded byte.
Copy fresh results and refresh the candidate manifest only when deliberately
preparing replacement evidence.

`verify.py` creates temporary modules for the Go 1.21/1.22 loop comparison, the
Rust 2024 comparison, and the two defect/clean fixture pairs. Its subprocesses
have a 90-second bound; Go tests have a 15-second process bound and two-second
operation waits. Rust controlled readers use manually polled gates, with
two-second waits for task signals and shutdown. The blocking callback has a
two-second escape bound. This is synthetic runtime evidence; no production I/O,
full runtime matrix, performance measurement, or proof of unsafe soundness is
claimed. Deliberate Rust task panic output belongs to a passing join-error control.

Captured results are in [results](results/). Trailing whitespace from terminal
output is trimmed; diagnostic and assertion text is preserved. The
[source identities](results/source-identities.json) identify extracted guide
bytes. The [primary-source identities](results/primary-source-identities.json)
identify inspected files from the installed Go archive and locked Tokio crate.
The lockfile records crate checksums. Toolchains and caches are disposable `/tmp`
content and are not part of the candidate.

The earlier `go-green.txt` contains the initial four tests; `go-race.txt` contains
the final nine top-level Go tests. `rust-build.txt` records the initial test-module
path error, which was corrected before runtime tests. `sensitivity-final.txt`
adds the edition-2024 check to the earlier sensitivity run. Negative logs are
intentional assertion failures and are not passing suite outputs.

## Miri follow-up

The [Miri verification record](miri-verification.md) supersedes the initial
missing-command limitation: isolated installation succeeded, all ten Rust tests
passed under one seed/target, and the inherited debug-only bounds wrapper was
rejected by the interpreter. It records installation, commands, and limits.

## Evaluation boundary

The [fixtures](fixtures/README.md) are prepared for a separately agreed review
exercise. Sensitivity checks prove that the assertions distinguish these defect
and clean variants. They do not measure model detection, false positives,
severity calibration, or evidence quality. Do not provide the harness, answer
key, audit narrative, or result logs to a future reviewer whose answers are
meant to be independent.
