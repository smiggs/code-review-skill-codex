# Human and AI checkpoints

AI prepares implementation and evidence. Human judgement settles review quality,
supported scope, and publication decisions. These checkpoints do not require
approval for every routine edit or repeat checks already accepted unchanged.

## Decision record

Record checkpoint, package, source revision or working-diff hash, evidence paths,
AI recommendation, human decision and reason, and any follow-up work. Include
decision date and reviewer identity as supplied; never invent a human approval.
Changes affecting the decision require the relevant evidence to be refreshed.

## Checkpoints

| Stage | AI prepares | Human judges |
|---|---|---|
| Review contract | Example findings, severity mapping, scope and authority | Whether findings are actionable and approval boundaries are clear |
| Core workflow | Concise entry point and sample reports | Clarity, useful detail, and acceptable no-findings output |
| Reference quality | Python rewrite and audit disposition; scoped language audits in packages 08–12 | Technical scope, supported versions, deferred work, and translation expectations for each audited revision |
| Helper tooling | Tested behaviour and heuristic limitations | Whether the helper is useful enough to retain |
| Evaluation | Raw reports, answer keys, scored outcomes | Disputed findings and a pass, fail, or unresolved decision against pre-agreed acceptance criteria |
| Severity calibration follow-up | Assessment of priority boundaries, proposed correction or no change, and bounded diagnostic evidence | Impact interpretation and criteria before evaluation; final disposition for the exact candidate, with limitations retained |
| Distribution | Installable candidate, validation and limitations | Readiness of the exact candidate and any publication request |

## Operating boundaries

- A favourable review recommendation is not GitHub approval or permission to merge.
- Target-project approval gates remain authoritative for that project's actions.
- Do not post evaluation results to live PRs or change repository settings as
  part of an offline evaluation.
- If a checkpoint is pending, continue independent authorised work and report
  exactly which dependent decision remains open.
- A failed or unresolved evaluation alone keeps package 05 open and blocks
  package 06. A human may explicitly approve a named exception to package exit
  criteria for an exact evaluated revision. Record that change and its limits
  separately; preserve original scores and do not relabel the run as passing.
  The [package 05 completion decision](evidence/05-completion-and-exceptions.md)
  records the approved severity and incomplete-comparison exceptions.
