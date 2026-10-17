# Package 03: Python and reference quality

Status: complete; the user approved the scoped audit on 18 October 2026.
See the [reference disposition](../reference/reference-status.md) and
[verification and decision record](evidence/03-python-and-reference-quality.md).

## Outcome

Provide technically sound Python review guidance and a deliberate maintenance
scope for the remaining inherited references.

## Deliverables and responsibilities

- Audit `reference/python.md` against supported Python versions and official
  documentation. Rewrite the Python guide in concise British English; do not
  merely translate incorrect or irrelevant examples.
- Prioritise resource cleanup, exceptions and cancellation, mutable state,
  iterator behaviour, filesystem/subprocess safety, and concurrency correctness.
- Review modern annotation examples against the target project's Python version.
  Do not mandate a particular checker, docstring style, or annotation syntax
  where the project has already chosen a supported convention.
- Treat performance claims as hypotheses needing a workload or demonstrated
  complexity problem; avoid recommending async, caching, or parallelism by reflex.
- Replace arbitrary coverage recommendations with meaningful behavioural tests
  and the target project's recorded requirements.
- Cross-check common-bug, security, architecture, performance, and
  `reference/code-review-best-practices.md` guidance for conflicts with the core
  contract. Remove prescribed review-time budgets and automatic requests to split
  large PRs wherever they remain in retained guides. Consolidate duplicates or
  retire routing only after checking their callers and intended role.
- Classify other language guides as verified, retained but not yet verified, or
  needing correction. Retain their scope honestly; do not imply a complete
  multilingual technical audit has happened.
- Keep reusable examples general. Use a separate synthetic consumer fixture to
  demonstrate that target-project invariants are discovered from its instructions.

## Tests and verification

Run self-contained Python examples where meaningful, using an isolated temporary
directory. Check known failure examples fail for the stated reason. Verify
version-sensitive claims using official docs and record sources. Validate links
and routing after moving or consolidating any guidance.

## Human checkpoint

Review the rewritten Python guide and the audit disposition of other references.
Confirm the supported scope and any deferred translations or technical checks.

## Exit criteria

- Python guidance is readable, technically checked, and version-aware.
- No blanket style preference is represented as a correctness defect.
- Retained references have a recorded review status and working links.
- Retained process guidance agrees with the core contract and updated templates.
- Project-specific approval and safety rules are consulted, not embedded globally.
