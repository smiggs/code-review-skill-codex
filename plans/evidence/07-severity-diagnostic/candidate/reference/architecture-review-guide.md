# Architecture review guide

Use this guide for a requested architecture review or a concrete design
consequence in a change review. Establish the component, comparison, and agreed
boundaries under the [review contract](review-contract.md). The
[reference status](reference-status.md) records the maintenance scope.

## Establish the project's architecture

Read the target's specifications, architecture decisions, dependency rules, and
migration requirements. Identify actual entry points, consumers, state ownership,
and deployment boundaries. Do not assume every project uses layered services,
repositories, dependency injection, or Clean Architecture.

A documented rule that domain code cannot import the database adapter can support
a requirement finding when the change adds that import. Without such a rule or
a concrete behavioural failure, a different layering choice is a design question
or suggestion rather than an automatic defect.

## Trace consequences

Use these prompts where relevant:

- Follow inputs, outputs, side effects, and failure propagation across boundaries.
- Check whether a replacement implementation preserves the contract required by
  its callers, including errors, ordering, and resource ownership.
- Trace shared state and dependencies when evaluating coupling and isolation.
- Check whether new dependencies introduce a demonstrated import cycle, deployment
  failure, or violated separation requirement.
- For a migration, compare old and new consumers, schema compatibility, rollout
  order, rollback, and supported configurations.
- For an external service, inspect timeouts, retries, idempotency, and partial
  failure against the target's documented guarantees.

Single responsibility, substitutability, interface separation, and dependency
inversion can help formulate questions. Their names do not prove that a concrete
implementation is wrong. An abstraction is useful only when its consequences
serve the supported requirements.

## Distinguish defects from preferences

A file's length, parameter count, nesting depth, method count, or coupling metric
can suggest where to inspect. None supplies a severity or mandatory refactor.
The same applies to duplication, a switch statement, an interface with one
implementation, or a class named `Manager`.

Directory layout, naming, inheritance, composition, and event-driven designs are
choices governed by project conventions and behavioural constraints. Explain an
actual failure or requirement violation before reporting a finding. Do not demand
a particular pattern because it might help an unspecified future feature.

## Verify and report

Test the affected contract or trace a concrete supported execution path. Use
relevant existing architecture checks when their purpose and side effects are
understood. Distinguish an observed build or runtime failure from a diagram-based
hypothesis. Report missing consumers or deployment information as limits.

Use the contract's priority mapping and the
[report template](../assets/pr-review-template.md). Put findings first; no findings
is valid. A review does not authorise moving files, changing public interfaces,
posting comments, or satisfying target-project human approval gates.
