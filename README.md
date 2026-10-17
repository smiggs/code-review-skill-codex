[English](./README.md) | [简体中文](./README.zh-CN.md)

# Code Review Skill for Codex

Reference: adapted from https://github.com/awesome-skills/code-review-skill

This fork is preparing an adaptation of NefelibataBIGR/code-review-skill-codex.
The [upstream baseline and inventory](plans/evidence/01-upstream-inventory.md)
record attribution and the preserved MIT licence. The
[review contract](reference/review-contract.md) was approved on 18 October 2026.
The package 02 entry point and templates were merged into `main`. Package 03's
scoped Python and topic-guide changes were approved on 18 October 2026; the
[reference status](reference/reference-status.md) records verified scope and
deferred technical checks. Rewritten guides and evidence are English only.
This describes the working branch, not the upstream checkout installed below.

A modular skill for Codex that turns code review into a structured, high-signal process.

It supports pull requests, patch review, and local-change review across
multi-language repositories, with architecture and security audits as explicit modes.

## What This Repository Contains

- `SKILL.md`: the primary skill entrypoint and trigger metadata
- `agents/openai.yaml`: Codex UI metadata
- `reference/`: language- and topic-specific review guides loaded as needed
- `assets/`: reusable templates and checklists
- `scripts/`: helper tooling, including PR analysis support

## Supported Review Areas

- React
- Vue
- TypeScript
- Python
- Java
- Go
- Rust
- C
- C++
- CSS / Less / Sass
- Qt
- Architecture review
- Performance review
- Security review
- Common bug patterns

## How Codex Uses This Skill

The skill is discovered through the metadata in [SKILL.md](./SKILL.md). Its trigger description is intentionally focused on when the skill should load:

- reviewing pull requests
- reviewing code changes
- conducting architecture reviews
- conducting security reviews
- giving structured review feedback on patches or local changes

Implementation and debugging requests without a review task do not activate it.

Once loaded, Codex can selectively read files from `reference/` instead of pulling the entire skill into context at once.

## Install

### Global installation

Clone or copy this repository into your Codex skills directory:

```bash
# macOS / Linux
git clone https://github.com/NefelibataBIGR/code-review-skill-codex.git \
  ~/.codex/skills/code-review-codex

# Windows PowerShell
git clone https://github.com/NefelibataBIGR/code-review-skill-codex.git `
  "$env:USERPROFILE\.codex\skills\code-review-codex"
```

### Alternative location

If your setup prefers personal agent skills, copy it into:

```bash
~/.agents/skills/code-review-codex
```

After installation, restart Codex so the new skill metadata is picked up.

## Usage

### Explicit invocation

Ask Codex to use the skill directly:

```text
Use code-review-codex to review this PR.
Focus on supported bugs, regressions, and violated requirements.
```

### Natural-language triggering

The skill is also designed to trigger from ordinary requests such as:

```text
Review these changes for bugs and maintainability issues.
```

```text
Do an architecture review of this refactor.
```

```text
Check this service for security problems before merge.
```

## Review Style

This skill supports reviews that:

- Prioritise bugs, regressions, and violated requirements over preferences.
- Give each finding a precise location, trigger, impact, and evidence.
- Keep priority separate from confidence, and questions separate from findings.
- Accept no actionable findings and disclose scope and verification limits.
- Load language and topic guides only when relevant.

A review request authorises analysis and an advisory report. Fixing code, posting
comments or reviews, approving, and merging need separate authorisation and any
target-project approvals. See the [report template](assets/pr-review-template.md)
for the findings-first format. Architecture and security checks relevant to a
change do not automatically expand into whole-system audits.

## Repository Layout

```text
code-review-codex/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- reference/
|   |-- reference-status.md
|   |-- review-contract.md
|   |-- react.md
|   |-- vue.md
|   |-- typescript.md
|   |-- python.md
|   |-- java.md
|   |-- go.md
|   |-- rust.md
|   |-- c.md
|   |-- cpp.md
|   |-- qt.md
|   |-- css-less-sass.md
|   |-- architecture-review-guide.md
|   |-- performance-review-guide.md
|   |-- security-review-guide.md
|   |-- common-bugs-checklist.md
|   `-- code-review-best-practices.md
|-- assets/
|   |-- review-checklist.md
|   `-- pr-review-template.md
`-- scripts/
    `-- pr-analyzer.py
```

## Notes for Maintainers

- Keep `SKILL.md` focused on triggers and core process, not exhaustive reference material.
- Put detailed patterns in `reference/`.
- Update both language docs when installation or usage changes.
- Keep examples realistic and review-oriented.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution and validation guidance.
