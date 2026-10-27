# Task 07: priority-boundary audit and decision brief

Initial audit prepared on 27 October 2026. The user subsequently agreed the
priority interpretation and preparation, recorded below. The runtime
clarification and fixture preparation are implemented. The approved six-review
diagnostic has finished; final disposition remains pending. The later sections record successive checkpoints; earlier
pending statements describe their preparation stage.
This record does not complete task 07. The original audit below describes the
pre-edit source identified at its start.

## Scope and source identity

Audited checkout: `1bc100147099d08e7ad7189d766c4f8f6ff07d8f`, on
`codex/task-07-severity-calibration`. The working tree was clean before this
work. The audit covers `SKILL.md`, `reference/review-contract.md`, and both
`assets/*.md` templates, together with the two original adjudication records.
The runtime files remain unchanged. Package 05's accepted runtime remains
`677beab3a37af42b08f9c46e5344b44afe84b3cf`; the checkout revision above is not
an assertion of behavioural equivalence or a newly assessed runtime.

The [task plan](../07-severity-calibration.md) authorises scoping and requires
human agreement before selecting a correction or diagnostic rubric. The user
requested work on this plan on a new branch; that request is not recorded as
agreement to a particular priority interpretation or six-review experiment.

## Wording audit

| Surface at the audited revision | Observed guidance | Assessment |
| --- | --- | --- |
| `SKILL.md`, lines 35–41 | Requires trigger, impact and evidence; assigns priority by impact and urgency; separates assumptions. | Consistent with the contract. No independent priority table or deployment-specific rule. |
| `reference/review-contract.md`, lines 77–85 | P0 includes demonstrated release-wide failure without special conditions; P1 includes core-path failure before the affected release or next use. | Potential overlap: a mandatory step failing for every invocation can be read as release-wide failure even when the evidence establishes only a blocked future operation. |
| Same contract, lines 87–95 | Project definitions govern; confidence concerns support, not impact; unresolved essential premises become questions. | Already separates confidence correctly. A successful reproduction does not itself establish urgency or breadth. |
| `assets/pr-review-template.md`, finding block | Requests trigger, observable impact, evidence, and separate assumptions; delegates labels to the contract. | Consistent. Does not independently request breadth or urgency, but does not contradict them. |
| `assets/review-checklist.md`, Verify candidates | Delegates priority to the contract and separates confidence and assumptions. | Consistent. No competing definitions to reconcile. |

This is a focused audit of the named surfaces, not a technical audit of every
inherited guide. The contract governs conflicting inherited advice. Nothing in
this audit establishes that all language guides apply priorities correctly.

## Cause assessment from existing evidence

The [batch 01 adjudication](05-behavioural-evaluation/runs/batch-01/adjudication.md)
accepted two fixture limitations: retention impact did not settle P1 versus P2,
and the status display's operational role did not justify the prescribed P2.
Those cases establish the need for explicit impact premises, not a general
instruction to lower priorities. Their original failed scores remain failed.

In [batch 02](05-behavioural-evaluation/batch-02/execution/adjudication.md),
the target establishes a required gate, no supported bypass, and inability to
start the next operation. The report correctly reproduces the caller failure
and acknowledges that deployment integration was not run. It assigns P0 from
the unconditional blockage. It does not provide evidence of a running-release
incident or immediate severe loss. The agreed rubric requires P1.

AI assessment: the report's interpretation of “release-wide failure” plausibly
explains the overlap. The P0 table's immediate-action meaning and P1's
next-operational-use meaning favour the agreed P1, but the table does not
explicitly say how those meanings constrain a broadly failing pre-release
step. This is a plausible wording/interpretation ambiguity, not demonstrated
systematic miscalibration. A single disputed label does not establish model
reasoning causality or prove that an edit will improve future reviews.

Four dimensions should remain distinct:

- Impact: what fails, is lost, or is exposed, and its recovery cost.
- Urgency: why action is immediate, due before the next use, or deferrable.
- Breadth: which supported users, operations, or configurations are affected.
- Trigger: the supported conditions making the failure reachable.

Confidence describes evidence for those claims. A release-blocking decision
is a project's acceptance decision; it does not independently prove P0.
Likewise, a conditional trigger can support P1 when consequences are severe.
No rule should classify every deployment gate, display, or retention change
at one fixed priority.

## Proposed decision, not selected guidance

Recommendation for human consideration: accept the limited ambiguity above
and permit a general clarification in the contract alone. Keep the P0–P3 table
and target-project override. A possible paragraph, subject to approval, is:

> Assess impact, urgency, breadth, and triggering conditions separately. For
> P0, explain the evidence requiring immediate action as well as the broad
> severe consequence. Failure on every invocation, or a requirement to block
> a release, does not alone establish that urgency and impact. A core-path
> failure that must be corrected before the affected release or next supported
> use can warrant P1. Do not infer an ongoing incident from a failed future
> operation. Supported conditional triggers can still warrant high priority.

This is draft text in planning evidence only. It does not silently replace the
approved contract. Human alternatives are a narrower clarification, different
interpretation, or no runtime change with an explicit retained limitation.
A no-change decision is valid. Existing results cannot test any option.

The [diagnostic proposal](07-severity-diagnostic-proposal.md) makes the proposed
cases, scoring dimensions, settings and limits reviewable. It is not a frozen
rubric or permission to dispatch. Agree the interpretation first; then prepare
and check concrete fixtures, inspect the available runtime, and obtain agreement
to the exact immutable inputs and candidate before any reviews.

## Verification and remaining work

The source inspection and local CLI version check ran on 27 October 2026.
`codex --version` reported `codex-cli 0.164.0-alpha.11.1`, with a warning that
PATH aliases could not be created on the read-only filesystem. This does not
verify evaluator authentication, isolation, or model availability. No context
preflight or model invocation ran. No original batch artefact was changed.

Validation on 27 October 2026:

- `python3 -B scripts/validate-skill.py`: passed structure and local link targets,
  including both new evidence documents. Manually checked that the plan index
  and task status consistently describe the pending checkpoint.
- System skill-creator `scripts/quick_validate.py .`: passed.
- British house-style linter: zero errors and warnings on the task plan and both
  new evidence documents; the final check also includes the edited plan index.
- `git diff --check` and `git diff --stat`: run for tracked edits; new documents
  are additionally checked and counted with `git diff --no-index` against
  `/dev/null`, since ordinary diff excludes untracked files.
- Runtime and historical batch artefacts are unchanged. No helper or behavioural
  tests are claimed: these changes are planning documents, not runnable fixtures.

These checks establish structural consistency, not priority accuracy. Task 07
remains open until the required human decisions and any agreed bounded
diagnostic finish.


## First human agreement and prepared candidate

On 27 October 2026, the assistant asked whether the user agreed that P0 requires
evidence of immediate urgency alongside broad severe impact, and approved
preparing the proposed clarification and concrete fixtures. The user replied,
“Agreed”. Reviewer identity: the user in this chat; no personal name supplied.
This selects the proposed general clarification for preparation. It does not
approve the exact diagnostic inputs/settings, dispatch, the final assessed
candidate, installation, or a release.

The proposed paragraph above is now inserted after the contract's priority
table. Other runtime guidance and templates are unchanged. Six original
synthetic fixtures and their test-first standard-library checker are prepared;
twelve non-inference context renders contain no grading materials or inherited
repository instructions under the documented local inspection limits.
The [prepared diagnostic](07-severity-diagnostic/README.md) records concrete
inputs, criteria, key, candidate, commands/settings, proposed temporary login
reuse and remaining execution limits. That package awaits the second checkpoint.
The earlier design proposal remains a historical proposal, not an approved key.

Post-preparation checks are recorded with the frozen package. Structural validity
and fixture premise checks do not establish model priority accuracy. No old
batch artefact or installed personal skill was changed.


## Second checkpoint package identity

Prepared on 27 October 2026; no model reviews run. The full preparation manifest
[`07-severity-diagnostic/preparation-sha256sums.txt`](07-severity-diagnostic/preparation-sha256sums.txt)
has SHA-256 `91121c929ed1ea3c4046c91d79a3a6f9bc0fe2b7b48da0a7c720df4975ac421d` and records 139 artefacts.
The candidate manifest SHA-256 is
`64915ca703ad8bfef44fd31757ac54bb795e0d3991049ed243ae1c3b4b436bbc`;
the fixture-input manifest SHA-256 is
`bd799c0e58c99d7e66650ae167a9998ab0a9492329481897a61b8c46c81548ee`.

The [run protocol](07-severity-diagnostic/README.md) and
[criteria](07-severity-diagnostic/acceptance-criteria.md) request at most six
fresh standalone reviews, one per case, requested `gpt-6.1-sol` with medium
reasoning, no repeats or upstream comparison, and temporary reuse of the
existing login through an auth symlink without reading credential bytes.
Authentication and actual backend settings remain unverified. Approval must
identify this manifest and the disclosed limits before dispatch. Pre-launch
hash/context/settings checks still apply. No second agreement is recorded.

[Validation](07-severity-diagnostic/validation.md) records six premise tests,
18 repository tests, 13 guide checks, repository/candidate structural checks,
link and house-style checks, and preserved whitespace in inherited/copied
artefacts and raw output. These are preparation results, not model scores.


## Run agreement, first attempt and live-context stop

On 27 October 2026, after presentation of the exact frozen package and request
for six reviews, the user replied “Approved”. The
[run agreement](07-severity-execution/agreement.json) pins the approved manifests.
One review ran and produced the expected P1 finding with correct detection and
evidence. Its live initial context contained additional general plugin guidance,
recommended-plugin catalogue, default-mode instruction and tool declarations
absent from the exact local debug preview. Model/reasoning settings matched;
no grading material or repository instruction leakage was observed.

The protocol requires halting on substantive differences. Case 01 is retained
with isolation unresolved; cases 02–06 stopped before authentication/dispatch.
The [execution record](07-severity-execution/README.md) records the frozen raw
output manifest, proposed separate scores, tool limits and authentication-link
cleanup. No retry or replacement occurred. The
[continuation amendment](07-severity-execution/continuation-proposal.md) requests
agreement to the exact observed live defaults for the five unused slots only.
It preserves case 01's original unresolved isolation result. Its manifest
SHA-256 is `7d971412dd210eb1388254a1edd0a7d2d7baf08e489b06096c0d61b1bf92c1f8`.
No amendment agreement or final disposition is recorded yet. The frozen
preparation and original batch artefacts remain unchanged.


## Approved continuation and final diagnostic result

After explanation of the live-baseline procedure, the user replied “Approved”
on 27 October 2026 to the five-slot continuation amendment. The
[continuation agreement](07-severity-execution/continuation-agreement.json)
pins its manifest. Cases 02–06 ran once each, matched the explicitly accepted
live baseline and actual settings, preserved all input hashes, and removed
their temporary authentication links. Case 01 and its original unresolved
isolation result remain unchanged. Exactly six reviews produced six reports;
there were no retries or replacement outputs.

The [final scorecard](07-severity-execution/final-scorecard.json) proposes four
of four seeded defects detected with complete evidence, all four expected
priorities matched (P1/P3/P0/P2), both clean controls passed, zero unsupported
findings, and scope/authority passes in six reports. Five contexts pass under
the approved continuation; the first remains unresolved under its original
agreement. The original all-criteria result is not retrospectively passed.

Before final scoring, 161 raw/output/setup artefacts were frozen in
[the complete raw manifest](07-severity-execution/all-outputs-sha256sums.txt),
SHA-256 `d7d29c52a2c4bc88e1c0b7913b81cb1375edabfcc6eaca412cbb054089aafc82`.
All original frozen manifests still verify. Forty local shell commands include
six unavailable-rg events with successful fallbacks; actual reviewer tool use
and verification claims were inspected. No prohibited access or authority
violation was observed. Exact backend build and broader reliability remain
unverified; operational incidents are synthetic premises.

The [completion proposal](07-severity-execution/completion-proposal.md)
recommends accepting the same candidate manifest
`64915ca703ad8bfef44fd31757ac54bb795e0d3991049ed243ae1c3b4b436bbc`
and closing task 07 with the retained first-context limitation. It does not
claim the edit caused an improvement, repair the CLI preview, change old batch
scores, or select a package 06 release. Repository tests (18), guide checks
(13) and live-baseline comparator tests (five) pass; validation is separate
from priority accuracy. Final human acceptance is pending; task 07 is open.


The [final disposition manifest](07-severity-execution/disposition-sha256sums.txt)
pins the completion proposal, final scores, trace/validation evidence, run
agreements and complete raw-output manifest. Its SHA-256 is
`dd5b007bbc13447e7651d4eb245ee8fe5158480834babbba2ae5be0bfc79bd70`.
Human acceptance of this disposition and assessed candidate has not yet been
recorded. Original frozen manifests and all candidate file bytes verify.


## Conditional acceptance and requested PR loop

The user subsequently requested commit, push, PR creation and the complete
CodeRabbit loop, stating that the changes are approved once CodeRabbit has
completed its reviews. The [conditional decision](07-severity-pr-approval.md)
records the exact assessed candidate, accepted isolation limitation and required
current-head review/check/merge gates. It supersedes the earlier request for
another final acceptance question. Frozen proposals, scores and raw evidence
remain historical artefacts and are not rewritten to record this later decision.
