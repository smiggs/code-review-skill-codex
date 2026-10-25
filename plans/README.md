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
decision. Package 02's entry point and templates were merged into `main`; its
[decision record](evidence/02-core-workflow-and-routing.md) records the user's
confirmation. Package 03's scoped Python and reference audit was approved on
18 October 2026 and is complete on
`codex/package-03-reference-quality`; its
[evidence](evidence/03-python-and-reference-quality.md) records the human decision.
The [reference status](../reference/reference-status.md)
records the scoped checks and remaining technical deferrals.

Package 04 is complete: the user approved and merged
[PR 3](https://github.com/smiggs/code-review-skill-codex/pull/3) on
18 October 2026. Its
[evidence](evidence/04-helper-tooling-and-validation.md) records the accepted
counts-only helper, input limits, resolved review comments, and passing CI on
merged revision `e5c3a10`. Package 05 is complete with human-accepted limitations
on 25 October 2026 for runtime `677beab3a37af42b08f9c46e5344b44afe84b3cf`.
The [completion decision](evidence/05-completion-and-exceptions.md) records the
explicit change to its original exit requirements: severity calibration remains
advisory and the upstream comparison is incomplete. Original scores, reports,
and failed attempts remain unchanged; neither batch is retroactively passed.
The [batch 02 results](evidence/05-behavioural-evaluation/batch-02/execution/README.md)
record all four defects detected, zero false positives, three of four severity
matches, and successful context isolation under disclosed runtime limits.
Package 06 is unblocked and has not started. No superiority claim or publication
is authorised by this completion decision.

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

7. [Severity calibration](07-severity-calibration.md):
   optional assessment of priority boundaries and a separately agreed diagnostic of
   at most six adapted reviews; no reopening of package 05.
8. [TypeScript, React, and Vue](08-typescript-react-and-vue.md):
   scoped technical audit and verification of retained guidance.
9. [Go and Rust](09-go-and-rust.md):
   scoped technical audit and verification of retained guidance.
10. [Java](10-java.md):
   scoped technical audit and verification of retained guidance.
11. [C, C++, and Qt](11-c-cpp-and-qt.md):
   scoped technical audit and verification of retained guidance.
12. [CSS, Less, and Sass](12-css-less-and-sass.md):
   scoped technical audit and verification of retained guidance.

[Human and AI checkpoints](human-ai-checkpoints.md) records the judgements that
automated checks cannot establish.

## Delivery order

Agree the contract in package 01 before changing the core workflow. Packages
02 and 03 can then progress independently. Package 04 supplies mechanical
checks; package 05 evaluates the resulting behaviour. Package 06 follows a
recorded human pass against the original criteria or an explicit human-approved
exception to package completion requirements for the evaluated revision. The
[package 05 decision](evidence/05-completion-and-exceptions.md) records the latter.
A finished failed or unresolved evaluation alone does not complete a package.

Task 07 is an optional follow-up to the accepted advisory severity limitation.
It does not block package 06 or require further package 05 reviews. Its scope
is planning only; agree any diagnostic inputs and run criteria before evaluation.

## Language audit requirements

Packages 08–12 are planned follow-on audits of the references deferred by package
03. The user requested insertion of task 07 on 25 October 2026; pending language
audits formerly numbered 07–11 are now 08–12. Package 06 retains its number
and scope. The language audits do not require package 06 or task 07 to run first.
Planning authorisation does not mark implementation, validation, or human
checkpoints complete. No guide is verified by these plans.

The language groups can proceed independently after their scope is agreed.
Coordinate edits to the common-bug checklist and reference status across groups.
Preserve package 05's agreed evaluation scope: add language fixtures in separately
agreed batches with acceptance criteria fixed before model runs. New guide
changes require proportionate re-evaluation of affected behaviour before any
release claim for that revision. Package 06's release-candidate checks and
disclosure requirements still apply.
Package 05's accepted completion exceptions are not reopened by these audits.

Each audit follows the Python package's method:

- Start with declared language, compiler, runtime, framework, and platform
  versions. Check retained technical claims in primary documentation and record
  versioned sources where available, access dates, and evidence limitations.
- Replace inherited good/bad recipes with concrete triggers, consequences, and
  project requirements. Preserve useful language-specific coverage while
  removing unsupported blanket rules and automatic priorities.
- Exercise meaningful examples with synthetic inputs, failure paths, and clean
  controls. Separate runnable examples from illustrative fragments. Use the
  installed TDD skill for behavioural code introduced during implementation.
- Consolidate only the corresponding sections of the common-bug checklist,
  checking callers and routing before removing duplicate guidance.
- Preserve reference paths, the skill name, and upstream MIT attribution. Keep
  the entry point concise and selectively routed.
- Update reference-status.md only to the extent supported by recorded evidence.
  Record translation limits honestly; align English and Chinese companion
  guidance if shared installation or usage behaviour changes.
- Run git diff --check, git diff --stat, the repository structural validator,
  and the system skill-creator quick validator when available. Verify links
  and cross-document consistency. These checks do not measure review accuracy.
- Use package 05's evidence and authority boundaries for separate behavioural
  evaluation: distributable fixtures, withheld answer keys, agreed criteria,
  raw reports, false positives, misses, and tool limits. Do not use private code
  or live PR mutations as evaluation side effects.

Installation, publishing, helper redesign, and unrelated language rewrites stay
outside these audit packages. Record package evidence under plans/evidence/
when work produces it; do not create placeholder success records.

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
