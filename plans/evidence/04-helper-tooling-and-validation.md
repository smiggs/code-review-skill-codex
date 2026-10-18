# Package 04 evidence: helper tooling and validation

Date: 18 October 2026.
Status: implementation prepared; human retention decision and remote CI result
pending. Package 04 is not recorded as approved or complete.
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

## Outstanding checkpoint and limits

Human judgement remains pending on whether the counts-only helper is useful
enough to retain and whether its limitations are sufficiently visible. No human
approval is inferred from the request to begin this package.

The first GitHub run passed the tests and structural checks on both matrix
legs, then failed the whitespace step; see the CI follow-up below. The installed CI hygiene scanner
passed, but zizmor and actionlint were unavailable locally. No private code,
live pull-request mutation, approval, merge, or repository settings change was
used for evaluation. Structural and helper tests do not establish independent
review accuracy; that remains package 05 work.

## Candidate identity

Implementation fingerprint: `ad3bb12dcc3f8d3fce0dd0247b6d664c46f7ec40489aa62316623da0a530cf8f`.
This is SHA-256 over sorted file entries changed from the recorded base revision, each
encoded as path, NUL, lowercase SHA-256 of file bytes, and newline. The evidence
file itself is excluded to avoid a self-reference; all other changed files
reported by `git diff --name-only 4e1366f72ec6f494ef5ae4120e14621c00c16e97` are included. Refresh this
fingerprint and relevant checks after implementation changes.

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
commit on pushes, without modifying inherited guide content. The pending human
retention checkpoint is unchanged. A fresh GitHub run is required after push.
