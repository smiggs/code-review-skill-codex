# Package 11: C, C++, and Qt

Status: technical audit candidate prepared at the user's request. Human
acceptance follows the PR review and merge gates under the user's standing
workflow. See the [audit evidence](evidence/11-c-cpp-and-qt.md) for the
checked scope, commands, corrections, candidate identity, and limits.
Behavioural evaluation remains a separate decision.

## Outcome

Provide checked review prompts for memory safety, resource lifetime, and
threading across C, C++, and Qt.

Apply the [package 03 approach](03-python-and-reference-quality.md) to [c.md](../reference/c.md), [cpp.md](../reference/cpp.md), [qt.md](../reference/qt.md).
Follow the [shared audit requirements](README.md#language-audit-requirements).

## Deliverables and responsibilities

- Establish C and C++ language modes, compiler and library versions, platform
  assumptions, and the relevant Qt version before retaining examples.
- Audit buffer sizes, overlap, nullability, integer conversions and overflow,
  partial I/O, allocation failure, and cleanup. State the input contracts of
  examples labelled safe, including truncation and error handling.
- Audit C++ ownership transfer, move operations, exception safety, view
  lifetimes, and synchronisation. Recheck the defaulted Socket moves and
  negative-size reserve example rather than trusting their recommended labels.
- Audit Qt parent ownership, deferred deletion, thread affinity, connection
  types, lambda captures, and shutdown. Replace blanket rejection of QThread
  subclasses with conditions tied to actual lifetime or threading failures.
- Respect project error and ownership conventions. Treat smart pointers,
  constrained templates, layouts, and allocation changes as conditional advice.
- Keep review commands read-only by default; remove in-place formatting from
  suggested review checks unless a separate edit has been authorised.
- Rewrite scoped guidance in concise British English, preserve existing paths
  and attribution, and reconcile corresponding common-bug checklist sections.
- Update the reference disposition with verified scope and remaining limits.
  Record corrections, sources, checks, and upstream divergence in a package
  evidence record when implementation produces evidence.

## Tests and verification

Compile complete retained examples with declared standards and required
headers. Exercise empty and boundary inputs, failure cleanup, moves, and
shutdown. Use sanitiser diagnostics where applicable; a clean run does not prove
the absence of undefined behaviour. Avoid relying on a particular observed
result from undefined code. Run Qt event-loop fixtures where available and
record GUI/platform limits. Include valid raw ownership and QThread designs
with explicit contracts as clean controls.

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
