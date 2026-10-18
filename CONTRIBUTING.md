[English](./CONTRIBUTING.md) | [简体中文](./CONTRIBUTING.zh-CN.md)

# Contributing

This repository packages a Codex skill. Contributions should preserve discoverability, progressive disclosure, and review quality.

## Goals

- keep the skill easy for Codex to discover
- keep core instructions short and specific
- move detailed material into `reference/`
- improve review accuracy without bloating the trigger metadata

## Repository Conventions

### Required files

- `SKILL.md`
- `agents/openai.yaml`

### Optional support files

- `reference/*.md`
- `assets/*`
- `scripts/*`

### Current layout

```text
code-review-codex/
|-- SKILL.md
|-- README.md
|-- README.zh-CN.md
|-- CONTRIBUTING.md
|-- CONTRIBUTING.zh-CN.md
|-- agents/
|   `-- openai.yaml
|-- reference/
|-- assets/
`-- scripts/
```

## Editing Rules

### `SKILL.md`

- Keep `name` stable unless there is a migration reason.
- Keep `description` focused on trigger conditions.
- Start the description with `Use when...`.
- Do not summarize the full workflow in the description.
- Keep the body focused on process and navigation.
- Keep the workflow and templates aligned with the approved
  [review contract](reference/review-contract.md). Its evidence and authority
  rules take precedence over conflicting inherited guide advice.

### `agents/openai.yaml`

- `display_name` should stay human-readable.
- `short_description` should match the skill scope without repeating the full README.

### `reference/`

- Put heavy guidance here, not in `SKILL.md`.
- Prefer one topic per file.
- Keep filenames lowercase and hyphenated.

### `README*`

- `README.md` is the English primary document.
- `README.zh-CN.md` is the Chinese companion.
- Both files must include language-switch links at the top.
- Keep installation and usage examples aligned across both languages.

### `CONTRIBUTING*`

- `CONTRIBUTING.md` is the English primary document.
- `CONTRIBUTING.zh-CN.md` is the Chinese companion.
- Keep contribution rules aligned between both documents.

## Adding or Updating Reference Guides

When adding a new language or topic guide:

1. Add the file under `reference/`.
2. Use a clear, lowercase, hyphenated filename.
3. Link to it from `SKILL.md` only if the skill should actively route readers there.
4. Update both README files if the supported scope changed.

## Validation Checklist

Before merging:

- Confirm `SKILL.md` frontmatter is valid YAML.
- Confirm `name` and `description` still match the intended trigger behavior.
- Confirm `agents/openai.yaml` exists and is in sync with the skill name.
- Confirm language-switch links work in all four docs.
- Confirm example installation paths still match Codex conventions.
- Confirm new reference files are actually referenced or intentionally discoverable by name.

## Suggested Manual Verification

Use a fresh Codex session after installation.

### Explicit invocation test

Ask Codex:

```text
Use code-review-codex to review these changes for supported bugs, regressions, and violated requirements.
```

Expected result:

- review is structured
- bugs and risks are prioritized
- feedback is not dominated by formatting trivia

### Natural trigger test

Ask Codex:

```text
Review these changes for security issues and maintainability problems.
```

Expected result:

- Codex recognizes this as a code review task
- the response emphasizes findings, severity, and concrete review feedback

Also inspect an unrelated implementation request, a clean refactor, a patch
without repository access, and unavailable review tools. The unrelated request
should not activate review mode. A clean change should allow no findings; missing
context or tools should produce honest limits rather than invented defects.
Review output alone must not fix code, post reviews, approve, or merge.

### Package 03 example checks

Package 03 provides standalone example checks using only the Python standard
library, exercised on Python 3.10.12 on Linux with symlink support:

```bash
python3 plans/evidence/03-python-examples.py
```

They verify guide examples and a synthetic consumer, not the diff helper or
independent review quality. See the [reference status](reference/reference-status.md)
for technical-audit and translation limits. These checks remain separate from the helper test suite.

## Non-Goals

- Do not turn the skill into a generic programming guide.
- Do not duplicate large sections from `reference/` into `SKILL.md`.
- Do not add extra docs unless they materially improve installation, contribution, or bilingual usability.

## Helper and structural checks

Use Python 3.10 or later and Git on Linux. The helper uses the standard library;
structural checks use the pinned PyYAML dependency in `requirements-dev.txt`.
Run the [local validation commands](reference/helper-tooling.md#local-validation)
before submitting helper or package changes. CI runs the same checks on Python
3.10 and 3.14. The tests verify counts, explicit errors, read-only operation, and
structural invariants; they do not measure independent review accuracy. Review
link anchors, prose consistency, and the documented unsupported cases manually.
