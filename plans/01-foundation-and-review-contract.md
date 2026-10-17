# Package 01: foundation and review contract

Status: complete; the user approved the contract on 18 October 2026. See the
[approved contract](../reference/review-contract.md),
[upstream inventory](evidence/01-upstream-inventory.md), and
[verification and decision record](evidence/01-foundation-and-review-contract.md).

## Outcome

Define what the adapted skill reviews, what makes a finding actionable, and
which decisions remain with the user before rewriting the workflow.

## Deliverables and responsibilities

- Record upstream repository, baseline commit, licence, and original attribution.
  Inventory every entry point, reference, template, helper, and inbound link.
- Retain PR, patch, and local-change review. Architecture and security reviews
  are explicit modes, not mandatory expansions of every small review.
- Define a finding as a supported defect or violated requirement with location,
  trigger, impact, and evidence. Label uncertainty without disguising it as a bug.
- Define severity using urgency and impact, with a documented mapping to Codex
  P0–P3 where appropriate. Keep confidence separate from severity.
- Define scope selection: comparison base/head for diffs, treatment of existing
  issues, surrounding context, and limits when the repository is unavailable.
- Define output: findings first, precise locations, verification limitations,
  and a valid no-findings result. Avoid mandatory praise, rhetorical questions,
  speculative improvements, and fixed findings quotas.
- Define read-only review authority and preserve the target project's human
  approvals. Recommendations do not post reviews, approve, or merge changes.

Put reusable contract detail in a focused reference linked from the eventual
entry point. Keep policy specific to this fork in `AGENTS.md`.

## Verification

Walk through a clear bug, a harmless refactor, an uncertain performance concern,
a pre-existing defect, and a review with missing context. Confirm the contract
produces distinct, honest outcomes without a line-count or coverage gate.

## Human checkpoint

Review the finding examples, severity mapping, default scope, and approval
boundaries. Record any requested changes before dependent implementation.

## Exit criteria

- Upstream attribution and baseline are recorded and licences preserved.
- Every example has a defensible finding, question, or no-findings outcome.
- Core review scope and authority are explicit and portable across projects.
- Photo-workflow invariants remain target-project instructions, not global rules.
