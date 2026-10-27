# Performance review guide

Use this guide to investigate a performance consequence within the agreed scope
of the [review contract](review-contract.md). Establish a supported workload and
an observable regression or violated bound before assigning defect priority.
See the [reference status](reference-status.md) for audit limits.

## Establish the comparison

Record input size, distribution, request rate, concurrency, cache state, runtime,
and relevant resource limits. Compare base and head under equivalent conditions.
Read the project's latency, throughput, memory, or cost requirements; do not invent
universal API-response, bundle-size, list-length, or query-time thresholds.

A measured regression or a trace that demonstrably exceeds a documented bound
can support a finding. Complexity alone does not establish harmful performance.
For example, a nested scan over an explicitly bounded small collection may be
acceptable. If production scale is unknown and could change the conclusion,
record the missing workload as a question.

## Frontend paths

Trace the interaction or render path the change affects. Inspect loading order,
main-thread work, layout, images, fonts, listeners, and retained objects where
relevant. Compare actual supported devices and navigation conditions.

[Core Web Vitals](https://web.dev/articles/vitals) identifies LCP, INP, and CLS
and evaluates recommended thresholds at the 75th percentile of visits. These
population measurements are context, not automatic defect gates for a diff.
FCP and TBT are other metrics; do not label every metric a Core Web Vital.

Code splitting, virtualisation, new image formats, workers, and memoisation need
an applicable bottleneck and compatibility check. An animation, a PNG, a large
list, or `transition: all` is not independently a blocking defect.

## Database and service paths

Trace query count, rows examined and returned, round trips, connections, result
materialisation, pagination, and repeated work for the supported input. An N+1
pattern needs an evidenced consequence, rather than an automatic priority.
An index is not mandatory on every filtered column; inspect the actual query
plan and data distribution.

Use the target database's tools only in a permitted environment. PostgreSQL's
[EXPLAIN documentation](https://www.postgresql.org/docs/18/using-explain.html)
distinguishes estimated plans from `EXPLAIN ANALYZE`, which executes the statement.
Do not run writes or costly experiments against a live database as a review side
effect. Bound result sizes and memory claims with evidence rather than assuming
that a generator or ORM API streams data.

## Caching and concurrency

Check cache keys, ownership, invalidation, staleness, capacity, and failure
behaviour. A cache that changes correctness is not an acceptable performance fix.
Before recommending HTTP caching, establish whether the response is public or
personalised. A validator such as an ETag must correspond to the representation;
a fixed value cannot safely stand in for changing content. See
[HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching).

Inspect whether concurrency reduces the relevant wait or instead increases load,
contention, task count, or memory. Confirm cancellation, cleanup, and backpressure.
Do not recommend async, caching, sets, or parallel execution by reflex.

## Verification and output

Use representative, repeatable checks when available. Record commands, conditions,
results, and relevant variance; do not present an unrun benchmark as evidence.
Verify that an optimisation preserves required ordering, precision, errors, and
supported inputs.

The [report template](../assets/pr-review-template.md) keeps supported findings,
material questions, and optional improvements distinct. Report verification limits
when measurements or production context are unavailable. No findings is valid;
priority follows impact and urgency rather than an optimisation checklist.
