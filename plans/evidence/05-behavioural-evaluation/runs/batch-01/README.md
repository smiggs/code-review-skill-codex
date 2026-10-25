# Batch 01 results and human checkpoint

Historical batch results below retain their original scores and limits. The
later [completion decision](../../../05-completion-and-exceptions.md) accepts
package 05 with explicit limitations and unblocks package 06; it does not
retroactively pass this batch. Earlier pending/blocking statements describe
status at the time of batch 01.

The initial 20 reviews are finished. The adapted skill found every seeded defect
and produced no false positives, but it did not meet the agreed severity
criterion in two cases. Evaluation independence is unresolved because the
subagent runtime injected the repository's review guidance into every context.
Package 05 has no human pass and package 06 remains blocked.

## Agreement and execution

The user agreed on 25 October 2026 before dispatch; the
[agreement record](agreement.json) pins the criteria, manifest, evaluator
arrangement, and limitations. The original [protocol](../../README.md),
[criteria](../../acceptance-criteria.md), prompt, fixtures, and key remain frozen.
Their preparation-time pending-status statements are historical; this document
and the package evidence record execution status.

The reviews ran from 17:27:17 to 17:35:15 UTC on 25 October 2026, in the
[recorded dispatch order](order.json). Three evaluator slots overlapped, but
dispatch followed numerical case order and the agreed alternating arm order.
Every dispatch used a fresh context with `fork_turns=none`, without a model or
reasoning override. All 20 session records expose `gpt-6.1-sol`, medium reasoning,
OpenAI provider, and CLI version `0.163.0-alpha.10.2`. They used Python 3.10.12
and Git 2.34.1 on Linux. Exact backend model build and nested shell-tool version
are unavailable. This was one review per case/arm; no repeats or correction
reviews were run.

Each case/arm directory contains the dispatched `prompt.md`, complete
`report.txt`, `metadata.json`, `tools.jsonl`, `commands.jsonl`, and the
`inherited-user-context.json` automatically supplied by the runtime. Tool traces
preserve calls and outputs; command events additionally preserve actual shell
commands, working directories, exit codes, outputs, and durations. Session
private reasoning and account metadata are excluded. The local runtime encrypts
task-message bodies in its session storage; the separately saved dispatch
prompts preserve the plaintext requests sent in this chat.

The [output manifest](outputs-sha256sums.txt) froze all 122 execution artefacts
before scoring. Its SHA-256 is
`1fa2d45820635dac1ca90219bed51a0bac0788ef95988b881842f9cd1db565e3`.
The scorecard and this write-up are grading artefacts outside that manifest.
Temporary paths in reports and metadata identify execution locations; use the
source fixtures and pinned revisions to recreate inputs rather than depending
on those temporary directories surviving.

## Paired results

These are AI-proposed scores, subject to human adjudication. Counts describe
this batch only. Shared inherited guidance limits attribution to either skill.

| Measure | Upstream | Adapted |
| --- | --- | --- |
| Seeded defects detected | 4/4 | 4/4 |
| Mandatory recovery/caller cases detected | 2/2 | 2/2 |
| Unsupported defect findings | 0 | 0 |
| Complete location, trigger, impact, and evidence | 4/4 | 4/4 |
| Explicit severity matches | 0/4; two unmapped labels, two mismatches | 2/4; two mismatches |
| No-findings and scope handling, cases 05–10 | 6/6 | 6/6 |
| Uncertainty handling, cases 07–08 | 2/2 | 2/2 |
| Observed authority violations | 0 | 0 |
| Evaluation independence | Unresolved | Unresolved |

The adapted skill used P1 rather than the required P2 in case 03's retention
normalisation and case 04's broken status rendering. Upstream also used P1 in
both cases; cases 01 and 02 used `blocking` without an explicit P-label mapping.
The fixed rubric therefore scores adapted severity as two failures and upstream
severity as two failures plus two unresolved mappings. Severity does not erase
a correctly detected defect or create a false positive.

| Case | Upstream raw report | Adapted raw report | Paired judgement |
| --- | --- | --- | --- |
| 01 | [Report](case-01-upstream/report.txt) | [Report](case-01-adapted/report.txt) | Both detect zero becoming 30; adapted gives required P2, upstream has unmapped blocking label. |
| 02 | [Report](case-02-upstream/report.txt) | [Report](case-02-adapted/report.txt) | Both reproduce recovery loss; adapted gives required P1, upstream has unmapped blocking label. |
| 03 | [Report](case-03-upstream/report.txt) | [Report](case-03-adapted/report.txt) | Both honour archive instructions and reject misleading comment; both give P1 instead of P2. |
| 04 | [Report](case-04-upstream/report.txt) | [Report](case-04-adapted/report.txt) | Both trace unchanged caller and reproduce TypeError; both give P1 instead of P2. |
| 05 | [Report](case-05-upstream/report.txt) | [Report](case-05-adapted/report.txt) | Both correctly report no findings on the local rename. |
| 06 | [Report](case-06-upstream/report.txt) | [Report](case-06-adapted/report.txt) | Both correctly report no findings on the documentation example. |
| 07 | [Report](case-07-upstream/report.txt) | [Report](case-07-adapted/report.txt) | Both identify missing order and performance requirements without a finding. |
| 08 | [Report](case-08-upstream/report.txt) | [Report](case-08-adapted/report.txt) | Both leave the unit contract unresolved and disclose excerpt-only limits. |
| 09 | [Report](case-09-upstream/report.txt) | [Report](case-09-adapted/report.txt) | Both separate the existing mean([]) defect from the unchanged total behaviour. |
| 10 | [Report](case-10-upstream/report.txt) | [Report](case-10-adapted/report.txt) | Both honour the positive-integer cache contract and report no findings. |

The [per-report scorecard](scorecard.json) includes counts, misses, severity,
evidence completeness, scope, uncertainty, authority, rationale, and exact
report excerpts. The [answer key](../../answer-key.md) remains separate from
all evaluator inputs. Paired detection and false-positive differences are zero;
this batch supplies no evidence that the adaptation improves those measures.

## Tool and context audit

The 101 completed shell command events were inspected. Every top-level shell
command exited zero. The case 04 subprocesses intentionally returned one with
TypeError in head and zero with ready in base; reports accurately distinguish
those child results. Some checks printed expected mismatches while returning
zero, which the reports disclosed. No network tools, source fixes, commits,
posted comments, approvals, merges, or settings changes were attempted.
Reads stayed within the chosen candidate and case inputs; runtime checks used
scratch copies. Before/after candidate and input file hashes match in every
case. Scratch files, including recovered/deleted synthetic data and Python
caches, were confined to the authorised temporary workspaces. No private code
or secrets were supplied or included in reports.

All 20 contexts automatically received the same 7,343-byte serialised user
context containing this repository's `AGENTS.md` and environment. That guidance
includes evidence, scope, severity, and authority rules resembling the adapted
contract. It was supplied by the runtime despite `fork_turns=none`; evaluators
did not fetch it by violating the access instruction. No answer key, prior
review report, criteria, sibling fixture, or parent conclusions appeared in
that inherited user context. Its bytes are saved alongside each report so this
limit can be checked rather than inferred.

Both arms had equivalent tool permissions and shared context, and the reports
show the two fixture-specific retention contracts being honoured. However,
these results cannot establish behaviour without global review guidance or
attribute the upstream's restraint solely to its own skill. The protocol's
fresh-context isolation requirement therefore remains unresolved. A future
batch needs evaluators launched outside this repository's instruction scope
and an inspection of the initial context before dispatching review cases.

## Human checkpoint and follow-up

AI assessment: the agreed adapted-skill criteria are not all met. The user
accepted the severity adjudication on 25 October 2026: case 03 has ambiguous
impact evidence, and case 04's expected P2 is insufficiently justified by its
fixture. The overall checkpoint remains unresolved; original scores and
pre-agreed criteria are unchanged.

No runtime skill correction or rerun was made. The P1 judgements refer to risks
and core-path failure that the existing severity contract can plausibly support;
forcing those two examples to P2 without adjudication would tune to the key.
The inherited-context problem is in evaluator setup, not demonstrated faulty
runtime instructions. Those issues need resolution before a justified narrow
correction can be selected. A fully isolated repeat of 20 reviews exceeds the
agreed six-review correction bound and needs a separately agreed batch.

The [severity adjudication record](adjudication.md) presents the evidence,
accepted recommendations, and the user's decision. Neither dispute establishes
faulty skill guidance. Future fixture impact and severity expectations need
clarification and agreement before evaluation.

Retain this finished run regardless of the decision. Only a later recorded
human pass against criteria met by the evaluated revision can complete package
05 and permit package 06. Approval of the criteria was not approval of results.

## Recorded stopping point

On 25 October 2026 the user requested, "Record the scoring only". The
20-report scorecard and raw reports are saved. No further evaluation, runtime
correction, or rerun followed that instruction. The subsequent severity
adjudication is recorded above; package 05 is open and package 06 remains blocked.
