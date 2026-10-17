# Review report template

Follow the [review contract](../reference/review-contract.md). Copy the relevant
sections below, replace the uppercase placeholders, and omit unused optional
sections. Repeat a finding only for a distinct supported defect. Honour a
required output schema rather than imposing this Markdown format.

## Findings

### [PRIORITY] FINDING_TITLE

`FILE_PATH:START_LINE–END_LINE` (new or old side as appropriate)

When TRIGGER occurs, the change causes OBSERVABLE_IMPACT rather than
EXPECTED_BEHAVIOUR. EVIDENCE establishes the causal link. CORRECTION_DIRECTION
is optional when it helps the reader act.

Verification: REPRODUCTION_RESULT or STATIC_TRACE_OR_REQUIREMENT. Disclose
REMAINING_ASSUMPTIONS separately from priority. Use P0–P3 according to the
contract, or explain the target project's severity mapping. Keep the location
as small as useful; if lines are unavailable, cite a symbol or patch hunk and
state that limit.

If there are no supported findings, replace the finding block with:

> No actionable findings in the reviewed scope.

## Material questions (optional)

UNRESOLVED_PREMISE could change MATERIAL_CONCLUSION. MISSING_EVIDENCE would
settle it. Keep speculation here without a defect priority.

## Scope and verification

Reviewed REVIEW_MODE and COMPONENT_OR_FILES, comparing BASE to HEAD_OR_WORKING_FILES.
List included untracked files and exclusions where relevant. If revisions or
repository context are unavailable, identify the supplied patch or excerpt and
state the limit.

Checks run: COMMAND_OR_INSPECTION and OBSERVED_RESULT.

Relevant checks not run: CHECK and REASON. Record unavailable callers,
requirements, or runtime context that materially limit conclusions. Never imply
that a proposed check was executed.

## Optional notes

Include useful or requested suggestions separately from defects. Identify any
material pre-existing issue as outside the change scope. Omit this section when
there is nothing to add.

The report is advisory. It neither submits an external review nor supplies the
user or target project's approval for fixes, publication, or merging.
