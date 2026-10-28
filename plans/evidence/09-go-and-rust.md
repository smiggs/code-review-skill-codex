# Package 09: Go and Rust audit evidence

Date: 28 October 2026. Technical audit candidate prepared at the user's request;
the user supplied [conditional acceptance](09-pr-approval.md) on 28 October
2026, effective after the current-head CodeRabbit and merge gates hold.
The [plan](../09-go-and-rust.md) governs scope
and the human checkpoint. This work does not reopen package 05, authorise
publication, or establish review accuracy for the changed guides.

## Candidate and changes

Work began on `957988a23e59285ef71fa8a298734093a5a914d6`. The PR branch is based
on main at `128b6a908bdeefd5a6d1a73b2fce91c5139294f6`, which merges that source
head with the same file tree; this PR base is recorded in the candidate manifest. The working candidate is identified
by the [manifest](09-executable-checks/results/candidate-manifest.json), which
covers the guides, checklist, disposition, provenance, plan, harness, fixtures,
and result records. It excludes this narrative and the manifest itself to avoid
self-reference, along with generated sources, caches, and toolchains. Human
acceptance must name the manifest's combined digest or an exact committed
revision; the user's conditional decision is recorded in the approval record.

`reference/go.md` and `reference/rust.md` were rewritten in British English
using the Google documentation variant of the house style.
Their existing paths, core selective routing, skill identity, and MIT attribution
remain. Only the Rust section of the common-bug checklist was replaced, and Go
routing was added; other language sections retain their existing content.
Reference disposition and provenance now describe this scoped candidate.

| Area | Correction and resulting contract |
| --- | --- |
| Go worker pool | The inherited pool accepted non-positive workers on empty input and hung on non-empty input; its context had no effect. The replacement validates positive counts before cancellation, bounds callbacks and queue storage, propagates causes, closes its own channel, and joins workers. Cooperative callbacks and stable input are explicit preconditions; no rollback or strict cancellation cut-off is promised. |
| Go ownership | Closure coordination replaces an absolute sender-closes rule. Nil and closed channel behaviour, wait-group registration, context ownership, typed nil interfaces, and shared slice storage have concrete triggers. |
| Go versions and preferences | Module 1.21/1.22 comparisons distinguish declared loop variables from assignment to existing variables. Error wrapping becomes an API decision. Interface, receiver, allocation, formatting, mocking, and test preferences no longer automatically establish defects. |
| Rust unsafe | Removed the unsound safe wrapper whose bounds proof disappeared in release builds, and the uncompilable generic transmute recipe. The retained safe operation and explicitly unsafe API distinguish enforced bounds from caller obligations. Foreign-code invariants require the foreign contract. |
| Rust cancellation | Corrected the contradiction about Tokio `read`; distinguished it from `read_exact` and multi-step framing. Replaced invented transaction and buffered-parser guarantees with explicit progress ownership and a checked resumable four-byte reader. |
| Rust tasks | Dropping a handle detaches work; abort requests cancellation, and joining observes termination. Started blocking work survives abort. Direct futures, nested task results, supervisor cancellation, and previous side effects have separate ownership contracts. |
| Rust clean controls | Borrowed fields, necessary clones, short standard mutex critical sections, and a literal parse invariant can be valid. Removed blanket production unwrap/expect bans, mandated error crates, universal trait rankings, and the false claim that String addition necessarily reallocates each time. |

## Sources and version boundaries

Primary sources were accessed on 28 October 2026. Versioned package pages and
locked crate source are preferred where available. Go's web specification and
Rust's standard-library/reference/book pages are rolling documents; they do not
by themselves prove old-version compatibility. The Go archive's specification
and the exact examples supplement them. Rust's rolling standard-library pages
reported 1.99.1 when accessed; the retained code was compiled with 1.85.0.
No claim is made for every release between them.

| Claims checked | Primary sources |
| --- | --- |
| Go wrapping and cause exposure | [Go 1.13 errors](https://go.dev/blog/go1.13-errors). |
| Go nil interfaces, channel and slice semantics | [FAQ](https://go.dev/doc/faq#nil_error), [specification](https://go.dev/ref/spec), and [slice storage](https://go.dev/blog/slices-intro); Go 1.22.12 archive specification inspected locally. |
| Go loop semantics | [Go 1.22 transition](https://go.dev/blog/loopvar-preview) and [module language directive](https://go.dev/ref/mod#go-mod-file-go), with executable 1.21/1.22 comparisons under compiler 1.22.12. |
| Go cancellation and synchronisation | [context at go1.22.12](https://pkg.go.dev/context@go1.22.12), [sync at go1.22.12](https://pkg.go.dev/sync@go1.22.12), and [race-detector limits](https://go.dev/doc/articles/race_detector). |
| Go library and conventions | [standard library](https://pkg.go.dev/std@go1.22.12), [time at go1.22.12](https://pkg.go.dev/time@go1.22.12), and [review comments](https://go.dev/wiki/CodeReviewComments). The JSON and strings versioned pages were unavailable through the web reader; encoding/json/encode.go and strings/clone.go in the 1.22.12 archive supplied those checks. |
| Rust validity and unsafe operations | [undefined behaviour](https://doc.rust-lang.org/reference/behavior-considered-undefined.html), [slice bounds](https://doc.rust-lang.org/std/primitive.slice.html#method.get_unchecked), [transmute](https://doc.rust-lang.org/std/mem/fn.transmute.html), and [2024 unsafe-block lint](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-op-in-unsafe-fn.html). An inherited invalid bounds call was later checked only in Miri, as recorded below. |
| Rust ownership and errors | [lifetimes](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html), [Option panic contract](https://doc.rust-lang.org/std/option/enum.Option.html#method.expect), and [anyhow 1.0.100 downcasting](https://docs.rs/anyhow/1.0.100/anyhow/struct.Error.html). Anyhow was documentation-only; it is not a harness dependency. |
| Tokio 1.48.0 I/O | [published AsyncReadExt source](https://docs.rs/tokio/1.48.0/src/tokio/io/util/async_read_ext.rs.html); the rendered trait page was unavailable, so the matching locked crate source was inspected and hashed. |
| Tokio 1.48.0 lifetime and scheduling | [JoinHandle](https://docs.rs/tokio/1.48.0/tokio/task/struct.JoinHandle.html), [spawn_blocking](https://docs.rs/tokio/1.48.0/tokio/task/fn.spawn_blocking.html), [try_join](https://docs.rs/tokio/1.48.0/tokio/macro.try_join.html), and [mutex choices](https://docs.rs/tokio/1.48.0/tokio/sync/struct.Mutex.html). |
| Rust async traits and String addition | [Rust 1.75 stabilisation and limitations](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/) and [String API/source](https://doc.rust-lang.org/std/string/struct.String.html). A capacity-preserving addition is also a runtime clean control, not a performance benchmark. |

## Executable verification

The [harness](09-executable-checks/README.md) records portable commands, exact
extraction, captured results, fixture contracts, and dependency locks. Baselines:
Linux/x86_64; Go 1.22.12; Rust and Cargo 1.85.0; Tokio 1.48.0; GCC 12.5.0;
Python and PyYAML versions appear in the validation log. Rust 2021 and 2024 use
the same lockfile. The minimum supported Rust version is a target-project
requirement, not inferred from this audit baseline. Native async traits' 1.75
boundary is documentation-only; no 1.75 compiler was run.

Go's inherited algorithm was adapted only to make its callback types concrete.
The first boundary test failed on an accepted invalid worker count before the
replacement was extracted. Final fixture tests additionally reproduce non-empty
input and cancellation hangs with bounded waits. For Rust, a synthetic variant
that resets persistent progress failed the partial-frame assertion before the
clean extracted implementation passed it. That is sensitivity evidence, not a
claim that the synthetic variant was the original inherited source.

| Check | Observed result |
| --- | --- |
| Exact Go example, initial contract tests | Four tests passed; [initial output](09-executable-checks/results/go-green.txt). |
| Go final suite with `-race`, 20-second process bound | Nine top-level tests passed, including two non-positive-count subtests; no reported races. Covers boundaries, errors, parent cancellation/deadline, worker bound, joined callbacks, closure, typed nil, wrapped causes, and shallow storage behaviour. [Output](09-executable-checks/results/go-race.txt). |
| Go loop comparison | Declared captures return `[3 3 3]` under module 1.21 and `[1 2 3]` under module 1.22; existing-variable assignment returns `[3 3 3]` in both. [1.21](09-executable-checks/results/loop-1.21.txt) and [1.22](09-executable-checks/results/loop-1.22.txt). |
| Rust 2021 debug and release | Ten tests passed in each, zero ignored; [debug](09-executable-checks/results/rust-final.txt) and [release](09-executable-checks/results/rust-release.txt). |
| Rust 2024 debug | Ten tests passed, zero ignored; [output](09-executable-checks/results/rust-edition-2024.txt). |
| Fixture sensitivity | Both defective heads rejected for runtime assertion failures; both clean bases passed. No compiler failure counts as detection. [Final summary](09-executable-checks/results/sensitivity-final.txt), [Go head](09-executable-checks/results/fixture-go-head.txt), and [Rust head](09-executable-checks/results/fixture-rust-head.txt). |
| Miri | Initially absent from stable; subsequently installed at the user's request. All ten Rust harness tests passed on nightly-2025-02-20, edition 2021, one seed/target. The inherited debug-only bounds wrapper was rejected for undefined behaviour with debug assertions disabled. See the [Miri record](09-executable-checks/miri-verification.md). No sanitiser run is claimed. |

Rust checks cover a pending single read losing a select, partial `read_exact`
consumption and restart, resuming the same pinned future, frame EOF, retained
frame progress, borrowed data, in-bounds unsafe access, deliberate panic/join
failure, detached work, destructors after abort-and-join, and started blocking
work that cannot be aborted. Controlled readers and explicit gates avoid network
timing as evidence. There is no real socket, FFI, database transaction, CPU
benchmark, broad feature/target matrix, or complete unsafe-code proof.

Toolchains were absent from PATH. Approved network execution fetched pinned
public archives and locked crates into `/tmp`; GCC packages were extracted
without system installation. Initial full Rust extraction plus a duplicate
installation exceeded the temporary disk quota. Removing only this task's
partial installation and extracting required components resolved it. The first
Go command ran outside its module; the first Rust build used a wrong relative
test path. Both setup errors were corrected before successful checks. Neither
is counted as a passing or failing behavioural assertion. The initial technical verification used no private code, model-review run,
external comment, commit, PR, repository setting change, skill installation, or
publication. The subsequent [PR authorisation](09-pr-approval.md) supplies the
separate review-loop and merge authority.

## Evidence-preservation correction before PR review

A regression reproduced routine extraction and verification replacing six
recorded evidence files, including source identities. The
[red output](09-executable-checks/results/evidence-integrity-red.txt.gz) preserves
that failure losslessly. Both scripts now write fresh output only under ignored
`.generated/results/`. The regression runs both in an isolated checkout with a
local prose edit, then checks every recorded result and the candidate manifest
byte for byte. The [green output](09-executable-checks/results/evidence-integrity-green.txt)
records the passing regression. This changes evidence storage only; the retained
Go/Rust examples, original result bytes, and Miri conclusions are unchanged.

## Documentation checks and human decision

The [final validation log](09-executable-checks/results/validation.txt) records
18 passing repository helper/validator tests, 13 passing package 03
examples, passing structural and system skill validation, house-style lint
with zero errors and one proper-name title warning, whitespace,
and diff statistics. These establish mechanical consistency within their scope;
they do not establish useful review behaviour. Candidate hashes include new files
that ordinary unstaged `git diff --stat` omits.

Human decision: [conditional acceptance supplied](09-pr-approval.md). Review the corrections, declared versions, retained
scope, English-only translation limit, and the scoped unsafe-tool checks against
the manifest digest or an exact committed revision. The user authorised acceptance of the reviewed candidate once the CodeRabbit
and merge gates hold; final evidence will be recorded in the PR conversation.

The Chinese installation and contribution documents need no shared-behaviour
change: this work changes reference guidance only. The rewritten guides and
evidence are English only, with no bilingual technical validation. Any model
review evaluation requires separately agreed prompts, withheld answer keys,
criteria, and raw reports. No package 09 accuracy claim or release is authorised.
