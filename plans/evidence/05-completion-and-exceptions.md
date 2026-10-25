# Package 05 completion with accepted exceptions

Status: complete with human-accepted limitations on 25 October 2026.
Package 06 is unblocked and has not started. This decision changes package 05's
completion requirements for the evaluated revision; neither batch passes its
original acceptance criteria retrospectively.

## Human decision and scope

The assistant proposed completing package 05 with two explicit exceptions,
preserving original scores, recording human acceptance of the evaluated
revision, and unblocking package 06. The user replied, "Yes approved".
Reviewer identity: the user in this chat; no personal name was supplied.

Accepted adapted runtime: `677beab3a37af42b08f9c46e5344b44afe84b3cf`.
Compared upstream runtime: `dcd254772fc253143889b6ab0184f31296482426`.
The [runtime inventory](05-behavioural-evaluation/batch-02/runtime-sha256.json)
pins file contents. This approval applies to that runtime and the recorded
evaluation scope. It is not approval of later runtime changes, a release,
installation, publishing, merging, or repository settings.

## Accepted exceptions

- Severity calibration remains an advisory limitation. Batch 02's adapted
  case 04 received P0 rather than the agreed P1. Its severity score stays
  failed. Human judgement remains necessary when acting on priorities;
  the approval neither establishes P0 as correct nor changes the rubric.
- The upstream comparison is incomplete. Batch 02 case 01 upstream failed
  on backend connectivity before producing a report and was not retried.
  Its scores stay unresolved with null counts. The available comparison
  supports no claim that the adapted skill is superior to upstream.

The user accepts those limits as non-blocking for package completion. No
further model review, skill correction, or priority adjudication is required
to close package 05. Any future evaluation needs its own agreed scope.

## Evidence supporting acceptance

The [batch 02 results](05-behavioural-evaluation/batch-02/execution/README.md)
record adapted detection of all four seeded defects, including both mandatory
cases, zero false positives, complete finding evidence, correct no-findings
and uncertainty handling, and no observed authority violations. Three of four
priorities match. All 20 initial contexts were audited; successful evaluators
had equivalent live tools without repository instructions, grader materials,
or prior reports. Ordinary runtime guidance remains a disclosed limit.

Both batches and the [batch 01 adjudication](05-behavioural-evaluation/runs/batch-01/adjudication.md)
remain available. Batch 01's context coupling and original severity scores are
unchanged; it is not used to establish independent behaviour. The synthetic
scope does not establish accuracy on other languages, large diffs, production
repositories, or repeated runs. No private code or secrets were supplied as
fixtures; candidate/input hashes were unchanged throughout evaluation.

The [package plan](../05-behavioural-evaluation.md) records the approved
exception to its original exit criteria. The [checkpoint rules](../human-ai-checkpoints.md)
distinguish this acceptance from an original-rubric pass. Package 06 must carry
the severity and incomplete-comparison limits into capability claims and
release evidence, alongside the existing reference and environment limits.

## Preserved score identities

- [Batch 01 scorecard](05-behavioural-evaluation/runs/batch-01/scorecard.json):
  SHA-256 `8038802e98eb258926e312b3cd4558972b649819456a9471a3e5f93ad047e0af`.
- [Batch 02 scorecard](05-behavioural-evaluation/batch-02/execution/scorecard.json):
  SHA-256 `c1a061b90e2ca28385cfba971c560058259fc89965f9402af76109795e9676e0`.

Frozen criteria, fixtures, agreements, raw reports, and output manifests remain
unchanged. Pending-status statements in frozen preparation artefacts describe
their historical stage; this completion decision supersedes package-blocking
statements in earlier records. The supporting validation for this documentation
change is recorded in the package evidence.
