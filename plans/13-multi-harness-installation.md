# Package 13: Multi-harness installation

Status: plan prepared on 28 October 2026; awaiting the user's agreement on the
install layout recorded in the human checkpoint below. This is a planning
record: agreeing it does not imply release publication, plugin packaging, or
any change to package 06's conditional completion.

## Outcome

A user of Claude Code, ZCode, OpenCode, or Antigravity can install a pinned
candidate of the skill into that harness's discovered skill location, guided by
documentation that separates verified behaviour from vendor documentation that
has not been exercised here.

The documented install path, `~/.agents/skills/code-review-codex/`, already
covers Codex, ZCode, and OpenCode if their documented discovery behaviour
holds; only Claude Code and Antigravity need an additional copy or link. This
package turns that observation into checked documentation and per-harness
evidence.

## Known discovery surface

Recorded on 28 October 2026 from the harnesses' published documentation and
issue trackers, and from ZCode's bundled configuration guide on the test
machine. Implementation must re-verify each path against official
documentation and record fresh checked-on dates before the documentation
merges.

| Harness | Personal scope | Project scope | Note |
| --- | --- | --- | --- |
| Codex (existing) | `~/.agents/skills/` | `.agents/skills/` | Current documented path. |
| ZCode | `~/.zcode/skills/`, `~/.agents/skills/` | `.zcode/skills/`, `.agents/skills/` | First same-named skill wins in discovery order; keep one copy to avoid shadowing. |
| OpenCode | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | Paths are reportedly fixed in the client, not configurable; verify on the tested version. |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | Standard Agent Skills frontmatter; whether symlinked skill folders are discovered must be verified. |
| Antigravity | `~/.gemini/antigravity/skills/` | unspecified in published documentation | An open upstream report says symlinked skills may not be discovered; plan a real directory copy. |

## Deliverables and responsibilities

- Re-verify the discovery surface above against official documentation for
  each harness, recording paths, frontmatter tolerance (name and description;
  the multi-line block-scalar description), invocation style, and symlink
  behaviour, each with a checked-on date.
- Confirm client availability on the test machine (ZCode and Claude Code are
  installed there; check OpenCode and Antigravity) and record which harnesses
  were actually exercised.
- Extend [distribution](../reference/distribution.md) with a per-harness
  install table covering personal and project scopes, the agreed install
  layout, the Antigravity symlink caveat, and an update and rollback procedure
  extended from one location to several (move-and-replace per location,
  rechecking discovery each time).
- Specify a preflight collision check in the same documentation: before
  installing, enumerate every location the target harness scans for the
  same-named skill in discovery order, and reject the installation with removal
  guidance when a higher-priority duplicate exists. The documented installer
  must not silently remove, rename, or overwrite another location's copy.
- Update the English and Chinese README install sections so they name the
  supported harnesses and paths, keeping the two languages aligned and
  recording translation limits honestly.
- Amend [helper tooling](../reference/helper-tooling.md) only if verification
  shows a harness without shell or Python access; otherwise the entry point's
  existing tool-unavailable fallback covers it.
- Leave `scripts/validate-skill.py` unchanged unless a harness requires extra
  frontmatter keys; any exception must be recorded and kept minimal.

## Tests and verification

For each harness available on the test machine: install the packaged candidate
into the verified location, confirm discovery, run the explicit and ordinary
invocation prompts from the README, and run one representative review on a
synthetic repository, recording loaded skill paths and reference reads. Use
ZCode's skill-diagnosis guidance for its discovery check and a headless
Claude Code run where supported. Harnesses that cannot be exercised are
recorded as documented but untested, never as validated.

Run the shared documentation and structural checks: `git diff --check`,
`git diff --stat`, the repository structural validator, the standard-library
unit tests, and the system skill-creator quick validator when available.
Verify relative links and cross-document consistency between the English and
Chinese README files. These checks do not measure review accuracy.

## Human checkpoint

Agree the install layout before implementation: one canonical copy in
`~/.agents/skills/code-review-codex/` covering Codex, ZCode, and OpenCode, a
symlink at `~/.claude/skills/code-review-codex` only if Claude Code is verified
to discover symlinked skills, and a real directory copy under Antigravity's
skills directory. The alternative, independent copies in every scanned
location, avoids symlink quirks at the cost of a synchronisation burden on
every update, and the chosen trade-off must be recorded. Project scope is part
of the same decision: the discovery table records project locations from
vendor documentation, validation exercises personal scope by default, and
project-scope instructions are labelled documented but untested unless the
user agrees to exercise them. Antigravity's project path is unspecified in its
published documentation and stays out of the documentation unless verification
finds an official source. Review the completed
documentation and per-harness evidence against the exit criteria before any
approval; publication remains out of scope.

## Exit criteria

- Every documented path cites an official source with a checked-on date, and
  untested harnesses are labelled as documented but untested.
- The install layout decision is recorded with the user's choice and date.
- Per-harness evidence, including unavailable checks, is recorded under
  `plans/evidence/` when implementation produces it; no placeholder success
  records.
- English and Chinese installation guidance are aligned, and relative links
  and cross-document references resolve.
- The structural validator and the standard-library unit tests pass on the
  changed documentation; no claim of review accuracy or release readiness is
  made by this package.
- Package 06's completion conditions, upstream attribution, the skill name,
  and existing `reference/` paths are preserved; no plugin, marketplace, or
  ChatGPT upload work is introduced.
