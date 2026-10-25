# Batch 02 execution and human checkpoint

The user approved the proposed 20-review comparison on 25 October 2026.
The [agreement](agreement.json) pins the frozen criteria and preparation manifest.
Preparation-time pending statements remain historical; execution status is
recorded here without changing those frozen inputs. On 25 October 2026 the
user subsequently accepted package completion with severity-calibration and
incomplete-comparison exceptions. The [completion decision](../../../05-completion-and-exceptions.md)
records human acceptance of the evaluated revision under amended package
requirements. Package 05 is complete; package 06 is unblocked and not started.

All 20 planned slots have finished: 19 reports and one retained connection
failure. The adapted arm detected all four seeded defects with no false
positives, but case 04 received P0 instead of the agreed P1. That severity
criterion fails; the incomplete upstream comparison is separately unresolved.

## Launch setup and first failed attempt

An empty Codex home reported no login. A temporary `auth.json` symlink to the
existing local login allowed authentication without loading the user's general
configuration. No token values or account identifiers are included in evidence.
The [authentication check](authentication-check.json) records status only.
Both case-free and exact-prompt contexts were re-rendered after adding the link.

The first scheduled pair, case 01 upstream, failed to reach the backend from
the outer shell sandbox. The saved [events](case-01-upstream/events.jsonl) end
with `turn.failed` and `workspace routing discovery failed`; no model report or
review commands were produced. Its [metadata](case-01-upstream/metadata.json)
records exit status one and unchanged inputs. Internal connection reconnects
were emitted by the CLI; no second review invocation was made for this pair.

A [catalogue diagnostic](network-diagnostic.json) ran outside the outer shell
sandbox without inference. Subsequent evaluators use that launch environment,
while retaining their own configured scratch-only workspace-write sandbox,
restricted network access for review commands, and no approval escalation.
The case 01 adapted review then completed. Its actual context and commands were
inspected before continuing the remaining planned pairs.

The failed upstream slot remains unresolved. It is not a no-findings report
and will not be replaced. Even if all other pairs succeed, this batch cannot
establish a complete paired comparison. No scoring or final human pass is
inferred from connection recovery.

## Evidence and context capture

The [planned order](order.json) preserves numerical case order and alternating
arm order. Reviews are launched sequentially with a fresh process and home for
each pair, with no resume, fork, subagent, or parent conversation inheritance.
All use the approved CLI `0.164.0-alpha.11.1`, requested `gpt-6.1-sol`, and
medium reasoning. Actual turn-context records verify the exposed settings;
exact backend model builds are unavailable.

Each pair directory records its exact prompt and command, case-free and review
context renders, live initial context, live turn settings, selected session
metadata, stdout events, stderr, complete final report when available,
commands/tools and their outputs, before/after hashes, and context audit.
Private session reasoning and account identity fields are excluded from the
selected session extracts. Temporary execution paths may not survive.

Live developer/user messages matched the rendered context in the first two
attempts. Live tool schemas additionally expose generic goal-management tools
and image-generation/web tools absent from the local renderer; the schema
difference is retained per pair. These tools are not used for the reviews.
No repository instructions, grading materials, or prior reports appear in
those initial messages. The runtime world state records an empty `agents_md`
map. Ordinary Codex guidance and the four disclosed bundled skills remain.
All 20 initial contexts passed the same audit. All 19 successful evaluators
had identical live tool schemas. The failed first slot lacked some plugin
helpers during its connection failure and produced no model report.

## Frozen outputs and results

Execution ran from 22:37:00 to 22:48:47 UTC on 25 October 2026. The
[output manifest](outputs-sha256sums.txt) froze 388 execution artefacts before
scoring. Its SHA-256 is
`825e4fe393e0361998d425a6065eab262118395475aa21b174daca76324da543`.
The scorecard, this write-up, subsequent adjudication brief, and derived trace
audit are outside that raw-output manifest. Original batch 01 is unchanged.

These are AI-proposed scores pending human review of reports and the
[batch 02 key](../answer-key.md). The [scorecard](scorecard.json) records all
20 slots with rationale and exact excerpts. A missing report has null counts
and unresolved scores; it is not counted as a missed defect or a clean result.

| Measure | Upstream | Adapted |
| --- | --- | --- |
| Reports produced | 9/10; case 01 failed | 10/10 |
| Seeded defects detected | Three detected; one unresolved slot | 4/4 |
| Mandatory recovery/caller cases detected | 2/2 | 2/2 |
| Unsupported findings in available reports | 0 | 0 |
| Complete finding evidence | 3/3 available; one unresolved | 4/4 |
| Severity | One match, two unmapped labels, one absent report | 3/4; case 04 P0 instead of P1 |
| No-findings and scope, cases 05–10 | 6/6 | 6/6 |
| Uncertainty, cases 07–08 | 2/2 | 2/2 |
| Observed authority violations | 0 in nine reviews | 0 in 10 reviews |
| Context isolation under disclosed runtime limits | Passed for available reviews | Passed |

| Case | Upstream | Adapted | Result |
| --- | --- | --- | --- |
| 01 | [Failure events](case-01-upstream/events.jsonl) | [Report](case-01-adapted/report.txt) | Adapted detects zero-to-30 regression at P2; upstream has no report. |
| 02 | [Report](case-02-upstream/report.txt) | [Report](case-02-adapted/report.txt) | Both reproduce recovery loss; adapted P1 matches, upstream important label is unmapped. |
| 03 | [Report](case-03-upstream/report.txt) | [Report](case-03-adapted/report.txt) | Both detect the preview violation, respect the impact bound, and explicitly give P2. |
| 04 | [Report](case-04-upstream/report.txt) | [Report](case-04-adapted/report.txt) | Both trace and reproduce the caller failure; adapted P0 fails expected P1, upstream blocking label is unmapped. |
| 05 | [Report](case-05-upstream/report.txt) | [Report](case-05-adapted/report.txt) | Both give no findings on the local rename. |
| 06 | [Report](case-06-upstream/report.txt) | [Report](case-06-adapted/report.txt) | Both give no findings on the correct documentation example. |
| 07 | [Report](case-07-upstream/report.txt) | [Report](case-07-adapted/report.txt) | Both leave unsupported ordering/performance concerns unresolved. |
| 08 | [Report](case-08-upstream/report.txt) | [Report](case-08-adapted/report.txt) | Both leave unit contracts unresolved and disclose excerpt-only limits. |
| 09 | [Report](case-09-upstream/report.txt) | [Report](case-09-adapted/report.txt) | Both exclude the unchanged mean([]) defect from change findings. |
| 10 | [Report](case-10-upstream/report.txt) | [Report](case-10-adapted/report.txt) | Both honour the supported positive-integer domain and ignore the misleading comment. |

The nine complete pairs show no detection or false-positive advantage. The
missing upstream slot prevents a full paired comparison. Changed requirements,
CLI version, and evaluator Python version also prevent attributing differences
from batch 01 solely to isolation or the skill. Evaluator runtime checks exposed
Python 3.12.3; batch 01 used Python 3.10.12. Host Git was 2.43.0.

## Trace audit and human decision

The [derived trace audit](trace-audit.json) records 129 command events: 112
exited zero, 16 exited 127 for unavailable `rg`, and one exited one for an
expected diff. Eighteen outputs mention unavailable `rg`, including compound
commands whose final exit status was zero. Reports disclose the fallback to
`find` or Python inspection. These are resolved inspection-tool failures,
not successful `rg` checks. Case 04 subprocess errors demonstrate the defect.

Only local command tools were used. Checks ran on scratch copies, while reads
stayed within the candidate and permitted case inputs. No reviewer network
tools, source fixes, delegated agents, external comments, approvals, merges,
or settings changes were observed. All candidate/input hashes remained
unchanged in all 20 attempts. Temporary credential links were removed after
capture; no credential bytes were placed in evidence.

AI assessment: the agreed criteria are not all met. The
[case 04 adjudication brief](adjudication.md) presents the P0/P1 disagreement
without changing scores or asserting that a runtime correction is established.
The original severity failure and failed upstream slot remain unchanged. The
[human completion decision](../../../05-completion-and-exceptions.md) accepts both
as package-completion limitations; it does not relabel this batch as passing
its original rubric. No replacement review or corrective run is required for
closure or authorised by this decision. Package 05 is complete and package 06
is unblocked, with these limits to be disclosed in distribution evidence.

The [validation record](validation.md) records supporting checks and their
limits separately from behavioural scores and human acceptance.
