# Package 08 CodeRabbit fixes

Date: 28 October 2026. PR: [9](https://github.com/smiggs/code-review-skill-codex/pull/9).
Reviewed head: `8b291d656db9f2e4acfd6a624ae519b47f31b1e9`.

Review `PRR_kwDOVN2iy88AAAABUorBhg` posted one actionable inline finding,
comment `4398413724`, thread `PRRT_kwDOVN2iy86xCc1q`, in `sensitivity.mjs`.
Its review-body prompt repeats that finding; it contains no additional
outside-diff defect or scope decision.

## Recorded-evidence overwrite

Verified defect. Routine `pnpm sensitivity` wrote run-dependent TAP durations
into the recorded red/green evidence and invalidated the candidate manifest.
The [red regression output](08-executable-checks/results/review-integrity-red.txt.gz)
shows an assertion failure because routine execution changed `green-react.txt`.
The reproduction runs the real runner in a temporary workspace, preserving the
original repository evidence.

The fix creates ignored `.generated/results/` and writes routine red/green
output there. The recorded `results/` files and candidate manifest are untouched
by routine runs. Preparing new evidence remains an explicit maintainer action.
A regression checks every recorded file remains byte-identical and verifies
fresh expected-failure and clean-control output exists under the generated path.

The [green suite](08-executable-checks/results/review-integrity-green.txt)
passes all 30 tests, including the original 29 framework/runtime checks and the
new preservation check. The [sensitivity rerun](08-executable-checks/results/review-sensitivity.txt)
rejects all three defective heads and accepts all three clean bases. Guide code,
original evidence bytes, fixtures, compiler/runtime dependencies, review-accuracy
limits, and the user's conditional gates remain unchanged. Documentation and
structural checks are repeated before pushing.

This preparation explicitly refreshes the candidate manifest to identify the
changed harness, documentation, new regression, and new evidence. It does not
rewrite the previous recorded red/green results. The fix commit, successful
thread reply/resolution, fresh review, and merge gates are recorded in the PR
conversation so no post-review bookkeeping push invalidates a clean head.
