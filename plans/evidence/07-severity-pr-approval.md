# Task 07 conditional acceptance and PR gates

On 27 October 2026, after the six-review results and completion proposal were
presented, the user requested: “commit and push open a PR and follow” the
`pr-coderabbit-loop` skill, adding “Once Code Rabbit has completed it's reviews
the changes are approved”. Reviewer identity: the user in this chat; no personal
name was supplied.

This supplies conditional human acceptance of the
[proposed disposition](07-severity-execution/completion-proposal.md), exact
assessed candidate and retained limitations. No further acceptance question
is required after the specified PR gates hold. The request authorises commits,
pushes, PR creation, CodeRabbit replies, verified fixes, thread resolution and
merge under the invoked skill's gates. It does not authorise another model
diagnostic, installation, publication, changed repository rules or a release.

## Accepted result and condition

Retain the general priority clarification and close task 07 when the current PR
head has completed a clean CodeRabbit review, all inline threads are resolved,
all review-body findings have a recorded disposition and reply, required checks
and approvals hold, and the PR merges under repository rules with an atomic
head guard. No AI review overrides an unresolved repository or user decision.

The assessed candidate manifest SHA-256 is
`64915ca703ad8bfef44fd31757ac54bb795e0d3991049ed243ae1c3b4b436bbc`.
The [disposition manifest](07-severity-execution/disposition-sha256sums.txt)
SHA-256 is `dd5b007bbc13447e7651d4eb245ee8fe5158480834babbba2ae5be0bfc79bd70`.
It fixes the completion proposal, scores and supporting evidence. Original
package 05 scores and acceptance exceptions remain unchanged.

Four seeded defects and all four priorities match; both clean controls pass;
zero unsupported findings are observed. Case 01's original isolation gate
remains unresolved, and the original all-criteria result remains not passed.
The other five contexts match the explicitly accepted live baseline. Human
acceptance retains this limitation rather than relabelling it. No claim of
systematic calibration, causal improvement, or a repaired CLI preview follows.

If a PR fix changes assessed runtime material, identify the changed candidate
and obtain any required scope decision instead of attaching old diagnostic
scores to new bytes. Evidence-only corrections must preserve frozen reports,
inputs, manifests, prior scores and the recorded limitations.

## PR preparation and final evidence

The branch is `codex/task-07-severity-calibration`, based on `main` at
`1bc100147099d08e7ad7189d766c4f8f6ff07d8f`. The PR targets `main` in
`smiggs/code-review-skill-codex`. Final review/head/check and merge evidence
will be recorded in the PR conversation when all gates hold. This avoids a
post-review bookkeeping push that would invalidate the verified head.

The existing evidence whitespace policy is extended to three narrowly scoped
task 07 patterns: unified fixture patches, captured CLI help and the initial
red-test output. The unchanged candidate is stored in a byte-verified archive
after CodeRabbit reported its 300-file limit; see the
[storage record](07-severity-execution/archive-storage.md).
This preserves manifest-pinned bytes while retaining normal checks on authored
prose and code. It changes no frozen candidate or raw evidence.

PR-event delivery is unavailable through the connected tools. Use bounded
checks during the active session and one 50-minute safety-net heartbeat,
removing monitoring created by this run when finished. This does not promise
background monitoring after cleanup. The local GitHub CLI login is invalid;
use the connected GitHub tools for supported operations and verify transport
separately. No credentials are copied into the repository.
