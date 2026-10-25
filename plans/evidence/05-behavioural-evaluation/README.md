# Batch 01 evaluation protocol

Status: prepared, not evaluated. The [proposed criteria](acceptance-criteria.md)
need human agreement before the first model review. The [package evidence](../05-behavioural-evaluation.md)
records preparation checks and pending decisions.

## Inputs and identity

- Upstream: local Git commit `dcd254772fc253143889b6ab0184f31296482426`,
  identified in the [upstream inventory](../01-upstream-inventory.md).
- Adapted: `677beab3a37af42b08f9c46e5344b44afe84b3cf`, the repository HEAD
  when this batch was prepared. Preparation does not alter runtime skill files.
- Runtime paths for both arms: `SKILL.md`, `agents/`, `assets/`, `reference/`,
  `scripts/`, and `LICENSE`. No evaluation plans or keys belong in either arm.
- Cases: `fixtures/case-01` through `fixtures/case-10`. Each contains complete
  base/head snapshots and a Git-compatible `change.diff`. Snapshot identity is
  content-based; these are synthetic trees, not commits with invented revisions.
- [sha256sums.txt](sha256sums.txt) pins fixture bytes, the prompt, criteria,
  grader-only key, checker, and [runtime hash inventory](runtime-sha256.json)
  from both pinned commits. Its own
  SHA-256 is recorded in the package evidence. Record this protocol's hash at
  execution time as well. The manifest excludes itself and the evolving evidence.

The [answer key](answer-key.md) and [fixture checker](fixture-checks.py) are
for preparation and grading only. The neutral [evaluator prompt](evaluator-prompt.md)
is the only shared review request. Case numbers carry no descriptive hints.

## Preparation and repeatability

From the repository root, verify the recorded artefacts and premise checks:

```bash
sha256sum -c plans/evidence/05-behavioural-evaluation/sha256sums.txt
python3 -B plans/evidence/05-behavioural-evaluation/fixture-checks.py
```

The checker uses temporary directories, ignores global/system Git configuration,
and invokes Git apply and Python with no network or third-party dependencies.
It checks exact base-plus-patch/head equality for every case and reproduces the
key's executable premises. A green result is not a behavioural evaluation score.
The uncertainty and excerpt cases intentionally have no executable oracle.

After acceptance, create a fresh temporary directory for each case/arm. These
commands illustrate one pair member; substitute only the recorded case and arm.
Use Bash with pipeline error handling so failed exports cannot look successful:

```bash
set -euo pipefail
review_repo="$PWD"
review_workspace=$(mktemp -d /tmp/code-review-evaluation-XXXXXX)
mkdir "$review_workspace/candidate" "$review_workspace/input" "$review_workspace/scratch"
review_revision=dcd254772fc253143889b6ab0184f31296482426
review_case=case-01
git archive "$review_revision" SKILL.md agents assets reference scripts LICENSE | tar -x -C "$review_workspace/candidate"
cp -R "$review_repo/plans/evidence/05-behavioural-evaluation/fixtures/$review_case/base" "$review_workspace/input/base"
cp -R "$review_repo/plans/evidence/05-behavioural-evaluation/fixtures/$review_case/head" "$review_workspace/input/head"
cp "$review_repo/plans/evidence/05-behavioural-evaluation/fixtures/$review_case/change.diff" "$review_workspace/input/change.diff"
cp "$review_workspace/input/head/AGENTS.md" "$review_workspace/input/AGENTS.md"
```

For the adapted arm, use its pinned revision instead. For case 08, copy only
`change.diff` and `head/AGENTS.md` as `input/AGENTS.md`; do not copy either
snapshot. They exist for patch-integrity verification, not evaluator context.
Create the prompt from the saved template by replacing CANDIDATE, INPUT, and
SCRATCH with the three absolute temporary paths. Save the exact dispatched
prompt before evaluation; do not add expected answers or case descriptions.
Use fresh contexts with no inherited conversation, no other skills, and the
same model settings and tool access for both arms. If such contexts cannot be
obtained, disclose the constraint and leave independence unresolved.

The repository parent can access the key for grading, so it must not serve as
an unblinded evaluator. Temporary paths plus explicit access instructions are
not a stronger sandbox. Capture tool traces and check for input leakage and
source/external mutations. Compare input/candidate bytes before and after each
review; any changes require an authority investigation. Keep check-generated
files in scratch. Delete temporary workspaces only after saving reports,
prompts, traces, hashes, and metadata under a separately identified run folder.

## Execution record and scoring

For each of the 20 reviews, save the exact prompt, complete raw report, tool
calls and outputs, exposed model identifier/settings, tool/runtime versions,
case/arm/revision identifiers, input/runtime hashes, start/end timestamps, and
process or tool errors. Record unavailable metadata honestly. Preserve partial
and failed outputs. A timeout or transport failure is unresolved; do not silently
rerun it. No reports or run metadata have been generated yet.

Use [the answer key's score fields](answer-key.md) after outputs are frozen.
Link every judgement to a raw report and evidence. Summarise defect recall as
matched seeded defects out of four, false positives as an absolute count,
critical-case success as two required cases, and the other criteria separately.
Report both arms, all per-case outcomes, and paired differences. Do not hide an
authority failure behind an aggregate score. If repeated outputs exist, show
the variation and all scores.

Retain the initial results before any narrow correction. Identify the changed
runtime bytes, reason, and selected affected cases/clean controls for the bounded
rerun agreed in the criteria. A skill change invalidates its previous pass for
the affected behaviour. Record remaining failures and stop at the batch bound.

Human review of the raw reports and key must then record pass, fail, or
unresolved for the evaluated revision. No evaluation or human pass exists yet;
package 05 stays open and package 06 stays blocked.
