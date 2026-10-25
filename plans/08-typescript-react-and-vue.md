# Package 08: TypeScript, React, and Vue

Status: planned; implementation and technical verification have not begun.

## Outcome

Provide version-aware review guidance for JavaScript and TypeScript behaviour,
React components, and Vue reactivity.

Apply the [package 03 approach](03-python-and-reference-quality.md) to [typescript.md](../reference/typescript.md), [react.md](../reference/react.md), [vue.md](../reference/vue.md).
Follow the [shared audit requirements](README.md#language-audit-requirements).

## Deliverables and responsibilities

- Separate compile-time types from runtime validation, including assertions,
  narrowing, indexed access, and untrusted data. Respect project compiler and
  lint settings rather than mandating strictness as a correctness requirement.
- Trace promise rejection, cancellation, stale responses, and request ownership.
  Recheck the TypeScript abort example and Vue's overlapping fetch example.
- Audit React effects, hook rules and exceptions, component identity, actions,
  server/client boundaries, and cleanup. Distinguish React behaviour from
  Next.js and TanStack Query APIs and record each dependency's version.
- Audit Vue reactive inputs, props destructuring, watchers, composables, and
  lifecycle cleanup against the target compiler and runtime versions.
- Require workload evidence for memoisation, virtual lists, or other performance
  recommendations. Keep valid alternative component designs as clean controls.
- Rewrite scoped guidance in concise British English, preserve existing paths
  and attribution, and reconcile corresponding common-bug checklist sections.
- Update the reference disposition with verified scope and remaining limits.
  Record corrections, sources, checks, and upstream divergence in a package
  evidence record when implementation produces evidence.

## Tests and verification

Exercise out-of-order request completion, rejection, disposal, and reactive
input changes using controlled promises and the relevant framework test tools.
Compile retained type examples under declared settings. Include valid hook and
reactivity patterns that must not become findings. Record browser or DOM test
environment limits separately from compiler results.

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
