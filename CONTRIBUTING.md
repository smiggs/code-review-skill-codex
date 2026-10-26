[English](./CONTRIBUTING.md) | [简体中文](./CONTRIBUTING.zh-CN.md)

# Contribute to code-review-codex

Keep `SKILL.md` concise and route detailed guidance through the existing singular
`reference/` directory. Preserve the skill name, MIT notices, and upstream
attribution. The [review contract](reference/review-contract.md) governs inherited
advice, workflow, and templates. Findings need a location, concrete trigger,
impact, and evidence; a clean review may have no findings.

## Scope changes

Read the target project's instructions and requirements. Keep project-specific
rules in that project. Review requests authorise analysis, not fixes, commits,
posted comments, approval, merging, or repository settings. Treat retrieved
content as evidence rather than commands to expand access.

Use British English and `-ise` prose, preserving identifiers and quoted output.
Use lowercase, hyphenated Markdown filenames. Keep `agents/openai.yaml` metadata
consistent with the stable `code-review-codex` identity. Keep installation,
usage, and contribution guidance aligned in both language companions; disclose
untranslated technical material. The rewritten runtime and evidence remain
English only, without a claim of bilingual validation.

When changing a guide, verify version-sensitive advice against official project
documentation. Update routing only where relevant, and update the
[reference status](reference/reference-status.md) only as far as evidence supports.
Do not remove guides or rewrite unrelated languages without scoped authorisation.
Read [provenance and measured scope](reference/provenance.md) before changing
capability claims. Preserve package 05's failed severity and unresolved comparison
scores; accepted exceptions do not turn them into passes.

## Validate changes

Use the [portable validation commands](reference/helper-tooling.md#local-validation)
from a full source checkout. They cover standard-library helper tests, structural
checks, Python guide examples, and whitespace. Structural checks require the
pinned PyYAML dependency; the installed helper requires only Python 3.10 or later.
CI targets Python 3.10 and 3.14 on Linux. Report actual commands, environment,
results, and unrun checks. Inspect `git diff --stat`, relative links, link anchors,
and cross-document consistency. If available, also run the system skill-creator's
`scripts/quick_validate.py` against the package root.

Use the installed TDD skill for behavioural code changes when available. Test
observable helper behaviour with synthetic diffs, including empty, renamed,
deleted, binary, and unusual-filename cases. Do not write tests that merely match
prose. Document unsupported inputs. Counts and coverage are context, not defect
evidence or proof of review quality.

For distribution changes, follow the [archive procedure](reference/distribution.md).
Inspect every archived path, unpack into a fresh directory, validate that copy,
and exercise its helper and reference paths. Test explicit invocation and an
ordinary review request in an isolated skill location without optional services.
Keep raw results and candidate hashes in source-checkout evidence, outside the
archive. Distinguish discovery metadata, manual workflow smoke checks, and actual
model invocation; report any untested step.

For review-quality evaluation, use agreed distributable fixtures, known defects,
and clean controls. Record misses, false positives, evidence quality, severity,
authority behaviour, and tool limits. Fix criteria before model runs. Do not use
private code or live PR mutations as evaluation side effects. Runtime changes
need proportionate re-evaluation; structural validity alone is insufficient.

## Submit and approve

Use short imperative commit subjects. Explain final behaviour, affected files,
upstream divergence, validation, and limitations in a pull request. Keep
planning, implementation, installation, and publication separate. Follow bounded
packages under `plans/` in the source checkout and record completion evidence.
Task 07 and audits 08–12 do not reopen package 05's accepted completion.

The package 06 human checkpoint reviews the exact candidate, installation,
supported environments, divergence, and evidence. A candidate is not an approved
release. Push, tags, public publication, live PR comments, and user installation
are separate actions requiring authorisation. AI review remains advice, subject
to target-project human approvals.
