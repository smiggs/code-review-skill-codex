# Task 07: severity calibration

Status: scoped on 25 October 2026; implementation and evaluation have not begun.
The user requested a separate severity-calibration follow-up, retaining package
06 and moving the pending language audits to packages 08–12.

## Outcome

Determine whether the observed priority disagreement warrants a general
guidance correction, clarification of impact evidence, or continued human
judgement. Produce a bounded diagnostic and an accepted disposition, including
no change when the evidence does not justify a runtime correction.

Package 05 remains complete under its [accepted exceptions](evidence/05-completion-and-exceptions.md).
This task is optional and does not block package 06 or the language audits.
It does not promise deterministic priority labels or remove human review.

## Starting evidence

Use the [approved contract](../reference/review-contract.md),
[batch 01 adjudication](evidence/05-behavioural-evaluation/runs/batch-01/adjudication.md), and
[batch 02 severity brief](evidence/05-behavioural-evaluation/batch-02/execution/adjudication.md).
Batch 02's adapted report assigned P0 to a required readiness gate where the
agreed rubric required P1. Detection and causal evidence were correct.
The accepted runtime was `677beab3a37af42b08f9c46e5344b44afe84b3cf`.

Retain both batches and their original scores. Their fixtures and reports are
diagnostic background, not fresh evidence of a correction. Do not rerun them
to select a preferred label or retrospectively alter their acceptance criteria.

## Scope and deliverables

- Audit priority wording in `SKILL.md`, `reference/review-contract.md`, and
  relevant report templates for consistency. Distinguish impact, urgency,
  breadth, and conditional triggers from confidence or whether a defect blocks
  a release. Keep any correction general rather than specific to readiness gates.
- Document whether the P0/P1 boundary is ambiguous in the guidance, the fixture,
  or its interpretation. Obtain human agreement on that interpretation before
  selecting a correction or diagnostic rubric.
- Prepare six original, distributable synthetic cases: four evidenced defects
  spanning P0–P3 and two clean controls. Supply the operational consequences
  needed to judge impact and urgency. Keep expected labels out of target inputs.
- Before model review, agree acceptable labels and rationale for each case,
  detection/evidence and false-positive criteria, evaluator setup, exact model
  and reasoning settings, runtime revisions, and permitted limits. Resolve
  fixture ambiguity before freezing inputs; do not choose tolerances from outputs.
- Make a narrow runtime correction only when the audit and human decision
  support it. No change is a valid outcome. Record the candidate's exact runtime
  revision or per-file content hashes before evaluation.
- Propose at most six adapted-skill reviews, one per case, in fresh standalone
  contexts. Reuse the documented isolation method after checking the actual
  available runtime; inspect initial context before supplying a case. Do not
  inherit repository instructions, keys, earlier reports, or parent conclusions.
- Retain every prompt, context audit, exposed version/setting, command/output,
  report, error, and before/after input hash. Freeze raw outputs before scoring.
  Score priorities separately from detection, evidence, scope, and authority.
- Record the cause assessment, source changes or no-change rationale, scores,
  false positives, misses, and remaining limits in a task evidence record when
  work produces them. Keep original batch scores and the package 05 acceptance
  decision intact.

## Boundaries and stopping rule

This plan authorises scoping only. Agree the six-review diagnostic and its
immutable inputs before dispatch. No automatic repeats, replacement reports,
correction batch, or upstream comparison are included. Failed or incomplete
reviews remain recorded; further reviews need separate agreement.

Do not fill the missing upstream slot from batch 02, rerun the 20-review
comparison, rewrite language guides, redesign helper tooling, or change
installation, publishing, or repository settings within this task. Do not add
rules that name these fixtures or force one label for every deployment gate.

The diagnostic is a small sample. It can expose an additional disagreement;
it cannot establish reliability across projects or prove that a correction
caused improvement. An unchanged candidate is not retried merely to obtain a
pass. Stop at the agreed bound and present the supported disposition.

## Verification and human checkpoints

Before evaluation, a human reviews the impact premises, priority interpretation,
rubric, proposed correction if any, and bounded run scope. Use synthetic premise
checks and clean controls where execution can establish those premises. Use
the installed TDD skill for any behavioural code introduced during execution.

Run documentation/link checks, `git diff --check`, `git diff --stat`, repository
structural validation, and the system skill-creator validator when available.
Apply meaningful affected checks if runtime guidance or fixture tooling changes.
Structural validity and green fixture tests do not establish priority accuracy.

After scoring, a human accepts the diagnostic conclusion and exact assessed
candidate, including any retained limitation. A failed severity criterion stays
failed even when the task closes with an accepted no-change disposition.

## Exit criteria

- The assessment of priority boundaries and correction or no-change decision are
  supported by recorded evidence and human judgement.
- Any agreed diagnostic has stopped within its bound, with all attempts retained
  and scored against frozen criteria; errors and disagreements remain visible.
- Guidance changes, if any, are general, consistent, and tied to the assessed
  revision. No claim of perfect or systematic calibration exceeds the sample.
- The human checkpoint accepts the final disposition. Package 05's original
  scores and completion exceptions remain unchanged.
- If package 06 selects a changed runtime from this task, its installation and
  release evidence cover that candidate and disclose its measured limits. This
  task alone does not approve a release or invalidate acceptance of the earlier
  package 05 runtime.
