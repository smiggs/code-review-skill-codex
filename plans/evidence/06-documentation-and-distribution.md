# Package 06 documentation and distribution candidate

## Status and candidate identity

Prepared on 25 October 2026. Human distribution approval is pending. At that
preparation checkpoint, no commit, push, tag, public release, ChatGPT upload,
live PR comment, or personal installation had been performed. Tests installed
a copy only under `/tmp/package-06-consumer/.agents/skills/code-review-codex`.
Subsequent installation and Git handoff are recorded below.

Source base: `f251b9b5ab9ae54187614196087d368219c79255` plus the package 06
working changes. This was an uncommitted candidate at preparation, not a Git release revision.
The exact 31 distributed files are pinned by the
[SHA-256 manifest](06-distribution/manifest.json); the
[archive record](06-distribution/archive.json) pins the ZIP bytes and entry list.
Those identities, rather than the source base alone, define this candidate.
`dist/code-review-codex.zip` is a local ignored build output, not a published asset.

Archive SHA-256:
`b10c6838941cad407a9fd1382f02316d346c3b48558bc1edbaaf4995e319e3eb`.
Archive size: 110034 bytes; 31 files under one `code-review-codex/` root.
The manifest permits byte-for-byte verification of another build even if ZIP
entry timestamps produce a different archive hash.

## Changes and provenance

Both READMEs and contribution guides now describe the implemented workflow,
permissions, real installation paths, fixed revisions, validation, and capability
limits. They install this adaptation from `smiggs/code-review-skill-codex`, not
an upstream checkout with different behaviour. Shared command examples and
installation/usage rules are aligned in Chinese; full technical guides and
historical evidence remain English only, without bilingual validation.

The bundled [provenance summary](../../reference/provenance.md) preserves upstream
links and measured scope. [Distribution guidance](../../reference/distribution.md)
covers allowlisting, fresh extraction, installation, update, rollback, and
conditional upload support. Reference status links to the bundled audit summary
instead of excluded plans. Helper documentation distinguishes development checks
from the dependency-free installed helper. The package plan, index, and root
repository instructions record the pending checkpoint.

Relative to package 05's accepted runtime
`677beab3a37af42b08f9c46e5344b44afe84b3cf`, the distributed differences are the
four companion docs, two new reference documents, and documentation-only edits
to `reference/helper-tooling.md` and `reference/reference-status.md`. `SKILL.md`,
UI metadata, contract, templates, technical guides, and helper code are unchanged.
Licence bytes match upstream `dcd254772fc253143889b6ab0184f31296482426` exactly:
SHA-256 `77e595673b752a4c6971fee076489240bf9dd76ed4286c9a5218ea4ac88d64c3`.
No additional licence or upstream-authorship claim was introduced.

## Archive verification

Built using the [documented staging procedure](../../reference/distribution.md),
with staging at `/tmp/package-06-stage` and extraction at `/tmp/package-06-check`.
A one-off independent comparison checked the exact allowlist, all extracted file
bytes against the source, absence of symlinks, ZIP CRC integrity, and the licence
against both source and upstream Git objects. All passed. The archive excludes
Git metadata, repository instructions, tests, plans, evaluation data, credentials,
caches, logs, validation dependencies, and build outputs. Every relative Markdown
file link resolves in the extracted copy; new fragment links were also inspected.

Validation environment: Linux x86_64, Python 3.12.3, Codex CLI/app-server
`0.164.0-alpha.11.1`. The repository's pinned PyYAML 6.0.3 was installed into
`/tmp/package-06-deps`; `PYTHONPATH=/tmp/package-06-deps` selected it for final
checks. No system packages or personal skills were installed. The system
interpreter's PyYAML 6.0.1 was used for initial checks, which were repeated with
the pinned dependency.

Commands exercised from the source root unless an absolute path is shown:

```bash
PYTHONPATH=/tmp/package-06-deps python3 -B -m unittest discover -s tests -v
PYTHONPATH=/tmp/package-06-deps python3 -B scripts/validate-skill.py
PYTHONPATH=/tmp/package-06-deps python3 -B scripts/validate-skill.py /tmp/package-06-check/code-review-codex
PYTHONPATH=/tmp/package-06-deps python3 -B /home/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
PYTHONPATH=/tmp/package-06-deps python3 -B /home/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py /tmp/package-06-check/code-review-codex
python3 -B plans/evidence/03-python-examples.py
python3 -B /tmp/package-06-check/code-review-codex/scripts/pr-analyzer.py --help
printf '' | python3 -B /tmp/package-06-check/code-review-codex/scripts/pr-analyzer.py --json
git diff --check
git diff --stat
```

Repository tests: 18 passed. Guide/example checks: 13 passed. Both structural
validators passed on source and extracted package. Empty helper input returned
zero files/additions/deletions. From `/tmp/package-06-consumer`, the installed
helper parsed `change.diff` as two files and three additions/three deletions,
without importing anything from the development checkout. The house-style lint
check passed on new English distribution prose. These checks establish helper,
link, and packaging properties, not independent review accuracy.

Environment failures were retained as limits rather than successful checks:
`python3 -m venv` failed because `ensurepip` is unavailable; the documented
alternative dependency installation above succeeded after sandbox network access
initially failed. Two initial app-server starts failed on read-only state paths;
a temporary SQLite root and approved runtime access allowed discovery to finish.
An initial validator batch ran from the consumer directory by mistake and failed
to locate source scripts; it was rerun from the source root. No failed attempt
is counted as a pass. Other operating systems, Python versions, client UI
selectors, and in-session hot reload were not exercised here.

## Installation smoke checks

The archive was extracted fresh, then its complete folder was copied into an
isolated synthetic repository's `.agents/skills`. App-server `skills/list`,
with `forceReload: true`, found exactly one enabled `code-review-codex` at that
path, with the intended description, UI metadata, and no discovery errors.
The [discovery record](06-distribution/discovery.json) preserves that result.
This verifies repository-scoped discovery in the tested CLI; personal-location
and automatic hot-reload behaviour are documented rather than directly tested.

The fixture combines a zero-timeout regression with a harmless local-variable
rename. It is a transparent installation smoke check, using a known package 01
example, not a blinded evaluation or a new severity-calibration batch. Both
explicit and ordinary requests use the same source snapshots and target
requirements. No private code or live PR was involved.

The first exploratory runs selected the archive skill but also read installed
house-style guidance; the ordinary run read the installed CodeRabbit skill.
They produced the expected result, but are not used to establish operation with
only this skill. The final runs disable the 27 other discovered skills only for
the test processes and ignore user configuration. They use ephemeral sessions,
read-only review commands, and `approval_policy="never"`. No model override was
set; the retained CLI event stream does not expose the backend model identifier.
These are distribution checks and do not establish context-isolated accuracy.

Both final runs completed successfully, read the archive's `SKILL.md` and bundled
review contract, reported one supported P2 zero-timeout defect, and made no
finding against the harmless rename. Each first tried unavailable `python`
(exit 127), then reproduced the behaviour with `python3` and disclosed that
fallback. Only local command tools were used, with no optional integration calls,
source changes, or external review actions. All installed bytes still match the
manifest, and all target files match the expected synthetic input bytes.

The [smoke results](06-distribution/smoke-results.json) record tool types,
command counts, fallback failures, and integrity checks. The retained
[explicit report](06-distribution/explicit-report.txt) and
[ordinary report](06-distribution/ordinary-report.txt), exact command arguments,
and event streams accompany the [fixture patch](06-distribution/fixture/change.diff).
The trace establishes these two observed runs, not a general accuracy claim. The exact prompts are
[explicit](06-distribution/explicit-prompt.md) and
[ordinary](06-distribution/ordinary-prompt.md). Neither invocation authorises
fixes, source mutation, or external services. The CLI itself requires backend
connectivity; review tool use is checked separately for optional integrations.

## Product documentation checks

The fetched [official skill documentation](https://learn.chatgpt.com/docs/build-skills),
checked on 25 October 2026, lists personal skills at `~/.agents/skills` and
repository skills at `.agents/skills`. It documents automatic change detection,
a restart fallback, and explicit CLI/IDE selectors. The READMEs distinguish
that documented behaviour from the narrower local checks above. They no longer
present the upstream clone as installation of this adaptation.

The fetched page does not establish a standalone ZIP import flow for a specific
ChatGPT account. The ZIP structure is locally verified, but importer acceptance,
account access, and script execution on ChatGPT surfaces are untested. Official
[plugin packaging](https://developers.openai.com/plugins/build/plugins) is a
separate distribution route; this archive is not a plugin. No plugin conversion,
upload, or publication is included in the candidate.

## Human checkpoint and remaining limits

Recommendation: review the manifest-pinned local candidate for package 06
acceptance. Human decision: pending. Review installation and rollback,
provenance, measured scope, Chinese companion limitations, and conditional
ChatGPT support before approving it. The plan requires a human distribution
checkpoint; this record does not invent that approval.

Package 05's accepted severity-calibration limitation and incomplete upstream
comparison remain disclosed. Original scores still include a failed priority
and an unresolved run; no superiority claim or original-rubric pass is made.
The retained unaudited references, limited environments, and synthetic evaluation
scope remain unchanged. Packaging success does not remove those limits.

After approval, a committed release candidate needs its full Git revision
recorded and its archive manifest checked against this candidate. README
`APPROVED_COMMIT` remains an explicit placeholder until an approved commit is
chosen. The local working-copy identity above is sufficient to review these
contents but is not a remotely installable published revision. Any push, tag,
publication, user installation, or live PR action needs separate authorisation.

## Subsequent installation and Git handoff

On 26 October 2026, the user authorised local installation. The user then
instructed "commit, push and open a PR",
authorising those Git actions separately. Neither instruction is recorded as
approval of the pending package 06 distribution checkpoint or public release.

Committed candidate source: `b7996cfec64ba2fde27e2dbd5c555ad3d47d70a4`, on `codex/package-06`, based on
`origin/main` at `2dfc944`. Every one of its 31 distributed files was checked
directly from the Git object against the existing manifest and matched. The
installed copy also matches. This revision makes the candidate source available
for a pinned checkout after the authorised push; it is not an approved release.
The following evidence-only commit records this source identity without changing
the distributed files, ZIP, or installation. The preparation snapshot and its
base revision remain above as historical evidence.

## Conditional completion approval

On 26 October 2026, the user requested the full CodeRabbit loop through merge
and stated that it is approved once successfully complete. Reviewer identity:
the user in this chat; no personal name was supplied. This supplies conditional
package 06 approval and authorises PR replies, fixes, thread resolution, and a
merge commit for PR 6 after the loop's gates pass. No further approval question
is required if those conditions hold. It does not authorise a tag, public
release, plugin publication, or ChatGPT upload.

The conditions are a completed clean CodeRabbit review for the final head, all
inline threads resolved, review-body findings disposed of with PR replies,
passing checks, and a mergeable PR with no blocking rule or open decision.
The final head, clean review, checks, disposition ledger, and merge result will
be recorded in the PR conversation when the conditions hold. This conditional
decision supersedes the earlier request for a separate distribution approval;
it does not relabel any package 05 score or widen the tested scope. The
manifest-pinned archive remains the checked preparation snapshot.
