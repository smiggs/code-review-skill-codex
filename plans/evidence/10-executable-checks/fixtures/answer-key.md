# Answer key (withheld from any independent review)

This file is for the human evaluator only: do not include it in the
material provided to a reviewer whose answers are meant to be independent.

## jpa-membership

- Defect location: `head/ParentReader.java`, the HQL string inside
  `readStaleParents`.
- Defect: `JOIN FETCH` is an inner fetch join, so users with no orders
  (`Cyd` in the seeded data) disappear from the result although the target
  requirement says every requested parent must be preserved. The base's
  `LEFT JOIN FETCH` is the retained correction from the guide.
- Expected finding shape: missing/lost parent membership triggered by
  parents with no related rows; fix is left join fetch (or an equivalent
  graph/batch plan that preserves membership).
- Non-findings: the eager `@OneToMany` mapping on its own, the single
  statement executed (both variants run one query in the fixture), or the
  absence of pagination in the fixture.

## failure-observability

- Defect location: `head/BatchRunner.java`, the `catch` block inside the
  submitted task body.
- Defect: the failure of `job-3` is caught and never published; the caller's
  returned list shows only `job-1-completed` and `job-2-completed`, so a
  failed nightly run is silently reported as clean. The base records
  `job-3-failed:IllegalStateException` in the returned outcomes.
- Expected finding shape: swallowed exception on a task boundary with the
  caller's contract requiring observable outcomes; fix is publishing the
  failure (recorded outcome, propagated call, or equivalent visible handling).
- Non-findings: `Executors.newFixedThreadPool` use, try-with-resources
  executor ownership, the thread-safe `CopyOnWriteArrayList` outcomes list,
  or the missing per-job timeout.
