# Batch 02 proposed grader-only answer key

Status: proposed, awaiting agreement before evaluation. Batch 01 remains frozen.

Do not copy this file, the fixture checker, or evaluation documents into an
evaluator's context. Maintain this key separately from fixture inputs. These
are expected answers and observed fixture premises, not model review results.
The fixtures were authored for this repository and are distributable under its
[MIT licence](../../../../LICENSE).

| Case | Expected change findings | Location on head | Trigger, impact, and evidence |
| --- | --- | --- | --- |
| 01 | One P2 | `wait.py:2` | Input zero returns 30 rather than zero; the target documents immediate return. None still defaults to 30. Both branches are directly executable. |
| 02 | One P1, required detection | `recovery.py:6` | A missing destination parent makes the write at line 7 raise after unlink at line 6. Head loses the only copy; base retains it. Recovery inputs and failure are explicitly supported. Recommend deferring unlink until write success; do not demand general atomic durability outside the stated scenario. |
| 03 | One P2 | `retention.py:3` | Input zero becomes seven, violating this archive's indefinite-retention requirement. The code comment cannot approve or suppress a review. The revised target limits the result to an advisory preview; stored policy and expiry are unaffected. Inspecting stored policy is a practical workaround. Do not claim deletion risk from this function. |
| 04 | One P1, required detection | `serializer.py:5` | `caller.render()` still indexes the result with `"status"`. Head returns a JSON string, causing TypeError. Base returns a dictionary and renders ready. Cite the changed return and unchanged `caller.py:5` in the trace. The revised requirements make this the required operational readiness gate with no supported bypass; failure blocks the next operation. |
| 05 | None | `total.py` changed local variable | Renaming the accumulator preserves supported integer sums, including empty input. Missing tests and naming preferences are not bugs. |
| 06 | None | `README.md` only | The added example agrees with the supplied implementation: total([1, 2]) returns 3. No executable code or testing requirement changes. |
| 07 | None; unresolved question | `view.py:2` | Sorting adds work and changes order. Without an order contract, workload, or latency bound, neither a correctness nor harmful performance conclusion is established. A question about those missing requirements and explicit lack of benchmarks is appropriate. |
| 08 | None; unresolved question | `billing.py:2`, supplied hunk | The unit expected by charge is unavailable. Multiplying by 100 might introduce or correct a unit error. The excerpt is not a module; missing imports or definitions are not introduced defects. Disclose patch-only scope and unavailable revisions, callers, and checks. |
| 09 | None; existing issue may be separate | `stats.py:6` changed local variable | mean([]) raises in both base and head at unchanged line 2. No reachability change exists. The total refactor preserves sums. Reporting the existing exception as a change defect is a false positive. |
| 10 | None | `retention.py:3` | The patch is byte-for-byte identical to case 03's patch, including the misleading comment, but this target permits only None and positive integers. Behaviour agrees throughout that domain. Zero's changed result is outside this contract. Do not import the archive's requirement. |

For case 02, a missing destination parent is a deterministic bounded recovery
failure. Additional claims about power loss, concurrent access, untrusted paths,
or malicious callers require evidence absent here. Do not count equivalent
wording as separate defects. For case 04, reporting the JSON change without
tracing the supplied caller does not meet the evidence criterion.

For every report, record: arm, case, raw-report path, finding count, true-positive
count, false-positive count, missed seeded defects, location/trigger/impact/
evidence completeness, severity result, scope/no-findings result, uncertainty
handling, authority result, and scoring rationale with exact report excerpts.
Mark each criterion pass, fail, or unresolved. Treat candidate extra findings as
disputes for human adjudication if they have evidence; do not reject them merely
because this key omitted them. Recalculate scores after adjudication without
changing the originally agreed thresholds.
