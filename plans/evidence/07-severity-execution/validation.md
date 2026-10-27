# Task 07 execution validation

Checked on 27 October 2026. These results validate local tooling and evidence
consistency; they do not establish review accuracy beyond the recorded sample.
No additional model review was used for validation.

| Check | Actual result and retained evidence |
| --- | --- |
| Live-baseline comparator, test-first | Initial import fails because the module does not exist; after implementation all five tests pass. `continuation-comparison-red.txt` and `continuation-comparison-green.txt` retain both stages. |
| `python3 -B -m unittest discover -s tests -v` | All 18 tests pass; `repository-tests.txt` retains output. |
| `python3 -B plans/evidence/03-python-examples.py` | All 13 checks pass; `guide-examples.txt` retains output. |
| Six fixture premise tests | Passed during frozen preparation; fixtures/candidate were unchanged and their approved hashes rechecked before each launch. They were not rerun to select model labels. |
| Repository structural validator | Final structure/local-link checks pass after adding this validation record. An earlier check correctly reported this then-missing linked file; no earlier failure is represented as a pass. |
| Candidate structural validator | Pass; assessed snapshot remains unchanged. |
| System skill-creator quick validator | Pass on repository and candidate. |
| British house-style linter | Zero errors/warnings on edited plans, audit record, execution README, completion proposal and this record. |
| Frozen manifests | Original preparation, first-attempt outputs, continuation proposal and complete raw/setup outputs all verify. Candidate matches the working runtime. |
| Whitespace/stat inspection | Tracked diff checks run; authored new Markdown/Python checked separately. Raw outputs, standard unified-diff blank context markers and inherited copied Qt-guide whitespace are preserved. |

Each of six slots has exactly one actual session and one report. All actual
models/reasoning settings match approval; remaining live contexts and sandbox
settings pass the amended audit. Case 01's original context audit remains
unresolved, not changed into a pass. All candidate/input before/after hashes
match and all temporary login symlinks were removed. Forty recorded shell
commands include six unavailable-rg events, resolved with local fallbacks.
No reviewer external access, delegation, source edit or approval was observed.

Raw-output manifests were frozen before their corresponding scoring. Derived
final scores and the proposed human disposition are outside the raw manifests.
No frozen input, first-attempt report/score, or historical package 05 artefact
was edited. No installed personal skill, publication or repository setting
was changed. Final human acceptance remains pending.
