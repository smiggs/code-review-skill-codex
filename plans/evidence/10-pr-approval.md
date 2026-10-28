# Package 10 conditional acceptance and PR gates

On 28 October 2026, after the audit, verification results, fixtures, and
retained limits were presented, the user requested following the
`pr-coderabbit-loop` skill "through to merger" and added that their approval
is conditional on completion. The user in this chat is the decision maker.

This supplies conditional human acceptance of the package 10 technical
candidate and its disclosed scope. The presented candidate is identified by the manifest committed in
[the results directory](10-executable-checks/results/candidate-manifest.json)
covering the guide, checklist, disposition, provenance, plan documents,
harness, fixtures, and result records; its combined digest at the final
reviewed head is stated in the PR conversation. The first package 10 commit
carried the pre-rebase manifest `08bc6149e62b710d6eaa7fb9d6754c8c74e85ed248afa3a40e361c776813746e`;
rebase-era digests are superseded rather than retained here.
The authorisation covers verified fixes within that scope, with refreshed
checks and candidate identities. It authorises the new branch, commits,
push, PR creation, review replies, thread resolution, and a guarded merge
commit. It does not authorise release, publication, a model evaluation, or
changed repository rules.

Acceptance becomes effective only after a completed clean CodeRabbit review
of the current head, all inline threads resolved, every review-body finding
given a disposition and PR reply, passing required checks and approvals, and
GitHub permitting a merge commit guarded by that exact head. A skipped
review or a successful check alone does not satisfy the clean-review gate.
Rule or scope decisions still require the user's ruling.

Retain the [audit](10-java.md) limits: pinned JDK 17.0.21/21.0.13, Hibernate
6.4.10.Final, H2 2.2.224, Spring Framework 6.1.14 baselines; synthetic H2 and
plain Spring contexts; no Spring Boot autoconfiguration or other providers;
English-only technical rewrites; and no independent review-accuracy claim.
Package 05's accepted limitations and release boundaries remain unchanged.

The branch is `codex/package-10-java`, originally based on `main` at
`118253c2ad794925417761fd7f95396bdb682539`. Package 13's plan (PR 11)
merged during preparation; the branch is rebased onto the current `main`
before the PR so the base carries it. The PR targets `main` in
`smiggs/code-review-skill-codex`.

The final head, finding ledger, required checks, effective acceptance, and
merge confirmation will be recorded in the PR conversation. This avoids a
bookkeeping push after the current-head clean review. Review fixes must
refresh affected validation and candidate identities before the next
review.

Connected tools provide no PR event delivery in this session. Bounded
status checks run during this session; no background monitoring continues
after the session ends, and no event subscription is created. The `gh`
login is authenticated for `smiggs`, so review, comment, thread, and
head-guarded merge operations run through it.
