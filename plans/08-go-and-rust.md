# Package 08: Go and Rust

Status: planned; implementation and technical verification have not begun.

## Outcome

Provide checked guidance for resource ownership, errors, cancellation, and
concurrency in Go and Rust.

Apply the [package 03 approach](03-python-and-reference-quality.md) to [go.md](../reference/go.md), [rust.md](../reference/rust.md).
Follow the [shared audit requirements](README.md#language-audit-requirements).

## Deliverables and responsibilities

- Audit Go channel ownership, goroutine termination, context propagation,
  worker bounds, error wrapping, typed nil values, and shared slice storage.
- Investigate zero or negative worker counts and the unused context in the
  inherited worker pool. Specify input and cancellation contracts before fixes.
- Verify Go loop-variable semantics against language/module versions, and
  qualify interface, allocation, formatting, and testing preferences.
- Audit Rust ownership, unsafe invariants, lifetimes, panic paths, and task
  ownership. Respect the project's minimum supported Rust version and edition.
- Correct the contradictory Tokio read cancellation examples after checking
  the chosen Tokio version. Distinguish cancellation of a future from stopping
  spawned or blocking work; verify any claimed transaction guarantees.
- Replace blanket bans on unwrap/expect and universal allocation advice with
  concrete failure conditions and measured consequences.
- Rewrite scoped guidance in concise British English, preserve existing paths
  and attribution, and reconcile corresponding common-bug checklist sections.
- Update the reference disposition with verified scope and remaining limits.
  Record corrections, sources, checks, and upstream divergence in a package
  evidence record when implementation produces evidence.

## Tests and verification

Exercise worker input boundaries, cancellation, channel closure, and task
shutdown with bounded waits. Compile Rust examples and test partial I/O and
cancellation using controlled readers. Use race detection or unsafe-code tools
where supported and relevant, recording their limits. Include intentional
panic invariants and valid ownership patterns as clean controls.

Run the shared documentation and structural checks. Record commands, versions,
results, and unavailable checks; do not equate example tests with review accuracy.
Prepare known-defect fixtures and clean controls for a separate, agreed
[behavioural evaluation](05-behavioural-evaluation.md).

## Human checkpoint

Review the technical corrections, supported versions, retained scope, and
translation limits. Record approval or outstanding work against the exact
revision. Behavioural evaluation acceptance remains a separate decision.

## Exit criteria

- Scoped guidance is concise, version-aware, and consistent with the contract.
- Retained technical claims have primary-source support and meaningful examples
  have recorded checks or explicitly accepted validation limits.
- No tool preference, style rule, or performance pattern alone becomes a defect.
- Guide routing and related checklist advice agree; relative links work.
- The evidence record states corrections, deferred work, and the human decision.
- Any claim of evaluated review accuracy cites a separate accepted evaluation;
  this technical audit does not itself complete package 05 or authorise release.
