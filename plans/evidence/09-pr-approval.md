# Package 09 conditional acceptance and PR gates

On 28 October 2026, after the audit, Miri results, and retained limits were
presented, the user requested a commit on a new branch, a PR, and the
`pr-coderabbit-loop` skill through merge completion, adding: "when the loop is
complete with no issue my approval should be inferred". The user in this chat
is the decision maker.

This supplies conditional human acceptance of the package 09 technical candidate
and its disclosed scope, including the Miri follow-up. The presented candidate
manifest was `4486081d4fa3e6cb5760a27064415ff2a9aea41d2ac726eb7dd8d95ae0d1a9cb`.
The authorisation covers verified fixes within that scope, with refreshed checks
and candidate identities. No further acceptance question is required once the
specified gates hold. It authorises the new branch, commits, push, PR creation,
review replies, thread resolution, and a guarded merge commit. It does not
authorise release, publication, a model evaluation, or changed repository rules.

Acceptance becomes effective only after a completed clean CodeRabbit review of
the current head, all inline threads resolved, every review-body finding given
a disposition and PR reply, passing required checks and approvals, and GitHub
permitting a merge commit guarded by that exact head. A skipped review or a
successful check alone does not satisfy the clean-review gate. Rule or scope
decisions still require the user's ruling.

Retain the [audit](09-go-and-rust.md) and
[Miri record](09-executable-checks/miri-verification.md) limits: pinned versions,
synthetic controlled I/O, one Miri seed/target, no complete unsafe proof,
English-only technical rewrites, and no independent review-accuracy claim.
Package 05's accepted limitations and release boundaries remain unchanged.

The branch is `codex/package-09-go-rust`, based on `main` at
`128b6a908bdeefd5a6d1a73b2fce91c5139294f6`, after package 08 merged in PR 9.
The original candidate was developed on that merge's source head; the base has
the same file tree and introduces no runtime change. The PR targets `main` in
`smiggs/code-review-skill-codex`.

The final head, finding ledger, required checks, effective acceptance, and merge
confirmation will be recorded in the PR conversation. This avoids a bookkeeping
push after the current-head clean review. Review fixes must refresh affected
validation and candidate identities before the next review.

Connected tools provide no PR event delivery. Use bounded checks during this
session and a 50-minute safety heartbeat, recording its returned identifier in
the PR conversation and deleting it after confirmed merge. No event subscription
is created. The local `gh` login is invalid; connected GitHub tools supply the
review, comment, and head-guarded merge operations. Authenticated Git push is
verified separately.
