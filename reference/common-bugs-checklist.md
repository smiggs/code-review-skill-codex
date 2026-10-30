# Common Bugs Checklist

Language-specific bugs and issues to watch for during code review.

Use patterns in this inherited guide as inspection prompts under the
[review contract](review-contract.md), not as findings or fixed severity rules.
Confirm the target's versions, caller behaviour, trigger, and impact. The
[reference status](reference-status.md) records unaudited framework examples.
Missing tests, an external test dependency, or a familiar pattern alone is not
proof of a defect.

## Universal Issues

### Logic Errors
- [ ] Off-by-one errors in loops and array access
- [ ] Incorrect boolean logic (De Morgan's law violations)
- [ ] Missing null/undefined checks
- [ ] Race conditions in concurrent code
- [ ] Incorrect comparison operators (== vs ===, = vs ==)
- [ ] Integer overflow/underflow
- [ ] Floating point comparison issues

### Resource Management
- [ ] Memory leaks (unclosed connections, listeners)
- [ ] File handles not closed
- [ ] Database connections not released
- [ ] Event listeners not removed
- [ ] Timers/intervals not cleared

### Error Handling
- [ ] Swallowed exceptions (empty catch blocks)
- [ ] Generic exception handling hiding specific errors
- [ ] Missing error propagation
- [ ] Incorrect error types thrown
- [ ] Missing finally/cleanup blocks

## TypeScript/JavaScript

Use the [TypeScript and JavaScript guide](typescript.md) for runtime validation,
indexed access, shared mutation, and promise ownership. Trace the consumer and
failure path: assertions do not validate JSON, `void` does not consume rejection,
and cancellation does not by itself prevent every stale continuation.
Propagating rejection to an awaiting caller and using `Promise.all` for required
results are valid controls. Compiler strictness and lint preferences need the
target project's configuration; they are not universal defect criteria.

### React

Use the [React guide](react.md) for Hooks, effects, identity, actions, Suspense,
and server/client boundaries. Confirm React, React DOM, framework, and query
library versions separately. Inspect stale result/error publication, unintended
state resets, form ownership, and actual recovery boundaries. Conditional child
rendering, React 19's conditional `use`, explicit loading state, inline callbacks,
and a client wrapper receiving server-rendered children can be valid controls.
Memoisation, boundary placement, and cache defaults need demonstrated impact.

## Vue 3

Use the [Vue guide](vue.md) for reactive inputs, compiler-sensitive props
transformations, watcher ownership, and lifecycle cleanup. Trace whether a
consumer needs a live value or an intentional snapshot. Inspect overlapping
request success, error, and loading writes and the exact listener target cleaned
up. Vue 3.5 reactive props destructuring is distinct from ordinary object
destructuring. Getter inputs, explicit prop/update pairs, `withDefaults`, and
non-virtual lists can be valid controls; missing type-only declarations or newer
API adoption alone do not establish defects.

## Python

Use the [Python review guide](python.md) for checked examples and version limits.
Inspect shared mutable defaults or class state, swallowed failures, resource
cleanup, exhausted iterators, cancellation, and input boundaries where relevant.
Intentional sharing and broad boundary handlers need their actual contracts;
string concatenation or missing annotations alone do not establish defects.

## Go

Use the [Go guide](go.md) for error chains, typed nil interfaces, channel
ownership, cooperative cancellation, worker bounds, joined shutdown, and shared
slice storage. Check the module language version before reporting loop captures;
assignment to an existing loop variable still reuses it. Intentional sharing,
concrete interfaces, direct sentinel comparisons under their contract, and
project formatting choices need their actual requirements.

## Rust

Use the [Rust guide](rust.md) for ownership, unsafe invariants, panic paths,
partial I/O, and task shutdown. Check the MSRV, edition, features, and Tokio
version. A debug-only check cannot establish a safe release-build boundary.
Distinguish cancel-safe single reads from multi-step framing, and dropping a
future or handle from stopping spawned or blocking work. Borrowed fields,
necessary clones, short standard mutex critical sections, and proven panic
invariants are valid controls. Crate, trait, and allocation preferences alone
do not establish defects.

## Java

Use the [Java guide](java.md) for JDK feature boundaries (records, switch
patterns, text blocks, virtual threads with their preview and API limits),
resource closure under failure, executor ownership and interruption, and the
difference between a thread-safe collection and atomic caller compound
actions. Check Spring transaction advice against the real proxy mode and
invocation path before reporting visibility or self-invocation problems, and
treat `readOnly` as a hint with a project-specific effect. For persistence,
verify fetch-join result membership (inner joins drop child-less parents),
statement counts for eager associations, pagination behaviour with
collection fetches, and entity equality over proxies. Fixed thread pools,
unannotated beans, and hand-written identifier-based equality are valid
controls; feature choice, annotation style, and framework preference alone
do not establish defects.

## C, C++, and Qt

Use the [C guide](c.md), [C++ guide](cpp.md), and [Qt guide](qt.md) for
buffer and copy contracts, partial-I/O and allocation-failure handling,
undefined-behaviour triggers, ownership transfer and move correctness, view
and capture lifetimes, and Qt parent ownership, deferred deletion, thread
affinity, and connection types. Check the declared language mode
(`-std=c11`/`c17`), the C++ standard, and the project's Qt version before
reporting version-boundary findings. Overlapping `memcpy` is undefined
behaviour while `memmove` is defined for it; a defaulted move of a class
whose destructor releases a raw handle double-closes; a negative count
converted to `size_t` for `reserve` throws `std::length_error`. A context
object on a lambda connection disconnects it with the receiver;
subclassing `QThread::run()` is valid when `run()` owns the work and the
subclass adds no slots. Deliberate macros, by-value containers, and missing
`reserve` alone do not establish defects.

## SQL

### Injection Vulnerabilities
```sql
-- ❌ String concatenation (SQL injection risk)
query = "SELECT * FROM users WHERE id = " + user_id

-- ✅ Parameterized queries
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### Performance Issues
- [ ] Missing indexes on filtered/joined columns
- [ ] SELECT * instead of specific columns
- [ ] N+1 query patterns
- [ ] Missing LIMIT on large tables
- [ ] Inefficient subqueries vs JOINs

### Common Mistakes
- [ ] Not handling NULL comparisons correctly
- [ ] Missing transactions for related operations
- [ ] Incorrect JOIN types
- [ ] Case sensitivity issues
- [ ] Date/timezone handling errors

## API Design

### REST Issues
- [ ] Inconsistent resource naming
- [ ] Wrong HTTP methods (POST for idempotent operations)
- [ ] Missing pagination for list endpoints
- [ ] Incorrect status codes
- [ ] Missing rate limiting

### Data Validation
- [ ] Missing input validation
- [ ] Incorrect data type validation
- [ ] Missing length/range checks
- [ ] Not sanitizing user input
- [ ] Trusting client-side validation

## Testing

### Test Quality Issues
- [ ] Testing implementation details instead of behavior
- [ ] Missing edge case tests
- [ ] Flaky tests (non-deterministic)
- [ ] Tests with external dependencies
- [ ] Missing negative tests (error cases)
- [ ] Overly complex test setup
