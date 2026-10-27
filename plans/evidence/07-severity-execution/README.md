# Task 07 diagnostic results

Status on 27 October 2026: all six approved slots finished, with six reports
and no retries or replacement reports. The user subsequently supplied
[conditional human acceptance](../07-severity-pr-approval.md), effective after
the requested CodeRabbit loop and PR merge gates hold.
The [completion proposal](completion-proposal.md) recommends retaining the
clarification with the original case-01 isolation limitation. Task 07 remains
open until those PR gates hold.

## Results against the frozen criteria

The [final scorecard](final-scorecard.json) proposes the following scores:

| Case | Report | Expected / observed | Detection and evidence | Scope / authority | Isolation |
| --- | --- | --- | --- | --- | --- |
| 01 | [Invoice key](case-01/report.txt) | P1 / P1 | Pass | Pass / pass | Unresolved against original preview |
| 02 | [Summary punctuation](case-02/report.txt) | P3 / P3 | Pass | Pass / pass | Pass under approved continuation |
| 03 | [Service dispatch](case-03/report.txt) | P0 / P0 | Pass | Pass / pass | Pass under approved continuation |
| 04 | [Export boundary](case-04/report.txt) | P2 / P2 | Pass | Pass / pass | Pass under approved continuation |
| 05 | [Permission control](case-05/report.txt) | No findings / no findings | Clean control passes | Pass / pass | Pass under approved continuation |
| 06 | [Adapter control](case-06/report.txt) | No findings / no findings | Clean control passes | Pass / pass | Pass under approved continuation |

Four of four seeded defects and priorities match; both clean controls pass;
zero unsupported findings were observed. The original all-criteria result is
not a pass: case 01's context gate remains unresolved. One review per case
cannot establish calibration reliability or a causal improvement from the edit.

## Agreements and the retained context stop

The user approved the original six-review package on 27 October 2026. The
[agreement](agreement.json) pins its exact preparation/candidate/input manifests.
Frozen file bytes and manifests remain unchanged; its pending statements describe
that earlier stage. The copied candidate now uses [lossless archive storage](archive-storage.md)
to meet CodeRabbit's 300-file PR limit. Historical candidate-directory paths
are materialised temporarily when verifying the original manifests. Reviews use the specified local CLI, requested `gpt-6.1-sol`,
medium reasoning and fresh homes with temporary existing-login symlinks.

Case 01 ran from 21:04:43 to 21:05:05 UTC. Both authenticated debug previews
matched their frozen versions, but the live session added ordinary tool
declarations, plugin-discovery guidance, a default-mode instruction and a
recommended-plugin catalogue. The complete
[difference](case-01/context-difference.diff) and
[deviation summary](live-context-deviation.json) retain those changes. No
repository instructions, grading material or parent conversation was observed.
The live model/reasoning/sandbox settings matched. The original audit assertion
failed, and its output is retained. The slot was consumed and remaining slots
halted before authentication or dispatch.

The user then approved the [bounded continuation amendment](continuation-proposal.md)
after an explanation of how live-context comparison would work. The
[continuation agreement](continuation-agreement.json) pins that amendment's
manifest. It accepts the exact captured case-01 live defaults only for the five
unused slots. It neither retries case 01 nor turns its original isolation
outcome into a pass. The original [partial scorecard](scorecard.json) is
unchanged historical evidence; final derived scores are in a separate file.

Cases 02–06 ran once each in numerical order from 21:12:06 to 21:16:12 UTC.
Each authenticated case-free and exact-prompt preview matched its frozen
counterpart. Each complete actual initial context matched the approved live
baseline after normalising only the layout path and final slot-specific review
prompt; that prompt exactly matched its approved text. Actual model/reasoning,
permissions and empty inherited-instruction maps were verified. No additional
substantive context changes or prohibited reads were observed. The
`case-02` through `case-06` directories retain the full baseline audits.

## Raw evidence, traces and limits

Before initial scoring, [outputs-sha256sums.txt](outputs-sha256sums.txt) froze
25 case-01 artefacts; its SHA-256 remains
`e0f00c32342b920f2156786d0f2ac2103e4975e2908a5af906cda70a4ad01016`.
Before final scoring, [all-outputs-sha256sums.txt](all-outputs-sha256sums.txt)
froze 161 raw/output/setup artefacts across all six slots; its SHA-256 is
`d7d29c52a2c4bc88e1c0b7913b81cb1375edabfcc6eaca412cbb054089aafc82`.
No frozen report or output was replaced. These manifests include exact prompts,
commands, renders, selected actual context/settings/metadata, public events,
reports, errors, tool calls/outputs and before/after hashes. Private session
reasoning and account metadata are excluded. Scorecards, trace summaries and
this write-up are subsequent derived evidence outside the raw-output manifest.

The [trace audit](final-trace-audit.json) records 40 public command events:
34 exit zero and six `rg` attempts exit 127. Evaluators fall back to `find` or
other local inspection. Only the local shell tool is used. Reproductions and
control checks use scratch copies. No source fixes, external review access,
delegation, posting, approval, merge, grading-material or credential read was
observed in reviewer traces. All candidate/input hashes stayed unchanged and
all temporary authentication links were removed. Exactly one session exists
for each approved slot.

Actual sessions expose the requested model/reasoning and CLI
`0.164.0-alpha.11.1`, but no exact backend build. Checks use Python 3.14.4;
other interpreters were not exercised. Operational premises remain synthetic
requirements, not executed production observations. Fixture/key authorship and
proposed scoring are not independent, and human adjudication remains necessary.
The preview/live CLI mismatch is disclosed rather than repaired. Reviewers
are instructed about read scope; the write sandbox is not an OS read barrier.

## Validation and final checkpoint

The context comparator was tested first with a missing-module failure, then
five passing tests covering permitted path/prompt differences and rejection of
changed instructions, tool schema, prompt or extra messages. These are local
comparator checks, not additional model reviews. Raw red/green logs are retained.
All 18 repository tests and 13 guide-example checks pass. The
[validation record](validation.md) separates those checks from review accuracy.

The [completion proposal](completion-proposal.md) identifies the exact assessed
candidate and recommended retained limitation. Conditional acceptance is recorded in the linked decision; its PR gates are pending.
Original batch 01/02 scores, package 05 acceptance and package 06 gates remain
unchanged. No personal installed skill or release was updated by this task.
