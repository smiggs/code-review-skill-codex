# Code review skill adaptation plans

These plans turn the upstream skill into a reusable ChatGPT/Codex review tool
with concise instructions, evidence-backed findings, and tested helper behaviour.
They follow the bounded work-package format used in photo-workflow: outcome,
deliverables, verification, human judgement, and exit criteria.

The scope is adaptation of this skill, not implementation of the photo pipeline.
No package below is complete merely because this plan exists.

Package 01 is complete: the user approved the
[review contract](../reference/review-contract.md) on 18 October 2026. The
[checkpoint evidence](evidence/01-foundation-and-review-contract.md) records the
decision. Package 02 implements the entry point and templates on
`codex/package-02-core-workflow`; its
[verification and decision record](evidence/02-core-workflow-and-routing.md)
awaits the core-workflow human checkpoint. Inherited guide audits remain in
package 03.

## Work packages

1. [Foundation and review contract](01-foundation-and-review-contract.md):
   upstream baseline, scope, findings, severity, and authority boundaries.
2. [Core workflow and reference routing](02-core-workflow-and-routing.md):
   concise entry point, tool portability, and review templates.
3. [Python and reference quality](03-python-and-reference-quality.md):
   technical audit, British-English Python guidance, and remaining guide scope.
4. [Helper tooling and validation](04-helper-tooling-and-validation.md):
   correct diff handling, honest heuristics, and automated structural checks.
5. [Behavioural evaluation](05-behavioural-evaluation.md):
   defect fixtures, clean controls, reproducible results, and false positives.
6. [Documentation and distribution](06-documentation-and-distribution.md):
   installation verification, attribution, companion docs, and release evidence.

[Human and AI checkpoints](human-ai-checkpoints.md) records the judgements that
automated checks cannot establish.

## Delivery order

Agree the contract in package 01 before changing the core workflow. Packages
02 and 03 can then progress independently. Package 04 supplies mechanical
checks; package 05 evaluates the resulting behaviour. Package 06 follows only
after the agreed checks and evaluation criteria are met and the package 05
human checkpoint records a pass for the evaluated revision. A finished evaluation
run with failed or unresolved criteria is evidence of outstanding work, not
completion of package 05.

## Cross-cutting rules

- Preserve the `code-review-codex` name and existing `reference/` paths unless
  a recorded migration justifies changing them.
- Keep the core skill general; read project requirements from each target.
- Preserve upstream attribution and MIT licence notices.
- Separate review findings from fixes and external review submission.
- Load relevant references rather than every language guide.
- Distinguish structural validity, helper correctness, and review accuracy.
- Keep evaluation fixtures synthetic or explicitly distributable.
- Record exact source revisions, model/tool versions where exposed, prompts,
  commands, results, and limitations; do not invent unavailable metadata.

## Completion records

When work begins, record package status and evidence under `plans/evidence/`
using a separate Markdown record per completed package or evaluation run.
Create that directory only when evidence exists. Include source commit or
working-diff hash, affected files, checks, results, human decisions where needed,
and outstanding work. Changes to evaluated material invalidate the relevant
completion claim until proportionate checks are repeated.
