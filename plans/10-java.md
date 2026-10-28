# Package 10: Java

Status: technical audit candidate prepared; the user conditionally accepted
it on 28 October 2026, subject to the
[CodeRabbit and merge gates](evidence/10-pr-approval.md). See the
[audit evidence](evidence/10-java.md) for the checked scope, commands,
candidate identity, and the separately prepared evaluation boundary.
Behavioural evaluation acceptance remains a separate decision.

## Outcome

Provide Java review guidance grounded in supported JDK versions and the
actual Spring, persistence, and concurrency contracts.

Apply the [package 03 approach](03-python-and-reference-quality.md) to [java.md](../reference/java.md).
Follow the [shared audit requirements](README.md#language-audit-requirements).

## Deliverables and responsibilities

- Verify records, switch patterns, text blocks, and virtual threads against
  release and preview-feature boundaries. Recheck the Java 16 switch claim.
- Trace resource closure, exception propagation, interruption, executor
  ownership, and shared mutable state. Separate thread safety of a collection
  from atomicity of compound operations performed by callers.
- Check Spring transaction advice against proxy mode, invocation path, method
  visibility, and framework version. Treat read-only hints and layering choices
  according to their actual contracts rather than universal rules.
- Check JPA fetch examples for query count, result membership, pagination,
  transaction lifetime, and entity equality. Verify that proposed replacements
  preserve users with no related records where required.
- Remove automatic preferences for records, Optional usage, dependency injection
  style, Lombok, test frameworks, and virtual threads as defect evidence.
- Rewrite scoped guidance in concise British English, preserve existing paths
  and attribution, and reconcile corresponding common-bug checklist sections.
- Update the reference disposition with verified scope and remaining limits.
  Record corrections, sources, checks, and upstream divergence in a package
  evidence record when implementation produces evidence.

## Tests and verification

Compile retained standalone examples on declared JDK targets, distinguishing
preview flags from permanent language features. Exercise closure after failure,
interruption, and task completion. Use isolated framework or database fixtures
only for retained claims that need them; record dependency versions and query
results. Include valid conventional classes and thread pools as clean controls.

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
