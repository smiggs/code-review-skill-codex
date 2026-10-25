# Package 05 preparation and decision record

Current status: package 05 is complete with human-accepted limitations on
25 October 2026. Package 06 is unblocked and has not started. The
[completion decision](05-completion-and-exceptions.md) accepts advisory severity
calibration and the incomplete upstream comparison for evaluated runtime
`677beab3a37af42b08f9c46e5344b44afe84b3cf`. This changes package completion
requirements explicitly; original batch criteria and scores remain unchanged.
The records below preserve their status at each historical stage.

## Preparation snapshot and evaluated revision

Prepared on 25 October 2026 against repository commit
`677beab3a37af42b08f9c46e5344b44afe84b3cf`. Package 05 is open. No model
review, upstream comparison, behavioural scoring, or human pass has occurred.
Package 06 remains blocked. This record documents completed preparation rather
than claiming that the package's evaluation outcome has been achieved.

The [batch protocol](05-behavioural-evaluation/README.md) pins upstream and
adapted runtime revisions, the neutral request, ten synthetic fixtures, isolated
workspace instructions, scoring fields, and a bounded correction policy. The
[proposed acceptance criteria](05-behavioural-evaluation/acceptance-criteria.md)
are ready for agreement before evaluation. The
[separate answer key](05-behavioural-evaluation/answer-key.md) is grader-only.

## Prepared scope and identity

Preparation adds this record and the batch directory and updates the plan index.
It changes no skill entry point, guides, templates, helper, installation,
contribution instructions, attribution, or licence. The fixtures are original
synthetic examples under the repository MIT licence; no private code, secrets,
live PR data, or external mutation is involved. Nothing was submitted to an
evaluator or an external review service.

Manifest SHA-256:
`57d621aa80a721bde6cdff774575ded1566070688900e9f5a461b37181e9c0ab`.
Criteria SHA-256:
`5f0fcb9c0b26a15e613e34fdcf431f388439f608654903ca214991dca5cd5de6`.
The [manifest](05-behavioural-evaluation/sha256sums.txt) covers 60 files:
fixtures, protocol, criteria, prompt, grader key, premise checker, and the
[runtime inventory](05-behavioural-evaluation/runtime-sha256.json). The inventory
records SHA-256 per runtime file from both immutable Git revisions. This evidence
file and later execution records are outside the manifest to avoid circular hashes.

The proposed batch has 20 fresh-context reviews, one for each case/arm pair.
No agents have been dispatched. Delegation and the permitted limitations are
included in the pending agreement. This author has read and created the key and
cannot provide a blind self-evaluation. Fresh evaluators must receive only the
chosen candidate, one case's permitted inputs, the neutral prompt, and scratch
access; tool traces must be inspected for leakage. This is context separation,
not a claim of an OS sandbox between evaluators and the repository.

## Preparation checks

Runtime exposed during preparation: Python 3.10.12 and Git 2.34.1 on Linux.
No evaluator model or evaluator tool version is recorded because evaluation has
not run. The preparation assistant's exact model build is not exposed.

Checks actually run:

- `python3 -B plans/evidence/05-behavioural-evaluation/fixture-checks.py`:
  seven tests passed. All ten patches applied to temporary base copies and
  produced byte-identical heads. The checker reproduced zero-timeout fallback,
  recovery loss on a failed write, target-specific retention behaviour, the
  unchanged caller's TypeError, preserved sums, and the pre-existing exception.
- The checker was written before fixture construction: its first run failed
  on missing snapshots. The next run found an incorrect checker expectation
  for unsupported zero in case 10. The checker was corrected to exercise that
  target's supported None/positive-integer domain; the final run passed.
  These are fixture-development results, not failed model reviews.
- `python3 -B -m unittest discover -s tests -v`: all 18 existing tests passed.
- An initial structural/link validation correctly failed because this evidence
  file and the manifest had not yet been written. Remaining checks and final
  validation results are recorded below after those artefacts exist.

The uncertainty fixture and billing excerpt intentionally have no executable
oracle. Static requirements, scope, and missing evidence form their answer key.
Green premise and structural checks cannot establish useful review behaviour.

## Pending human agreement

AI recommendation: accept the scoped criteria and run the initial paired batch
with fresh isolated evaluator contexts. Required adapted results include four
out of four supported detections, both mandatory cases, zero false positives,
complete evidence, stated severity calibration, correct no-findings/uncertainty
handling, and no authority violations. The proposal permits only the documented
small-sample and tool/context limits and at most one correction batch of six
adapted reviews. Upstream is measured by the same rubric but need not lose.

Human agreement: pending. No reviewer identity, approval, or decision is invented.
Record the user's decision, date, criteria/manifest hashes, allowed evaluator
arrangement, and any changed scope before the first model review. After reports
and scoring exist, a separate human checkpoint must decide pass, fail, or
unresolved for the exact evaluated revision.

## Final preparation validation

- `python3 -B scripts/validate-skill.py`: passed after the evidence and manifest
  were written; local Markdown file targets resolve.
- `python3 -B plans/evidence/03-python-examples.py`: all 13 checks passed.
- System skill-creator `scripts/quick_validate.py .`: passed. This supplements
  structure validation and does not score reviews.
- British house style lint: no errors or warnings in the four batch documents,
  this evidence record, and the updated plan index; Google variant used.
- `sha256sum -c plans/evidence/05-behavioural-evaluation/sha256sums.txt`:
  all 60 listed files matched. The paired case 03/10 patches were also compared
  byte-for-byte and are identical; only their target contracts differ.
- `git diff --check`: passed for the tracked plan-index edit. New-file
  `git diff --no-index --check /dev/null <path>` checks found no diagnostics
  outside the patch data. Three fixture patch files contain intentional single
  spaces representing blank unified-diff context lines; preserve those bytes.
- `git diff --stat`: inspected; the tracked edit is four lines in `plans/README.md`.
  Git's tracked diff omits the 62 added evidence/batch files, totalling 986 lines
  before this final validation section. `git status --short` confirms only the
  plan index and package 05 evidence are changed or added. No commit was made.

Cross-document status is consistent: the plan index, protocol, criteria, and this
record all leave behavioural evaluation and both human decisions outstanding.
The root installation and contribution guidance in both languages is unchanged.

## Acceptance recorded before evaluation

On 25 October 2026 the user replied, "Agree acceptance criteria before evaluation",
to the request to approve the proposed criteria and fresh subagents for the
20-review comparison. This accepts the criteria and manifest hashes above,
fresh contexts for both arms, the documented limitations, and the bounded
correction policy. The [agreement record](05-behavioural-evaluation/runs/batch-01/agreement.json)
was saved before dispatch. The preparation and pending-status statements above
are historical. The final human quality checkpoint remains pending.

## Finished batch 01

All 20 planned case/arm reviews completed on 25 October 2026, using fresh
subagent contexts and the agreed immutable inputs. All sessions expose
`gpt-6.1-sol`, medium reasoning, and CLI `0.163.0-alpha.10.2`. The
[run record](05-behavioural-evaluation/runs/batch-01/README.md) links raw reports,
per-case scores, prompts, full tool/command outputs, before/after hashes,
inherited context, and the execution manifest. No model review was repeated.

Both arms detected four of four defects, including both mandatory cases, with
zero false positives. The adapted arm matched severity in two of four cases;
its P1 labels for cases 03 and 04 conflict with the agreed P2 rubric. Both
arms respected target-specific requirements, uncertainty, change scope, and
analysis-only authority in the observed traces. Supplied bytes were unchanged
in all 20 workspaces. No secrets, private code, or live PR mutation was used.

Automatic injection of the repository's AGENTS.md into every subagent prevents
claiming an evaluation free from global review guidance. This shared context
is preserved for inspection and treated as an unresolved method limit. The
results do not demonstrate an upstream/adapted detection advantage.

AI assessment: criteria not all met; human checkpoint unresolved pending the
user's review of reports, answer key, severity disputes, and context limitation.
No runtime change or corrective review was justified before that adjudication.
A new isolated 20-review batch would exceed the accepted six-review correction
bound and requires separate agreement. Nothing in this finished run completes
package 05 or authorises package 06.

## Severity adjudication accepted

On 25 October 2026 the user replied, "OK I accept your recommendations", after
clarification that the original P2 expectations were too rigid for the supplied
evidence. The [adjudication record](05-behavioural-evaluation/runs/batch-01/adjudication.md)
links reports, requirements, and the contract for evaluated adapted revision
`677beab3a37af42b08f9c46e5344b44afe84b3cf`.

The accepted classifications are ambiguous fixture impact evidence for case 03
and insufficient justification for case 04's expected priority. Neither
establishes faulty skill guidance. Clarify fixture impact and agree severity
expectations before another batch; no replacement priority was approved.

Original criteria, fixtures, reports, and scores remain unchanged. This decision
does not retrospectively pass batch 01 or authorise further reviews. Evaluator
independence and the overall human checkpoint remain unresolved. Package 05
stays open and package 06 remains blocked.

## Isolated batch 02 prepared for agreement

The [batch 02 proposal](05-behavioural-evaluation/batch-02/README.md) retains both
runtime revisions and executable fixture bytes. It adds operational impact to
case 03 and 04's target requirements and proposes P2/P1 respectively. The
revised key and criteria belong to this separate batch; batch 01 is unchanged.

Two local case-free CLI context renders, outside this repository with an empty
Codex home, contain no repository instructions or prior conclusions. The
[isolation record](05-behavioural-evaluation/batch-02/isolation/README.md)
preserves exact commands, contexts, and tool help. Bundled system guidance
remains visible. No model call, authentication test, or review was performed;
actual evaluator independence is not yet established.

The proposal requests separate agreement for 20 standalone reviews with
`gpt-6.1-sol`, medium reasoning, and CLI `0.164.0-alpha.11.1`. The CLI differs
from batch 01, equally for both arms. No corrective reruns are included.
Agreement is pending; package 05 remains open and package 06 remains blocked.

## Batch 02 approval and execution

On 25 October 2026 the user replied, "approved", to the batch 02 proposal and
criteria. The [agreement](05-behavioural-evaluation/batch-02/execution/agreement.json)
pins criteria SHA-256
`ea68388fe5ea9ce43ed2bcab0b71b2bd9355a52df017b0a6349adb26d9dab595`
and manifest SHA-256
`b4bc3bbe296a54519416df9ef249c65ce25478422238d3df45f2b193cfad71d0`.
The preparation-time pending statements above and in the frozen inputs are
historical. Approval permits the 20 standalone reviews and disclosed limits,
not replacement runs or a final human quality pass.

The [execution record](05-behavioural-evaluation/batch-02/execution/README.md)
preserves authentication checks, launch context, commands, and reports. The
first upstream slot failed on backend routing before producing a report.
It is retained without retry. The next adapted slot completed after launching
outside the outer shell sandbox while retaining its own scratch-only sandbox.
Live context extraction confirms the expected messages without repository
guidance; extra goal-management, image-generation, and web tool schemas are
disclosed and unused. All planned slots have finished with 19 reports and the
single retained failure. The [scorecard](05-behavioural-evaluation/batch-02/execution/scorecard.json)
credits adapted detection of four of four defects, zero false positives, and
three of four severity matches. Case 04's P0 fails the agreed P1 expectation;
the [adjudication brief](05-behavioural-evaluation/batch-02/execution/adjudication.md)
presents the dispute without changing scores.

The output manifest froze 388 execution artefacts before scoring, with SHA-256
`825e4fe393e0361998d425a6065eab262118395475aa21b174daca76324da543`.
All 20 live contexts were audited; the 19 successful reviews had identical
tool schemas. All candidate/input hashes were unchanged. No review was repeated
and no runtime correction was made. The missing upstream report and severity
dispute leave the overall checkpoint unresolved; package 06 remains blocked.

## Completion accepted with exceptions

The user replied, "Yes approved", to completing package 05 with two recorded
exceptions and unblocking package 06. The [completion record](05-completion-and-exceptions.md)
pins the evaluated runtime, original scorecard hashes, acceptance rationale,
and limits to carry into package 06. Severity calibration is accepted as an
advisory limitation. The missing upstream case 01 report is accepted as a
comparison limitation, with no claim of superiority over upstream.

The original failed severity score and unresolved comparison slot remain.
This is human acceptance under amended package requirements, not a pass against
the frozen original rubric. No further model review or runtime correction is
required for package 05 closure. Package 06 is unblocked, not started, and
retains its own release-candidate and publication approval requirements.

## Completion-record validation

- Repository structure/link validation and the system skill-creator validator
  passed after the completion changes.
- British house style lint passed for all 11 changed instruction, plan,
  decision, and result documents, with no errors or warnings; Google variant used.
- All four manifests still verified: 640 preparation/execution entries matched.
  Both scorecards also matched the hashes in the completion record.
- `git diff --check` passed and `git diff --stat` was inspected. Authored
  completion documentation has no whitespace diagnostics. Frozen raw evidence
  retains its captured formatting.

No model reviews, source corrections, commits, PR submissions, or publication
were performed as part of recording this approval. Package 05 is complete with
the accepted limitations; package 06 is unblocked and has not started.

## Commit and PR preparation

On 25 October 2026, the user requested committing, pushing, and opening a PR.
The local checks passed: 18 helper/structural tests, 13 guide checks, seven
fixture checks per batch, repository and system skill validators, and all
640 manifest entries. No additional model reviews were launched.

The full staged PR diff initially failed Git whitespace checks on frozen
patch context, captured help, a raw report, and tool-schema differences.
Scoped `.gitattributes` entries preserve those captured bytes. A synthetic
Git check confirmed that captured output is accepted while trailing spaces
in authored Markdown are still rejected. Both staged commit and full PR
whitespace checks passed after the attribute change; no manifest was altered.
