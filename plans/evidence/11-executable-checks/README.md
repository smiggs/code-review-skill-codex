# Package 11 executable checks

This development-only harness verifies the claims retained in
`reference/c.md`, `reference/cpp.md`, and `reference/qt.md`. It extracts
every C and C++ code fence from the three guides verbatim, compiles the
extracted units at the declared standards, runs contract tests against the
extracted bytes, and runs fixture-sensitivity checks for the prepared
review fixtures. Qt adapters and fixtures run against a pinned Qt build
when one is supplied. It does not invoke a model reviewer.

## Reproduction

Use Linux/x86_64, Python 3.10+, and a GCC 13.3.0 toolchain with binutils,
glibc headers, and the sanitiser runtimes. This audit executed the checks
from disposable caches outside the checkout (GCC 13.3.0 stack, binutils
2.46.1, glibc 2.39 sysroot, Qt 6.12.0 and its runtime libraries from the
conda-forge channel), so no system installation or repository CI change is
required. With a compiler on `PATH` that can compile and link C11, C++17,
and C++20 with sanitiser support, point `PREFIX` at a prefix whose
`bin/x86_64-conda-linux-gnu-gcc` (and `-g++`) exist and whose sysroot is at
`x86_64-conda-linux-gnu/sysroot`.

The sanitiser runs require disabled address-space randomisation on this
kernel (`setarch -R`); the runner applies it to every execution. A clean
sanitiser run does not prove the absence of undefined behaviour, and no
check relies on a particular observed result from undefined code: the
fixtures' defective variants produce their wrong outputs through defined
behaviour only.

From the repository root:

```bash
python3 plans/evidence/11-executable-checks/extract.py
python3 plans/evidence/11-executable-checks/run_checks.py \
  --qt-prefix /path/to/qt-prefix
python3 -B plans/evidence/11-executable-checks/test_evidence_integrity.py
```

Without `--qt-prefix` the C and C++ sections and the non-Qt fixtures still
run, and the Qt sections are recorded as not run.

`extract.py` publishes every fence from the three guides into ignored
`.generated/guide-src/` and records one identity per fence in
`.generated/results/source-identities.json`. The C units are the four
complete fences in `reference/c.md`; the C++ units are the ten complete
fences in `reference/cpp.md`; the four Qt fences are statement or
member-function fragments spliced verbatim into the committed adapter
templates at marked positions. Editing a guide in a way that changes the
fence count or the marked bodies makes the runner fail loudly rather than
silently checking different bytes.

## What is exercised

- C, three compiler variants (address/undefined sanitiser, `-O2`, thread
  sanitiser): the bounded-copy contract (exact fit, truncation, empty,
  zero capacity), whole-file reading (small, grown past the initial
  capacity, empty, missing, and a directory whose read fails, with buffer
  cleanup asserted on every failure path), the one-past-the-end sum loop,
  and the C11 atomic stop flag read by worker threads under the thread
  sanitiser.
- C++, five variants (sanitiser and `-O2` on C++20 and C++17, thread
  sanitiser on C++20): `unique_ptr` ownership on success and failed init,
  the `fclose` wrapper (open and failed open), view and lambda lifetimes
  against caller-owned data, rule-of-zero copying, the move contract of
  the corrected Socket (moved-from closes nothing, exactly one close,
  move-assignment releases the old handle, copies are rejected),
  `std::stoi` failure mapping, an eight-thread atomic counter, a guarded
  vector under eight threads, and `build`'s negative-count rejection
  (`std::invalid_argument`, not `std::length_error`).
- Qt 6.12.0 event-loop adapters (offscreen where widgets are needed):
  parent destruction deleting the child, `deleteLater` behaviour after the
  loop stops, `qobject_cast` and `QPointer` contracts, the context-object
  lambda disconnection, the guarded-setter signal loop, and the full
  worker-object shutdown (started → quit → finished → both objects
  deleted, bounded waits).
- Fixtures: each known-defect variant fails its recorded expectation and
  each clean control passes, for partial-I/O handling (C), defaulted-move
  double close (C++), and lambda connections surviving owner destruction
  (Qt). These are sensitivity checks for review fixtures, not model
  detection results.

## Evidence discipline

Routine extraction and running write fresh outputs only under ignored
`.generated/results/`. Recorded `results/` and the candidate manifest are
refreshed only by running with `--record`, which is a deliberate evidence
step. `test_evidence_integrity.py` re-runs both scripts in an isolated
checkout with a local guide edit and checks every recorded byte, so a
future regression cannot silently replace recorded evidence.

## Evaluation boundary

The [fixtures](fixtures/) are prepared for a separately agreed review
exercise. Sensitivity checks prove that the assertions distinguish these
defect and clean variants; they do not measure model detection, false
positives, severity calibration, or evidence quality. Do not provide the
harness, answer key, audit narrative, or result logs to a future reviewer
whose answers are meant to be independent.

Widget behaviour beyond the offscreen parent-child lifecycle, embedded
targets, other compilers and standard-library implementations, and other Qt
build configurations are outside the recorded checks; see the
[audit evidence](../11-c-cpp-and-qt.md) for the full limit list.
