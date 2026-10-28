# Go review guide

Use this guide under the [review contract](review-contract.md). Report a concrete
failure path or violated project requirement. Interface shape, formatting,
allocation counts, and test style alone do not establish a defect.

## Versions and review scope

Read `go.mod`, any workspace file, build tags, toolchain selection, and CI
commands. The executable audit baseline is Go 1.22.12 on Linux/amd64, with
module language versions 1.21 and 1.22 for loop comparisons. These are
reproducibility baselines, not recommendations to downgrade or claims of support
for every release. Check APIs against the target's supported versions.

Start with error contracts, resource ownership, goroutine termination, channel
closure, cancellation propagation, and shared storage. The
[reference status](reference-status.md) records validation limits.

## Errors and nil interfaces

An ignored error is actionable when failure changes a required result, loses
state, or prevents recovery. Returning an existing error unchanged is valid when
it already carries sufficient information. Logging and returning can also be
intentional; demonstrate duplicate reporting before calling it a defect.

Use `%w` when callers need the wrapped cause through `errors.Is` or `errors.As`.
Wrapping exposes that cause as part of the API; `%v` or translation to a public
error can deliberately hide implementation details. Direct comparison is valid
for an explicitly unwrapped sentinel contract. Check the expected chain before
requiring `errors.Is`. See [Go's error wrapping contract](https://go.dev/blog/go1.13-errors).

An interface is nil only when both its dynamic type and value are absent.
Returning a typed nil pointer as `error` produces a non-nil interface. Return
literal `nil` for success; a nil receiver method may be valid if it supports that
case. The [Go FAQ](https://go.dev/doc/faq#nil_error) explains this distinction.

## Goroutines, channels, and cancellation

Trace who starts each goroutine, how it can finish on every exit path, and who
waits for completion. A cancellation branch helps only if the context can
actually be cancelled and every blocking operation can respond. A background
context alone supplies no shutdown signal.

The owner that can prove all sends have finished may close a channel. With
multiple senders, this often requires a coordinator after a wait group. Receivers
must not close while sends remain possible. Closing is unnecessary when no
consumer needs an end-of-stream signal. A nil channel blocks sends and receives;
a closed channel drains buffered values and then yields zero values with
`ok == false`. Sending on a closed channel, closing it twice, or closing a nil
channel panics. See the [channel specification](https://go.dev/ref/spec#Channel_types).

Register positive `WaitGroup.Add` calls before launching work when `Wait` could
otherwise see a zero count. Do not copy a used mutex or wait group. Concurrent
map access involving writes and overlapping slice writes need synchronisation;
independent storage and deliberately serial access are valid controls. Consult
[the versioned sync contract](https://pkg.go.dev/sync@go1.22.12).

Propagate the request context through operations whose lifetime belongs to it.
Creating a fresh root can discard deadlines and cancellation. A detached service
job can have a separately owned lifetime, but needs its own shutdown contract.
Arrange to call the cancel function returned by `WithCancel` or `WithTimeout`
on all owned paths. Parameter position and storing contexts are API conventions;
identify the lifetime failure before making a finding. Context cancellation is
cooperative and does not forcibly stop arbitrary code. See
[context ownership](https://pkg.go.dev/context@go1.22.12).

### Bounded worker example

This complete package uses Go 1.22. `workers` must be positive, including for
empty input; validation precedes cancellation. A pre-cancelled context returns
its error. Otherwise empty input succeeds. For non-empty input, `process` must
be non-nil, safe for concurrent calls, and return promptly when its context is
cancelled. Input storage must remain stable until return.

The pool admits at most `min(workers, len(items))` callbacks at once, stops
feeding on cancellation, closes its own jobs channel, and joins all workers.
The first cause recorded by the derived context wins, whether from the parent
or a callback. Simultaneous cancellation and job readiness can admit work, so
this does not promise a strict cut-off instant. Completed side effects are not
rolled back. A callback that ignores cancellation or panics is outside this
example's contract; joining cannot impose a deadline on such a callback.

```go
package audit

import (
    "context"
    "fmt"
    "sync"
)

func ProcessAll(parent context.Context, items []int, workers int,
    process func(context.Context, int) error) error {
    if workers <= 0 {
        return fmt.Errorf("workers must be positive: %d", workers)
    }
    if err := parent.Err(); err != nil {
        return err
    }
    if len(items) == 0 {
        return nil
    }
    if workers > len(items) {
        workers = len(items)
    }
    ctx, cancel := context.WithCancelCause(parent)
    defer cancel(nil)
    jobs := make(chan int)
    var wg sync.WaitGroup
    for w := 0; w < workers; w++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for {
                select {
                case <-ctx.Done():
                    return
                case item, ok := <-jobs:
                    if !ok || ctx.Err() != nil {
                        return
                    }
                    if err := process(ctx, item); err != nil {
                        cancel(fmt.Errorf("item %d: %w", item, err))
                        return
                    }
                }
            }
        }()
    }
feed:
    for _, item := range items {
        select {
        case <-ctx.Done():
            break feed
        case jobs <- item:
        }
    }
    close(jobs)
    wg.Wait()
    return context.Cause(ctx)
}
```

## Loop variables and shared storage

For language versions before Go 1.22, closures can observe a reused loop variable
after it changes. With Go 1.22 semantics, variables declared by the loop have
per-iteration identity. Check the module's `go` directive and file constraints,
not just the installed compiler. Assignment to an existing variable with `=`
still reuses that variable. Neither new semantics nor passing an argument copies
the objects reached through pointers, maps, or slice elements. See
[the loop-variable transition](https://go.dev/blog/loopvar-preview).

A subslice shares its backing array. Copy with `make` and `copy` when independent
elements are required; that copy remains shallow for reference-bearing elements.
A full slice expression can restrict append capacity but does not isolate writes
to existing elements. Retaining a small slice can retain a larger allocation;
show retention under the actual workload before alleging a leak. See
[Go slice storage](https://go.dev/blog/slices-intro).

## Resources and observable values

`defer` runs when the surrounding function returns. Deferring every close in a
long loop can exhaust descriptors; a per-item helper can bound ownership.
Preserve errors from writes and closes when the resource's durability contract
requires them. Check ownership before closing a resource supplied by a caller.

Writing to a nil map panics, while reads and deletes are valid. Nil and non-nil
empty slices can have different serialised representations; match the actual
encoder and API contract. For `time.Time`, use `Equal` when comparing instants;
`==` also compares representation, which can be intentional for a key or exact
value check. Verify lengths before slicing: a prefix operation can panic on
short input. `strings.Clone` (Go 1.18+) provides an explicit independent string
copy when measured retention warrants it. These prompts need the target's
[standard-library contracts](https://pkg.go.dev/std@go1.22.12).

## API, performance, and verification choices

Small consumer interfaces often help express dependencies, but concrete inputs,
interface returns, and mixed receiver types can be deliberate API choices.
Check method sets, mutation requirements, and copying of synchronisation state.
Generics require Go 1.18+ and do not guarantee zero runtime cost or allocation.
Pointer returns do not by themselves prove an allocation problem. Preallocation,
`sync.Pool`, and string builders need workload evidence; a pool can discard
entries and requires safe object reuse. Follow project formatting and lint gates
without turning every convention into a correctness finding. See
[Go review conventions](https://go.dev/wiki/CodeReviewComments).

Use the project's tests, static checks, and supported race detector. Race-free
runs cover only executed paths. Prefer tests for input boundaries, callback
errors, cancellation, closure, and joined shutdown over mandated test syntax,
mocking libraries, or coverage ratios. Parallel subtests require independent
state and version-correct captures. See
[the race detector's limits](https://go.dev/doc/articles/race_detector).
