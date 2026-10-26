[English](./README.md) | [简体中文](./README.zh-CN.md)

# Code review for Codex

`code-review-codex` reviews pull requests, supplied patches, and local changes for
supported bugs, regressions, and violated requirements. Architecture and security
audits are explicit modes with agreed boundaries. It uses local files or available
connected tools; no CodeRabbit, GitHub CLI, MCP server, or other integration is
required. The optional counts helper requires Python 3.10 or later.

This adaptation comes from
[NefelibataBIGR/code-review-skill-codex](https://github.com/NefelibataBIGR/code-review-skill-codex),
which credits [awesome-skills/code-review-skill](https://github.com/awesome-skills/code-review-skill).
The [MIT licence](LICENSE) and original copyright notice are preserved. See
[provenance and measured scope](reference/provenance.md) for baseline revisions,
local changes, evaluation results, and unresolved provenance limits.

## Review behaviour and limits

The [entry point](SKILL.md) routes to relevant references and the
[review contract](reference/review-contract.md). Findings require a precise
location, trigger, impact, and evidence. Questions and suggestions stay separate;
an empty findings list is valid. A review authorises analysis and an advisory
report. Fixes, commits, posted reviews, approval, and merging require separate
authorisation and the target project's approvals.

Python and selected topic guides have a scoped audit. React, Vue, TypeScript,
Rust, Java, Go, C, C++, Qt, CSS/Less/Sass, and inherited common-bug examples have
remaining technical checks. Read the [reference status](reference/reference-status.md)
before relying on language or version advice. The rewritten runtime guidance is
English; the Chinese companion documents align installation and contribution
steps, but do not provide a full technical translation or bilingual validation.

The accepted synthetic evaluation detected four seeded defects with zero false
positives, but matched only three of four priorities. Severity remains advisory:
one agreed P1 was reported as P0. One upstream run failed before producing a
report, so the comparison is incomplete and establishes no superiority over
upstream. The original acceptance criteria did not all pass. Results do not
establish accuracy on other languages, production repositories, large diffs, or
repeated runs. See the [evaluation summary](reference/provenance.md#verification).

## Install a pinned copy

Use Git and Python 3.10 or later on Linux for the documented commands. Choose a
full commit ID from a human-approved release-candidate record. `APPROVED_COMMIT`
is a placeholder, not a published version. Package 06's candidate is awaiting its
human checkpoint; no release has been published by this work.

```bash
git clone https://github.com/smiggs/code-review-skill-codex.git /tmp/code-review-source
git -C /tmp/code-review-source checkout --detach APPROVED_COMMIT
git -C /tmp/code-review-source rev-parse HEAD
```

Confirm the resolved revision matches your chosen ID. From that checkout, follow
[distribution and installation](reference/distribution.md) to build and inspect
the allowlisted ZIP, then extract it into `~/.agents/skills`. The complete skill
includes `reference/`, `assets/`, `agents/`, `scripts/pr-analyzer.py`, and `LICENSE`;
copying only `SKILL.md` loses its supporting material. Avoid duplicate copies
with the same skill name in other scanned locations.

OpenAI documents personal skills in `~/.agents/skills` and repository skills in
`.agents/skills`. Codex detects changes automatically; restart it if the skill
does not appear. In CLI or IDE, use `/skills` or `$code-review-codex` to select it.
These are documented behaviours, not a claim that every client was tested here.
See [official skill guidance](https://learn.chatgpt.com/docs/build-skills), checked
on 25 October 2026, and the candidate evidence for the environments actually tested.

## Use the skill

Explicit invocation:

```text
Use code-review-codex to review these changes for supported bugs, regressions, and violated requirements.
```

Ordinary review request:

```text
Review these changes for bugs and regressions.
```

Provide the patch or repository and intended comparison. The skill establishes
scope, reads project requirements, investigates concrete failure paths, and
reports findings first with checks and verification limits. Implementation and
debugging requests without a review task are outside its trigger scope.

The optional [diff helper](reference/helper-tooling.md) supplies file and text-line
counts, not risk scores or approval recommendations. It runs without third-party
Python packages. Its documented restricted Git-diff input contract still applies.

## Distribution and maintenance

The [distribution guide](reference/distribution.md) defines archive contents,
installation, update, rollback, and conditional ChatGPT upload guidance. The ZIP
is a standalone skill folder, not a plugin or a universally supported ChatGPT
attachment. Upload availability and execution support must be checked in the
specific surface and account; no upload was performed here.

See [contribution guidance](CONTRIBUTING.md) for validation and change boundaries.
Full planning and evaluation records live under `plans/` in the source checkout;
they are deliberately excluded from the installable archive.
