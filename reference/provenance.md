# Provenance and measured scope

## Attribution and divergence

This adaptation is maintained in
[smiggs/code-review-skill-codex](https://github.com/smiggs/code-review-skill-codex).
Its upstream is
[NefelibataBIGR/code-review-skill-codex](https://github.com/NefelibataBIGR/code-review-skill-codex),
recorded at `dcd254772fc253143889b6ab0184f31296482426` from local Git objects.
Upstream credits
[awesome-skills/code-review-skill](https://github.com/awesome-skills/code-review-skill).
No earlier-source commit, file mapping, or separate licence was recorded in the
inherited checkout; that earlier provenance has not been independently audited.
This is not a check of upstream's latest remote state.

The [MIT licence](../LICENSE), including `Copyright (c) 2026 Nefelibata`, is
preserved byte for byte. No new licence or claim to upstream authorship is added.
Local adaptations replace the entry point and templates with an evidence-based
review contract, selectively audit Python and topic guides, replace heuristic
scores with a counts-only helper, add validation, and document evaluation limits.
Package 08 also rewrites TypeScript, React, and Vue guidance and consolidates its
common-bug duplicates. Scoped TypeScript compilation and React/Vue checks pass
under the versions and limits in the reference status. Its human acceptance is
effective following [PR 9 completion](https://github.com/smiggs/code-review-skill-codex/pull/9#issuecomment-6464622303).
Any separately agreed model review evaluation remains outside that technical
acceptance.
Package 09 also rewrites Go and Rust, replaces their inherited universal rules
with requirement-based prompts, consolidates Rust checklist duplicates, and adds
Go routing. Scoped executable checks and conditional human acceptance are recorded
in `plans/evidence/09-go-and-rust.md` in the source checkout.
The skill name and singular `reference/` directory remain unchanged.

## Verification

Package 03's approved scoped audit covers Python and selected process,
architecture, performance, and security guidance. Python examples were exercised
on Python 3.10.12 on Linux; this is not a runtime matrix or dependency audit.
The [reference status](reference-status.md) records each guide's remaining limits.
Full audit evidence is in `plans/evidence/03-python-and-reference-quality.md` in
the source checkout, outside the distributed runtime.

Package 04 added standard-library helper tests, PyYAML structural validation,
and CI targeting Python 3.10 and 3.14. See [helper tooling](helper-tooling.md).
Structure and helper checks do not measure review accuracy.

On 25 October 2026 the user accepted package 05 with explicit exceptions for
runtime `677beab3a37af42b08f9c46e5344b44afe84b3cf`. Batch 02 detected all four
seeded defects, with zero false positives, complete finding evidence, correct
no-findings and uncertainty handling, and no observed authority violations.
Only three of four priorities matched: case 04 was P0 against agreed P1.
That severity score remains failed, and priorities require human judgement.

One upstream run failed on backend connectivity before producing a report;
its scores remain unresolved. The comparison is incomplete and supports no
superiority claim. Neither batch passed the original criteria retrospectively.
Batch 01's context coupling prevents using it to establish independent behaviour.
Batch 02 audited all 20 initial contexts, with equivalent live tools for successful
evaluators and disclosed ordinary runtime guidance. Synthetic results do not
establish accuracy across other languages, production repositories, large diffs,
or repeated runs.

The source checkout preserves the decision at
`plans/evidence/05-completion-and-exceptions.md`, raw reports, scorecards,
fixtures, and context audits under `plans/evidence/05-behavioural-evaluation/`.
These evaluation artefacts are excluded from distribution. Rewritten guides and
evidence are English only. Companion Chinese installation and contribution docs
do not establish full translation or bilingual validation.

Package 06 checks packaging and installation separately. Its candidate manifest
and results are recorded in `plans/evidence/06-documentation-and-distribution.md`
in the checkout. A packaging smoke check does not repeat the independent
behavioural evaluation or validate inherited unverified references. Release
approval and any publication remain distinct human decisions.
