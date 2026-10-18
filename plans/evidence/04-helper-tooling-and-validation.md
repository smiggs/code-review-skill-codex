# Package 04 evidence: helper tooling and validation

Date: 18 October 2026.
Status: complete. The user approved and merged PR 3 on 18 October 2026.
Final PR head: `bdea4cda918236d88bb1da3f26f4cbc2f5dd80ba`.
Merged revision: `e5c3a103f4ccc80f4d2e570a79f3c9f76e3712d0`.
CI passed on the merged revision for both Python matrix jobs and the final gate.
Base revision: `4e1366f72ec6f494ef5ae4120e14621c00c16e97`.

## Audit and recommendation

The inherited helper counted leading `+`/`-` characters without validating hunk
boundaries, excluded changed lines beginning with `+++`/`---`, retained quoted
path escapes as filename text, and accepted malformed or partial input. Its
complexity score included a test-line ratio and its suggestions could request
tests before approval based only on changed-line counts. Empty input was an
error, and file/decoding failures could produce tracebacks.

AI recommendation: retain optional file identities and text-line counts as
navigation context, remove all scores, review-time estimates, classifications,
risk factors, and review recommendations. This is an intentional divergence
from the upstream helper, preserving its CLI filename and existing flags but
replacing its report format and internal Python API. Licence and attribution
files remain unchanged. The helper is not required for a review.

The [input contract](../../reference/helper-tooling.md) defines supported cases,
explicit rejection, binary-count limits, UTF-8 handling, and the distinction
between parse validity, patch applicability, completeness, and review accuracy.
It also records structural-validator limits and portable setup commands.
English and Chinese README/contribution additions describe the same behaviour;
the detailed contract is English only, with that translation limit stated.

## Implementation and validation

- `scripts/pr-analyzer.py`: deterministic counts and JSON; exact hunk accounting,
  consistent file markers, quoted paths, rename/copy/mode metadata, binary
  summaries, empty input, and explicit errors without partial stdout.
- `tests/test_pr_analyzer.py`: synthetic expected identities/counts, CLI errors,
  missing/invalid input, alternate working directory, repeatability, and a real
  temporary Git checkout with unusual paths and unchanged file snapshots.
- `scripts/validate-skill.py` and `tests/test_validate_skill.py`: safe YAML and
  duplicate-key checks, metadata identities/types, package completeness, and
  local Markdown link targets, including negative controls and code examples.
- `requirements-dev.txt`: PyYAML 6.0.3 for structural checks; helper and test
  runner use the standard library. Python 3.10 is the exercised baseline.
- `.github/workflows/ci.yml`: Ubuntu 24.04, Python 3.10/3.14 matrix, read-only
  token, disabled persisted checkout credentials, pinned actions, bounded jobs,
  PR/push/merge-group triggers, and a final success check that rejects skipped,
  failed, or cancelled validation. No packaging, lint/type gates, publishing,
  or repository settings changes were introduced.

TDD evidence: the initial helper test run failed with 15 failures and two errors,
including incorrect header-like content counts, quoted identities, acceptance
of malformed input, and missing JSON behaviour. The first structural run failed
because the validator did not exist; valid-fixture cases then failed until the
implementation met the metadata contract. An additional inline-code fixture
reproduced a false link error before the checker was corrected. The temporary
Git fixture initially allowed identical contents to make rename identity
ambiguous; distinct fixture contents corrected that test expectation.

Local runtime: Python 3.10.12 on Linux; Git and PyYAML 6.0.3. The machine's system
PyYAML 5.4.1 also passed the early tests, but is not the pinned validation setup.
Fresh `venv` creation failed because the host lacks `ensurepip`; the exact pinned
wheel was instead installed under `/tmp/code-review-package04-deps`, with
`PYTHONPATH` set for validation. No system Python packages were changed. The
standard `venv` procedure remains documented for machines with that module.

Local commands and outcomes:

- `PYTHONPATH=/tmp/code-review-package04-deps python3 -B -m unittest discover -s tests -v`:
  17 tests passed; the entire suite also passed from `/tmp` with an absolute
  discovery path.
- `PYTHONPATH=/tmp/code-review-package04-deps python3 -B scripts/validate-skill.py`:
  package structure and local link targets passed, including from `/tmp`.
- `PYTHONPATH=/tmp/code-review-package04-deps python3 -B plans/evidence/03-python-examples.py`:
  13 standalone example/consumer tests passed.
- System skill-creator `scripts/quick_validate.py .`: passed; structural evidence
  only, not review-quality evidence.
- Python CI skill `scripts/check_workflows.py --repo .`: zero errors and warnings.
- `git diff --check` and `git diff --stat`: checked. The tracked diff statistic
  excludes added untracked files until staging; those files were inspected
  separately with `git status --short`. A smoke parse of the full tracked
  working diff matched `git diff --numstat`: nine files, 255 additions, and
  354 deletions at the time of the check.

The workflow action pins were resolved from official release pages:
[checkout v4.2.2](https://github.com/actions/checkout/releases/tag/v4.2.2) and
[setup-python v5.6.0](https://github.com/actions/setup-python/releases/tag/v5.6.0).
The YAML dependency version was checked against
[PyYAML on PyPI](https://pypi.org/project/PyYAML/6.0.3/).

## Human decision and completion

Checkpoint: package 04 helper retention and visibility of limitations.
AI recommendation: retain the optional counts-only helper with the documented
input limits and no correctness or approval recommendations.
Human decision: approved. On 18 October 2026, the user stated "approved and
merged, refresh main" after reviewing the fixes, then instructed the assistant
to complete the record and push it to `main`. This approves the retained helper
and documented scope. No separate rationale or reviewer name was supplied.

[PR 3](https://github.com/smiggs/code-review-skill-codex/pull/3) merged the final
reviewed head `bdea4cd` into `main` as `e5c3a10`. The
[final PR CI run](https://github.com/smiggs/code-review-skill-codex/actions/runs/39140977891)
and the [merged main CI run](https://github.com/smiggs/code-review-skill-codex/actions/runs/39141672235)
both passed Python 3.10/3.14 validation and `all-checks-passed`. The two Minor
CodeRabbit comments were fixed; the inline thread was replied to and resolved.

All package 04 exit criteria are met:

- The retained helper has expected-count, error, read-only, unusual-path, and
  Git-configuration regression checks, with supported and rejected inputs documented.
- Structural validation has a portable setup and runnable command.
- Statistics produce no correctness judgements or automatic approval requirements.
- The final checks pass, and no repository settings were changed.

No package 04 implementation work remains. Package 05 must separately evaluate
review behaviour; approval of this package does not approve review accuracy or
distribution.

## Remaining limitations

The first GitHub run passed the tests and structural checks on both matrix
legs, then failed the whitespace step; see the CI follow-up below. The installed CI hygiene scanner
passed, but zizmor and actionlint were unavailable locally. No private code,
live pull-request mutation, approval, merge, or repository settings change was
used for evaluation. Structural and helper tests do not establish independent
review accuracy; that remains package 05 work.

## Approved implementation identity

Approved implementation fingerprint: `d89f22d27235974e29237bf428ef5ab39ebda0d65a28e2b3248eed2bce3bca61`.
This is SHA-256 over sorted file entries changed from the recorded base revision, each
encoded as path, NUL, lowercase SHA-256 of file bytes, and newline. The evidence
file itself is excluded to avoid a self-reference; all other changed files
reported by comparing base `4e1366f` with approved PR head `bdea4cd` are
included. This identifies the approved snapshot before the documentation-only
completion-record update. Refresh the relevant evidence after implementation
changes.

## CI follow-up for PR 3

The initial [CI run](https://github.com/smiggs/code-review-skill-codex/actions/runs/39139926954)
failed both validation jobs at `git show --format= --check HEAD`. Checkout's
single-commit shallow boundary made Git compare the whole tree as a root commit,
reporting two inherited trailing spaces in `reference/qt.md`. The tests and
structural checks passed on Python 3.10.22 and 3.14.8 in that run.

A temporary local clone with `--no-local --depth 1` reproduced exactly those two
errors. Fetching depth 2 and running `git diff --check HEAD^ HEAD` passed. The
workflow now explicitly fetches two commits and checks the first-parent diff.
This preserves whitespace checking for the PR merge's changes and for the tip
commit on pushes, without modifying inherited guide content. The corrected
[GitHub run](https://github.com/smiggs/code-review-skill-codex/actions/runs/39140102654)
passed both Python matrix jobs and `all-checks-passed` for commit `db0d219`.

## CodeRabbit review follow-up

Both Minor comments on PR 3 were verified against commit `db0d219`. The Git
fixture inherited contributor configuration: forced diff colours, disabled
rename detection, and required signing each caused a reproducible failure while
the clean control passed. A permanent regression test reproduced all three
failures before the fix. Fixture Git commands now ignore global/system Git
configuration and disable terminal prompts; all three configurations pass.
`AGENTS.md` now describes the helper's optional file and text-line counts.

The updated helper/structure suite passes all 18 tests on Python 3.10.12 with
PyYAML 6.0.3. Structural/link validation, the system skill-creator validator, and
`git diff --check` pass. Package 03 material is unchanged. No review accuracy
claim is inferred from these corrections. The subsequent PR and merged-main
CI runs passed; the human decision is recorded above.
