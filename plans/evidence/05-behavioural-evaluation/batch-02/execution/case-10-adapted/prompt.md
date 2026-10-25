Use only the review skill at /tmp/review-batch02-b_8auotx/candidate to review the supplied change in /tmp/review-batch02-b_8auotx/input.
Read that skill's SKILL.md and selectively load its relevant supporting files.
Do not substitute another installed review skill.

Read /tmp/review-batch02-b_8auotx/input/AGENTS.md for the target's instructions. If base/ and head/ are
present, compare those snapshots using change.diff and inspect relevant
surrounding code, including unchanged callers. Otherwise only the supplied
patch is available. Report actionable introduced or newly exposed defects and
material verification limits. This is an advisory change review.

You may read only /tmp/review-batch02-b_8auotx/candidate, /tmp/review-batch02-b_8auotx/input, and standard local tool documentation.
Use local file inspection, Git, and Python standard-library checks as needed.
Run any checks in /tmp/review-batch02-b_8auotx/scratch, copying inputs there first. Do not modify /tmp/review-batch02-b_8auotx/candidate
or /tmp/review-batch02-b_8auotx/input. Do not use network services, other repository paths, answer keys,
evaluation criteria, other cases, or previous reports. Do not fix source,
commit, post comments, submit reviews, approve, merge, or change settings.

Return your complete review report, including scope and checks actually run.
Record commands and outcomes accurately; static inspection is permitted.
