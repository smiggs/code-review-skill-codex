# Package 09 Miri verification

On 28 October 2026, after the initial audit recorded Miri as unavailable, the
user asked whether it could be installed. An isolated installation succeeded.
This record supersedes that tooling limitation. The subsequent conditional
human acceptance remains subject to the PR review and merge gates.

## Installation and version

Miri 0.1.0 (`f280acf4c7`, 19 February 2025) is installed with
`nightly-2025-02-20-x86_64-unknown-linux-gnu`, Rust 1.87.0-nightly. The dated
nightly keeps this supplemental check close to the audit's stable 1.85.0
baseline. It is not a claim about the latest Miri release. See the
[exact versions and installer checksum](results/miri-versions.json).

The official rustup installer was downloaded and its SHA-256 checked against
the published checksum. `RUSTUP_HOME` is `/tmp/package-09-rustup`; `CARGO_HOME`
is `/tmp/package-09-cargo`. Installation used `--no-modify-path`, with no shell
configuration or system installation change. Rustup's default applies only to
this isolated root. The stable compiler checks still use their original
standalone Rust 1.85.0 toolchain. These temporary directories can be removed
by the host; this is not a persistent user-level installation.

The [official Miri instructions](https://github.com/rust-lang/miri#using-miri)
require a nightly toolchain. The
[rustup installation documentation](https://rust-lang.github.io/rustup/installation/other.html)
describes the manual installer and path-preserving option. Both were accessed
on 28 October 2026. The [installation log](results/miri-toolchain-install.txt)
and [sysroot setup](results/miri-setup.txt) record successful completion.

The first sysroot build could not find `cc`; Miri's sysroot build did not use the
previous command's linker flag. A task-local `cc` wrapper now invokes the already
extracted GCC 12.5.0 driver, and is placed on PATH for setup and tests. The
[initial failure](results/miri-setup-initial.txt) is retained. A separate rustup
version query hit a sandbox signal-handling error; direct installed binaries
supplied the versions. Neither setup diagnostic is a behavioural result.

## Checks and limits

All ten existing Rust harness tests passed under Miri, with zero failures and
zero ignored tests. The run used the unchanged guide code, Tokio 1.48.0 from the
existing lockfile, edition 2021, Linux/x86_64, and `-Zmiri-seed=0`. The
[full output](results/miri-tests.txt) includes the unsafe in-bounds call, safe
out-of-bounds controls, borrowing, panic invariant, partial I/O, and task lifecycle
checks. No Miri diagnostic was reported for those executions. Normal compiler
checks on editions 2021 and 2024 remain separately recorded in the main audit.

A separate [negative probe](miri-probes/inherited-bounds.rs) preserves the
inherited safe wrapper from base revision
`957988a23e59285ef71fa8a298734093a5a914d6`, with a main function that passes an
out-of-bounds index. With debug assertions disabled, Miri exited 1 and reported
undefined behaviour inside `get_unchecked`. The
[diagnostic](results/miri-negative.txt) confirms the stated release-build defect.
The invalid operation ran only in the interpreter; the negative probe was not
built and run as a native executable. This probe is development evidence, not
an additional independently scored review fixture.

One Miri seed, one nightly, and one target do not prove that arbitrary safe
callers can never violate an unsafe invariant. No broad schedule, aliasing-model,
platform, or feature matrix is claimed, and no sanitiser was run. This work does
not change package 09's human checkpoint or establish model review accuracy.
The initial [missing-command log](results/miri.txt) remains historical evidence.

## Reproduction

With the recorded temporary installation present, use the isolated rustup
proxies, the `cc` wrapper, and the sysroot:

```bash
export RUSTUP_HOME=/tmp/package-09-rustup
export CARGO_HOME=/tmp/package-09-cargo
export MIRI_SYSROOT=/tmp/package-09-miri-sysroot
export CARGO_TARGET_DIR=/tmp/package-09-miri-target
export PATH=/tmp/package-09-miri-bootstrap:/tmp/package-09-cargo/bin:$PATH
cargo +nightly-2025-02-20 miri setup
MIRIFLAGS=-Zmiri-seed=0 timeout 180s cargo +nightly-2025-02-20 miri test --manifest-path plans/evidence/09-executable-checks/rust/Cargo.toml --locked --offline
/tmp/package-09-rustup/toolchains/nightly-2025-02-20-x86_64-unknown-linux-gnu/bin/miri --sysroot "$MIRI_SYSROOT" -C debug-assertions=no plans/evidence/09-executable-checks/miri-probes/inherited-bounds.rs
```

The last command is expected to fail with an undefined-behaviour diagnostic.
If recreating the temporary installation, first use the official rustup installer
with the stated isolated roots, then install `nightly-2025-02-20` with the
`minimal` profile and components `miri` and `rust-src`. The `cc` wrapper contains
`exec /tmp/package-09-toolchains/cc/usr/bin/gcc-12 "$@"` after its shell shebang;
use a working system C compiler instead when available.
