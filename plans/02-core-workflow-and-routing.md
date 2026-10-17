# Package 02: core workflow and reference routing

## Outcome

Make the entry point short, usable in ChatGPT/Codex, and focused on supported
findings rather than generic review etiquette.

## Deliverables and responsibilities

- Rewrite `SKILL.md` around the package 01 contract: establish scope, read target
  instructions, inspect changed behaviour and callers, verify concerns, report.
- Keep discovery focused on review tasks. Do not activate for every coding task.
- Remove prescribed minute budgets, automatic requests to split large PRs,
  compulsory praise, and blanket requirements to phrase defects as questions.
- Route to the matching language and topic guides only when they aid the review.
  Avoid loading the entire reference library by default.
- Support local tools, connected GitHub, and supplied patches without requiring
  a specific MCP, shell, browser, or Claude-specific path or environment variable.
- With only a patch, bound claims to the evidence and request missing context
  only when it materially changes the conclusion.
- Keep review-only execution distinct from fixes and external submission.
- Update `assets/pr-review-template.md` and `assets/review-checklist.md` to match
  the contract. Treat checklists as prompts for inspection, not issue generators.
- Keep `agents/openai.yaml` consistent with the stable skill name and discovery
  scope; preserve automatic discovery unless the user requests otherwise.

## Verification

- Check frontmatter and relative links, including every routed reference.
- Exercise explicit invocation, an ordinary PR review request, and an unrelated
  coding request to inspect routing and boundaries.
- Confirm a no-findings review produces no invented criticism or approval action.
- Check behaviour with local files, supplied patch only, and unavailable tools.

## Human checkpoint

Review a short defect report and a no-findings report for clarity and useful
evidence. Confirm the entry point is understandable without loading all guides.

## Exit criteria

- Entry point and templates implement the same review contract.
- Reference links resolve; relevant detail is progressively disclosed.
- No hard dependency on unavailable tools or Claude-specific infrastructure.
- Review output does not imply permission to mutate the target repository.
