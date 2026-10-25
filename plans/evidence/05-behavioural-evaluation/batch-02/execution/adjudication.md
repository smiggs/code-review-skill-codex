# Batch 02 case 04 severity dispute

Completion disposition: the user accepted this severity mismatch as an
advisory limitation on 25 October 2026. The [completion decision](../../../05-completion-and-exceptions.md)
closes the package without relabelling this report or its failed severity score.
No further priority adjudication is required for package completion.
Evaluated adapted revision:
`677beab3a37af42b08f9c46e5344b44afe84b3cf`.

The user approved the [batch 02 criteria](../acceptance-criteria.md) before
review. They require P1 for case 04. The [adapted report](case-04-adapted/report.txt)
instead assigns P0, stating that the required readiness gate unconditionally
prevents the next operation from starting. The [scorecard](scorecard.json)
therefore records a severity failure while crediting correct detection and
complete evidence. No criterion, fixture, report, or original score is changed.

The [target requirements](../fixtures/case-04/head/AGENTS.md) make `render()`
the required deployment readiness gate with no supported bypass. The report
correctly traces the return-type change through the unchanged caller and
reproduces TypeError. It discloses that the deployment procedure itself was
not supplied or run. The [upstream report](case-04-upstream/report.txt) detects
the same issue but uses an unmapped blocking label, so it cannot settle P0/P1.

The [approved contract](../../../../../reference/review-contract.md) defines
P0 as critical with immediate action, typically a demonstrated release-wide
failure broadly affecting supported use without special conditions. P1 covers
failure of a core path under supported conditions before the affected release
or next operational use.

The concrete disagreement is whether unconditional failure of this documented
deployment gate establishes that P0 release-wide impact, or whether the
evidenced next-operation failure warrants P1. The fixture does not supply a
running release, deployment integration, or an immediate incident. Those limits
support the agreed P1 interpretation, while the mandatory gate explains the
report's broader interpretation.

Pre-completion AI recommendation: retain the P1-rubric failure and obtain human
classification of the cause before changing reusable guidance. A correct defect report with
a disputed priority does not establish a missed defect or a false positive.
Do not force a lower label through a special rule for readiness gates. Any
fixture/rubric clarification belongs to a separately frozen future evaluation.

The pre-completion recommendation was that a human decision identify faulty
skill guidance, ambiguous fixture scope, or an overly rigid expected priority,
with its impact rationale. It
must not silently turn this batch into a pass. The missing upstream case 01
report remains a separate unresolved comparison limit, even if severity is
adjudicated. No further review is launched by preparing this brief.
