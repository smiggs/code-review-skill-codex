# Review communication and process

Use this reference when review communication or team process is part of the
request. The [review contract](review-contract.md) governs findings, priority,
scope, and authority. A team may supply its own response targets and approval
process; this guide sets no review-time budget or automatic PR-size rule.

## Communicate a supported problem

Lead with the defect and explain the concrete trigger, impact, location, and
evidence. Direct statements help the author distinguish verified behaviour from
uncertainty. Use a question when a material premise is missing, rather than
turning a known defect into a rhetorical question.

For example, when the target accepts zero as an immediate timeout:

> [P2] Preserve zero as a valid timeout
>
> `wait.py:2`: Supplying `0` selects the new `30` fallback and delays an operation
> that the documented contract requires to return immediately. Static evaluation
> of `0 or 30` establishes the regression.

Priority describes urgency and impact; confidence describes evidence. Follow the
contract's P0–P3 mapping or explain the target's own mapping. A pattern, a test gap,
a naming preference, or a large file does not establish a defect on its own.

## Keep the report useful

Put findings first. Record scope, checks, results, and material verification limits.
A clean review can say "No actionable findings in the reviewed scope" without
praise, suggestions, or approval language. Use the
[report template](../assets/pr-review-template.md) when it helps.

Keep optional improvements separate and include them only when useful or requested.
Consolidate repeated symptoms of one cause. Offer a correction direction when
supported, without expanding a review into an unrequested rewrite.

## Resolve disagreement with evidence

Check the relevant requirement, caller, reproduction, or dependency contract.
If the evidence disproves a concern, remove it. If evidence is missing, record
what would settle the question. Escalation and human sign-off follow the target
project's process; an AI recommendation supplies neither.

For large changes, identify the reviewed areas and any omitted paths. Request a
narrower scope only when needed to give a useful review, explaining the specific
limit. Line counts alone do not require splitting a PR.

## Learn from outcomes

Where the team requests process evaluation, inspect escaped defects, false
positives, repeated misunderstandings, and the quality of evidence. Response time,
review counts, and coverage can give context; they are not proof of review quality.
Use synthetic or explicitly permitted artifacts for experiments. A review request
does not authorise source fixes, external comments, submitted reviews, approval,
or merging. Preserve the target's human approval requirements.
