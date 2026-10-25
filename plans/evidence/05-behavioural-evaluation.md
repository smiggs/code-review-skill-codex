# Package 05 preparation and decision record

Current status: the initial 20 reviews are finished following criteria agreement.
The [batch results](05-behavioural-evaluation/runs/batch-01/README.md) record
complete defect detection and no false positives in both arms, two adapted
severity mismatches, and unresolved evaluator independence. No human pass is
recorded; package 05 remains open and package 06 remains blocked. The preparation
sections below retain their historical status at the time they were written.

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
