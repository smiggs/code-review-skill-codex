# Preparation validation

Checked on 27 October 2026 on Python 3.14.4. No inference, authentication,
production operation, or model-priority assessment ran.

| Check | Actual result |
| --- | --- |
| `python3 -B plans/evidence/07-severity-diagnostic/check-fixtures.py` | Six tests pass; intended defective heads, base outputs, bounded consequences, workarounds and controls checked in scratch copies. |
| `python3 -B plans/evidence/07-severity-diagnostic/preparation/verify-inputs.py` | All six patches apply and produce byte-identical head trees; six premise tests pass; candidate/input hashes unchanged before and after. See `preparation/input-integrity.json`. |
| `python3 -B -m unittest discover -s tests -v` | All 18 repository tests pass; raw output in `preparation/repository-tests.txt`. |
| `python3 -B plans/evidence/03-python-examples.py` | All 13 guide-example checks pass; raw output in `preparation/guide-examples.txt`. This does not establish independent review accuracy. |
| `python3 -B scripts/validate-skill.py` | Repository structure and local link targets pass. |
| Same validator with `plans/evidence/07-severity-diagnostic/candidate` | Candidate structure and local link targets pass. |
| System skill-creator `scripts/quick_validate.py` on repository and candidate | Both pass. |
| British house-style linter | Zero errors and warnings on new/edited English Markdown outside the copied candidate. |
| Whitespace and diff inspection | Tracked diff checks pass. New-file checks/counts retain eight data/guide exceptions, detailed below and in `preparation/diff-validation.json`. |
| Candidate consistency | Every candidate file equals its corresponding working source; the only runtime difference from the audited base is the agreed contract paragraph. |

Eight new-file paths emit preserved-data warnings: the unchanged Qt guide (two
inherited spaces), four unified patches (required blank context markers), and
three raw CLI/test outputs. No authored prose/code whitespace warnings remain;
raw outputs are unchanged.

The test-first red record contains missing-fixture errors, not an assertion that
model behaviour failed. Original batch artefacts and the installed personal
skill remain untouched. Structural checks and green fixture checks do not
establish calibration, reliability, or improvement. The run and final human
checkpoints remain pending.
