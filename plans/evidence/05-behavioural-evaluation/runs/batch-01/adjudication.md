# Batch 01 severity adjudication brief

Prepared and accepted on 25 October 2026. The user accepted the recommendations
below. This record changes no report, score, fixture,
criterion, or runtime file. No further model reviews have run.

Evaluated adapted revision: `677beab3a37af42b08f9c46e5344b44afe84b3cf`.
The [accepted criteria](../../acceptance-criteria.md) require P2 for both cases.
The [original scorecard](scorecard.json) records both as severity failures.
Those scores remain the batch 01 results regardless of a later rubric revision.

## Case 03: indefinite retention becomes seven days

Read the [upstream report](case-03-upstream/report.txt),
[adapted report](case-03-adapted/report.txt),
[target requirements](../../fixtures/case-03/head/AGENTS.md), and
[changed function](../../fixtures/case-03/head/retention.py).

Both reports establish that supported input zero returns seven instead of
zero. Both describe a risk of premature expiry and explicitly disclose that
no downstream archive deletion implementation was supplied or exercised.
Neither claims to have reproduced deletion. The target says a user relies on
zero to retain an archive beyond seven days.

The [review contract](../../../../../reference/review-contract.md) permits P1
for severe loss under concrete supported conditions, and P2 for bounded impact.
The [answer key](../../answer-key.md) requires P2 and warns against elevating
severity from an imagined caller. The disagreement is whether the documented
retention consequence supports a severe-loss risk without the expiry code.
The reproduction alone cannot settle that impact judgement.

AI recommendation: classify the fixture's impact evidence as ambiguous for
severity. Keep the observed contract violation and original P2 mismatch.
Before another batch, specify the expiry consequence or a bounded operational
impact in the fixture, then agree severity from that evidence. The reports do
not establish a need to change the reusable skill.

## Case 04: supported status display always raises

Read the [upstream report](case-04-upstream/report.txt),
[adapted report](case-04-adapted/report.txt),
[target requirements](../../fixtures/case-04/head/AGENTS.md),
[changed serialiser](../../fixtures/case-04/head/serializer.py), and
[unchanged caller](../../fixtures/case-04/head/caller.py).

Both reports trace the changed return type through the unchanged caller.
The recorded checks show base returning ready and head raising TypeError.
Every call to the documented entry point fails. The target supplies no
alternative display path, practical workaround, operational urgency, or
statement that this display is peripheral to the application.

The contract permits P1 for failure of a core path under supported conditions.
The accepted rubric calls this broken status rendering bounded and requires
P2, but the fixture does not establish that operational bound. P1 is defensible
if the sole documented entry point is treated as a core path; P2 is defensible
if it is a peripheral display with bounded consequences.

AI recommendation: classify the expected priority as insufficiently justified
by the fixture. Preserve the original mismatch. Before another batch, supply
the display's operational role and agree its priority. Do not teach the skill
that status rendering always warrants P2.

## Human adjudication recorded

On 25 October 2026, after clarification that the original P2 expectations were
too rigid for the supplied evidence, the user replied, "OK I accept your
recommendations". Reviewer identity: the user in this chat; no personal name
was supplied.

- Case 03: accepted ambiguous fixture impact evidence. The documented reliance
  on indefinite retention and absence of downstream expiry code do not settle
  P1 versus P2.
- Case 04: accepted an insufficiently justified expected priority. P1 is
  defensible for failure of every call to the supported entry point; the
  fixture does not establish the bounded operational impact assumed by P2.
- Neither case establishes faulty reusable skill guidance. Do not change the
  skill to force P2. Clarify fixture impact and agree severity before another
  batch. No replacement expected priority was approved for either case.

This is acceptance of the severity adjudication, not a pass for the evaluated
revision. Original reports and scores remain unchanged; batch 01 does not
retroactively pass. No additional reviews or reruns were authorised by this
decision.

The overall checkpoint remains unresolved: evaluator independence is also
unresolved, so resolving severity alone cannot complete package 05. Context
inspection must precede supplying cases to any isolated evaluators. A full
20-review repeat needs separate agreement beyond the unused six-review
correction allowance. No repeat is proposed for approval in this brief.
