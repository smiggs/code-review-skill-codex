# Package 05: behavioural evaluation

## Outcome

Demonstrate that the adapted skill finds concrete defects without flooding
reviews with unsupported suggestions or bypassing target-project instructions.

## Deliverables and responsibilities

- Build small distributable review fixtures with base/head patches, necessary
  surrounding code, target instructions, and a separately maintained answer key.
- Include known Python defects, clean refactors, documentation-only changes,
  uncertainty, missing context, and misleading comments embedded in reviewed code.
- Cover at least one generic filesystem/recovery case and one project-specific
  requirement discovered from the fixture's `AGENTS.md` or specification.
- Include a patch whose important failure sits in unchanged callers, and a case
  where the apparent issue predates the patch, to test scope judgement.
- Agree acceptance criteria before evaluation: critical defects to catch,
  unacceptable false positives, evidence required, and permitted limitations.
  Avoid selecting thresholds after seeing results.
- Compare upstream and adapted skills on the same fixtures with equivalent
  context and tool access. Keep answer keys out of evaluator context.
- Record prompts, fixture hashes, skill revision, model/tool versions when
  exposed, commands actually run, outputs, and scoring rationale.
- Use isolated temporary workspaces. A separate evaluator is useful where
  delegation is available and authorised; otherwise disclose evaluator coupling.
- Correct observed failures narrowly and rerun affected fixtures plus relevant
  clean controls. Limit each evaluation batch to its agreed scope; report
  unresolved failures rather than retry indefinitely.

## Verification

Score defect detection, false positives, correct location/trigger/impact,
severity calibration, no-findings quality, and authority boundaries. Structural
checks and green fixture tests are supporting evidence, not behavioural scores.
Where outputs vary, record that variability rather than selecting the best run.

## Human checkpoint

A human reviews raw reports alongside answer keys, resolves disputed findings,
and decides whether the evidence meets the pre-agreed acceptance criteria.
Record pass, fail, or unresolved against the evaluated revision. Record finished
evaluation runs even when criteria fail or remain unresolved. Such runs alone
do not complete this package or permit package 06 to start. The explicit
human-approved completion exception below provides a separate disposition
for the recorded evaluated revision.

## Original exit criteria

- Evaluation can be repeated from recorded artefacts and instructions.
- Pre-agreed acceptance criteria, including critical-case and false-positive
  criteria, are met and the human checkpoint records a pass. Any outstanding
  limitations were explicitly permitted before evaluation.
- No fixture code, secrets, or private PR data escaped its permitted workspace.
- Evidence demonstrates target instructions are honoured without global coupling.

## Approved completion exception

On 25 October 2026 the user approved completing this package for adapted runtime
`677beab3a37af42b08f9c46e5344b44afe84b3cf` with two accepted limitations:
advisory severity calibration and an incomplete upstream comparison. The
[completion decision](evidence/05-completion-and-exceptions.md) records the
approval, evidence, exact score identities, and downstream disclosure duties.

That human acceptance satisfies the package checkpoint through an explicit
exception to the original completion requirements. Package 05 is complete and
package 06 is unblocked. Original failed and unresolved scores are preserved;
neither batch is relabelled as passing its original rubric. No superiority
claim, further evaluation, runtime correction, or publication is authorised.
For another runtime revision, the original exit criteria still apply unless
a separate human decision changes them.
