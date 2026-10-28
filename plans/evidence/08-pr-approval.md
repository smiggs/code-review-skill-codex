# Package 08 conditional acceptance and PR gates

On 28 October 2026, after the guide corrections, executable results, and remaining
limits were presented, the user requested: “Create a PR and run” the
`pr-coderabbit-loop` skill “until completion”, adding “my approval is dependent
on Coderabbit running green”. The user in this chat is the decision maker.

This supplies conditional human acceptance of the package 08 technical candidate
and its disclosed scope. No further acceptance question is required after the
specified gates hold. The request authorises the package branch, commits, push,
PR creation, review replies, verified fixes, thread resolution, and guarded merge
under the invoked skill. It does not authorise a separate model evaluation,
publication, installation, release, or changed repository rules.

Acceptance becomes effective only when CodeRabbit has completed a clean review
of the current head, every inline thread is resolved, every review-body finding
has a disposition and reply, required checks and approvals hold, and GitHub
permits a merge commit against the verified expected head. A skipped or merely
successful check without a completed clean review is insufficient.

The [execution record](08-executable-verification.md) describes 29 passing
framework/runtime checks, three defective fixtures rejected and three controls
accepted, strict TypeScript compilation, and the compiler/runtime versions.
Retain its simulated-DOM, browser, full SFC type-checking, Next.js, integration,
translation, and independent review-accuracy limits. No new behavioural review
batch has been agreed or run, and package 05's accepted limits are unchanged.

The branch is `codex/package-08-typescript-react-vue`, based on `main` at
`29eb9c2341cd00fbc981ee394b22cc9a01180033`, after task 07's PR merged. The initial
technical candidate was developed on its parent task-07 head; updating the base
introduces no runtime change. The PR targets `main` in
`smiggs/code-review-skill-codex`.

Final head, review ledger, required checks, conditional acceptance becoming
effective, and merge evidence will be recorded in the PR conversation. This
avoids an evidence-only push after the verified clean review. Review fixes must
refresh affected validation and candidate identities; no old evaluation score
may be attached to changed runtime bytes.

PR event delivery is unavailable in the connected tools. Use bounded checks
while active and the 50-minute safety heartbeat
`package-08-coderabbit-safety-check`; remove monitoring created by this run on
completion. No event subscription was created. The local `gh` login is invalid;
use the connected GitHub tools and verify authenticated push separately.
