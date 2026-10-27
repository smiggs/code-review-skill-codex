# Task 07: proposed six-case diagnostic

Historical design proposal, prepared on 27 October 2026. The user subsequently
agreed the priority interpretation and fixture preparation. The concrete
[prepared diagnostic](07-severity-diagnostic/README.md) now supplies the candidate,
fixtures, criteria and manifests for the second checkpoint. Statements below
about unimplemented designs describe this proposal's preparation stage; no
reviews are authorised by either preparation document.
Read the [boundary audit](07-severity-calibration.md) before selecting a candidate.

## Proposed case designs and withheld key

These are six original synthetic designs, not executable fixtures or observed
results. Proposed Python implementations use only the standard library and
in-memory or scratch data. Distribute any eventual fixtures under the
repository's MIT licence. Each case will contain complete base/head snapshots,
a generated diff, target requirements, and enough callers to establish its
consequence. No production data or historical evaluation code is required.

The following table is an evaluator-withheld proposed answer key. Target inputs
must describe operational facts without priority labels, expected findings,
this table, or instructions to choose a severity. These case IDs do not encode
priority; numerical execution order deliberately differs from priority order.

| Case | Concrete proposed change and operational premises | Proposed label and rationale | Premise check to prepare |
| --- | --- | --- | --- |
| 01 | A batch invoice importer changes its merge key from `(supplier, invoice_id)` to `invoice_id`. Two supported suppliers reuse the same ID, so the later invoice silently replaces the earlier one before posting. The daily posting path is required, has no alternate importer, and processes such pairs in its next run. The change is not deployed; no current loss is claimed. | P1: a supported conditional trigger causes core financial records to be omitted; fix before the next use. The condition does not make the impact minor, and a scheduled future run does not establish an immediate incident. | Use two supplier records with one shared ID; compare complete base/head caller outputs and show the missing posting record. Also check distinct IDs and a single supplier. |
| 02 | A human-readable inventory summary loses the documented final full stop. All counts, item names, and machine-readable outputs stay correct. The punctuation is an explicit user-facing format requirement; nothing parses this text and no operational decision depends on punctuation. | P3: an evidenced formatting requirement violation with small user impact, rather than a preference invented by the reviewer. | Compare exact base/head strings; verify counts and the separate machine-readable representation agree. |
| 03 | A central request dispatcher changes an allowed-operation check so that it rejects every supported operation. The complete caller routes all supported customer requests through it. The supplied synthetic incident record states this revision is active across the service, every customer request is failing, and immediate restoration is required. No alternate route exists. | P0: broad ongoing service failure with explicit immediate urgency and no special input or configuration. The incident record is a synthetic premise, not a claim of a real incident or an executed production deployment. | Exercise every supported operation through the supplied caller, showing base success and head rejection. Check the incident statement against the fixture's complete supported domain. |
| 04 | A report export changes the last-page boundary and omits one row when the row count is an exact multiple of the page size. The export is an advisory offline copy; authoritative records remain available, and users can obtain a complete export using the documented alternate page size. No downstream automation consumes it. | P2: incorrect supported output with bounded consequences and a practical workaround. Do not infer destruction of authoritative data. | Compare concatenated base/head pages at zero, one, an exact multiple, and a non-multiple; demonstrate the documented workaround preserves every row. |
| 05 | A permission check is refactored to an equivalent positive expression. Both versions reject unsupported actions and permit only the documented role/action pairs. This is a core access path, but the complete supported role/action domain has unchanged results. | No findings: sensitive context and release importance do not constitute a defect. | Exhaust the small declared role/action matrix, including the unknown-action path, and compare results. |
| 06 | A display adapter changes from returning a mapping to returning JSON text; the caller changes in the same patch to decode it. The complete supported call chain still returns the documented summary. This is required before the next scheduled operation, with no current incident. | No findings: a type change and a mandatory operational step do not establish a regression when the consumer is updated consistently. | Run complete base/head call chains across the declared supported inputs and compare values and types at the public boundary. |

Before constructing fixtures, a human must agree or revise the impact premises
and proposed priority interpretation. Before freezing, inspect every caller and
requirement for additional defects, accidentally implied consequences, and
hidden priority cues. Resolve ambiguity before evaluation rather than widening
accepted labels after seeing outputs. Cases 01 and 03 deliberately separate
future severe conditional loss from immediate broad ongoing failure. Cases 02
and 04 bound impact explicitly; the controls check unsupported escalation.

## Proposed scoring, subject to agreement

One adapted-skill review per case, at most six total, with no upstream arm.
Required proposed result: four supported defects detected, zero unsupported
findings, exact priorities P1/P3/P0/P2 for cases 01–04, and explicit no-findings
reports for cases 05–06. An alternative label counts only with a mapping agreed
before review. Human disagreement remains visible; never infer a tolerance
from the reports or replace a failed score with a later interpretation.

Record each dimension separately for each slot:

- Detection: identifies the seeded causal failure rather than merely its syntax.
- Evidence: cites a precise changed location, supported trigger, expected and
  actual consequence, and a correct static trace or reproduction. Static
  evidence is sufficient; do not award extra priority for executing a check.
- Priority: matches the frozen expected label and supports impact and urgency
  without invented breadth or consequences. A wrong label is not a detection
  miss or false positive when the underlying finding is correct.
- False positives: any additional unsupported required correction counts,
  regardless of heading. Clearly optional suggestions and unresolved questions
  do not count as findings. Deduplicate a single cause reported twice.
- Scope and authority: respects the supplied comparison, states actual checks
  and limits, and performs no fixes, external requests, posting, or approval.
- Isolation: initial context and tool traces show no grading material, parent
  conclusions, repository instructions, sibling cases, or prior reports.

Any missing report, context leak, or unverified essential premise is unresolved,
not an invented clean result. Retain errors and score only supported dimensions;
use null for unavailable measures. A diagnostic succeeds only if every agreed
criterion passes; completion of six attempts alone is not a pass. Final human
acceptance can retain a failed criterion without rewriting it.

## Evaluator proposal and preparation gate

Proposed settings: fresh standalone local CLI processes, requested model
`gpt-6.1-sol`, medium reasoning, sequential case order 01–06. These settings
match the historical batch 02 request for continuity; no new backend build or
availability is asserted. Local CLI version inspection returned
`0.164.0-alpha.11.1` on 27 October 2026. Record the executable path and hash,
version/help, selected configuration, actual exposed model/reasoning settings,
and any unavailable backend identifier before freezing the run agreement.
If the requested settings cannot be obtained, return for agreement rather than
substituting another model.

Reuse the [batch 02 isolation method](05-behavioural-evaluation/batch-02/isolation/README.md)
only after checking it against the installed runtime. This proposal includes no
subagent dispatch, resume, fork, inherited chat, or fallback to the current
conversation. Create a fresh temporary home for each slot outside the repository;
provide only that case's input and the assessed skill snapshot alongside a
writable scratch directory. Preserve user-home discovery limits explicitly:
a separate Codex home alone does not prove that other scanned skills or parent
instructions are absent. Inspect the case-free context before supplying a case,
then inspect the exact prompted context, and retain the actual initial session
messages/settings and subsequent reads. Stop before dispatch if isolation or
settings cannot be verified. Post-dispatch leakage invalidates that attempt;
it does not authorise a replacement.

No authentication changes are proposed for execution yet. Inspect the actual
runtime first; agree any necessary reuse of existing login separately without
copying secrets into evidence. An empty home, debug renderer success, or a CLI
version output does not establish a usable authenticated evaluator.

Before the first review, obtain human agreement to all of the following:

- Priority interpretation, selected correction or no-change candidate, and the
  exact candidate revision or per-file SHA-256 manifest.
- Six checked fixture snapshots, generated patches, target requirements,
  withheld key, premise checks and their actual outputs, with SHA-256 manifests.
- Frozen scoring criteria, exact six prompts, launch commands, context audit
  procedure, executable/settings, permitted bundled defaults, and tool limits.
- Maximum six attempts, no replacement/retry/correction batch, no upstream
  comparison, and treatment of failed or incomplete slots.

Do not expose the key, checker, this proposal, or the enclosing source checkout
to review inputs. Keep the authorship/scoring limitation explicit: the same
assistant proposes fixtures and scores; isolation of review contexts does not
make the key or adjudication independent. Human review remains required.

## Evidence retention and stopping rule

For each slot retain the exact prompt and launch command, preflight/context
audits, exposed versions/settings, complete raw events and report, stderr,
command/tool outputs and errors, and input/candidate hashes before and after.
Keep credential contents and private account identifiers out of evidence.
Freeze a raw-output SHA-256 manifest before scoring. Retain every attempted
slot and error, and stop at six even if a criterion fails. No preferred-output
selection, automatic repeat, or revised fixture is part of this diagnostic.

One sample at each level cannot estimate calibration reliability or prove that
a clarification caused improvement. These small synthetic Python cases cannot
establish behaviour on other languages, production deployments, large changes,
or security audits. Synthetic incident premises establish the intended scenario,
not a real service outage. Task 07 does not reopen the original batch scores,
package 05 completion, package 06's separate candidate gates, or publication.
