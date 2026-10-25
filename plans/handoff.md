# Package 05 handoff

Recorded on 25 October 2026 for branch `codex/package-05`.

## State to resume

The initial behavioural evaluation is finished and scored. Package 05 remains
open because severity calibration has two mismatches and evaluator independence
is unresolved. No human quality pass is recorded; package 06 remains blocked.
The reusable skill has not been changed in response to these results.

The user agreed the acceptance criteria before evaluation, then requested
"Record the scoring only" to conserve the usage window. The subsequent request
is to preserve the work and these next steps on this branch. Do not launch
further reviews or reruns as part of this handoff.

## Evidence to read

- [Package 05 plan](05-behavioural-evaluation.md): deliverables and exit criteria.
- [Package evidence](evidence/05-behavioural-evaluation.md): preparation,
  agreement, execution status, and outstanding human decisions.
- [Batch 01 results](evidence/05-behavioural-evaluation/runs/batch-01/README.md):
  paired results, raw-report links, context audit, and stopping point.
- [Scorecard](evidence/05-behavioural-evaluation/runs/batch-01/scorecard.json):
  all 20 report scores, rationale, and exact excerpts.
- [Accepted criteria snapshot](evidence/05-behavioural-evaluation/acceptance-criteria.md)
  and [agreement](evidence/05-behavioural-evaluation/runs/batch-01/agreement.json).
- [Grader-only answer key](evidence/05-behavioural-evaluation/answer-key.md):
  keep this and previous reports out of evaluator context.
- [Review contract](../reference/review-contract.md): approved severity and
  evidence definitions for adjudication.

The frozen protocol and criteria still contain preparation-time pending-status
statements. Preserve their bytes: the agreement and execution records supersede
those historical statements. The fixture manifest and execution manifest pin
inputs and raw outputs separately from subsequent scoring documents.

## Recorded results

The batch used ten synthetic cases with two skill arms, for 20 fresh-context
reviews. Both arms used `gpt-6.1-sol`, medium reasoning, CLI
`0.163.0-alpha.10.2`, and equivalent tools. There were no repeat reviews or
corrective runs.

| Measure | Upstream | Adapted |
| --- | --- | --- |
| Seeded defects detected | 4/4 | 4/4 |
| Mandatory recovery and unchanged-caller cases detected | 2/2 | 2/2 |
| Unsupported defect findings | 0 | 0 |
| Severity matches | Two unmapped blocking labels; two mismatches | 2/4; two mismatches |
| No-findings and scope handling, cases 05–10 | 6/6 | 6/6 |
| Evaluator independence | Unresolved | Unresolved |

Both skills assigned P1 to case 03's retention normalisation and case 04's
broken status rendering; the agreed rubric requires P2 for both. Those are
severity disagreements, not missed defects or demonstrated new runtime
regressions in the adapted skill. The original scores must remain available.

Despite `fork_turns=none`, the runtime automatically injected this repository's
`AGENTS.md` into every evaluator context. That shared guidance contains review
rules resembling the adapted contract. No answer key or prior conclusions were
in the inherited user context, and evaluators respected the intended file-access
boundaries. However, the comparison cannot establish behaviour without global
review guidance or attribute upstream restraint solely to its skill.

## Next steps, in order

1. Obtain human adjudication of the case 03 and 04 reports against the approved
   severity contract and the accepted rubric.
2. Record whether each disagreement indicates faulty skill guidance, an
   ambiguous fixture, or an overly rigid expected priority.
3. Prepare evaluator isolation outside this repository's instruction scope.
4. Inspect the initial evaluator context before supplying any review case.
5. Make a narrow runtime correction only if adjudication establishes a skill
   defect supported by the evidence.
6. Agree the scope and immutable criteria for a separately identified isolated
   batch before running further model reviews.
7. Record the resulting human pass, fail, or unresolved decision against the
   exact evaluated revision.

If adjudication changes a fixture or expected severity, retain batch 01 and
freeze the revision before evaluation; do not silently change its scores or
relax its thresholds after observing the outputs. Avoid adding special-case
skill rules solely to force the expected P2 answers.

Isolation affects the entire comparison. A complete isolated repeat requires
20 reviews, exceeding the accepted correction bound of at most six adapted
reviews in one narrow batch. That full repeat therefore needs separate
agreement. The six-review allowance has not been used. Package 06 cannot start
until package 05's exit criteria and human checkpoint are satisfied.

## Revisions and validation

Upstream runtime: `dcd254772fc253143889b6ab0184f31296482426`.
Adapted runtime: `677beab3a37af42b08f9c46e5344b44afe84b3cf`.
Per-file hashes, exact prompts, raw reports, tool calls, command outputs, and
before/after input hashes are saved in the evidence. Temporary paths in reports
may not survive; recreate inputs from the pinned revisions and fixtures.

Recorded preparation checks passed: seven fixture checks, 18 existing helper
and validator tests, 13 guide checks, structural/link validation, and the system
skill-creator validator. Both evidence manifests were subsequently verified:
60 preparation files and 122 execution artefacts matched. Candidate and input
bytes were unchanged in all 20 evaluator workspaces. These supporting checks
are separate from behavioural scores and human acceptance.

For documentation changes, use structural/link validation, house style lint,
and Git whitespace/stat checks. Three fixture patch files intentionally contain
single-space blank context lines; preserve those manifest-pinned bytes.
No additional evaluation is needed to validate this handoff document.
