# Package 04: helper tooling and validation

## Outcome

Make supporting checks trustworthy while keeping heuristic PR statistics
separate from actual code review findings.

## Deliverables and responsibilities

- Audit `scripts/pr-analyzer.py` before retaining or changing it. Decide whether
  its size statistics aid review enough to justify maintenance.
- If retained, label scores and review-time estimates as heuristics, or remove
  them. Do not turn missing changed tests or test-line ratios into automatic
  requests for changes. Documentation-only patches need no fabricated test work.
- Define supported diff input and failure behaviour. Handle or explicitly reject
  malformed, quoted-path, rename, deletion, binary, and unusual-filename cases;
  never silently present a partial parse as complete.
- Keep helpers read-only, deterministic apart from declared fields, and explicit
  about encoding and errors. Do not add network access or execute reviewed code.
- Add a small test setup for helper behaviour and structural checks. Select a
  supported Python baseline based on actual syntax and dependencies, then
  document the runnable commands. Use installed packaging/testing/lint skills
  only for the tooling actually introduced.
- Validate frontmatter, reference links, metadata consistency, and package
  completeness without tests that merely freeze prose wording.
- Add proportionate CI for those commands once they work locally. Keep repository
  settings changes outside this package unless specifically authorised.

## Tests

- Synthetic diffs: normal edits, empty input, multiple files, renames, deletions,
  binary files, spaces/Unicode/quoted paths, and malformed headers.
- Golden expected file identities and counts for supported inputs.
- Assert unsupported cases produce explicit diagnostics rather than false totals.
- Run from a directory different from the repository to expose path assumptions.
- Confirm helpers leave their inputs and target checkout unchanged.

## Human checkpoint

Review whether retained metrics add useful context and whether limitations are
visible enough to avoid confusing heuristics with verified defects.

## Exit criteria

- Retained helpers have meaningful tests and documented input limits.
- Structural validation has a portable documented command.
- Automation does not invent correctness judgements from line counts.
- Required checks pass; no live repository settings changed incidentally.
