# Fixture answer key: withhold from reviewers

## Go worker

The adapted inherited pool launches no workers for zero or negative counts.
Non-empty input then waits forever for results; empty input silently succeeds.
Its context is not used to stop scheduling or workers. Passing the context to a
cooperative callback alone does not give the pool a cancellation or joined
shutdown policy. The clean base validates input, propagates cancellation with a
cause, closes its jobs channel, and joins workers. `verify.py` requires the
non-empty input and cancellation tests to fail by bounded termination assertions
for the head, and to pass for the base. Other possible findings require their
own demonstrated trigger; no priority score is assigned here.

## Rust reader

The head resets the persistent offset to zero on every call. After the first
call consumes `ab` and is dropped at the controlled wait, the next call starts
at `c` and returns `cdef` rather than `abcd`. The base retains the offset across
cancelled calls, then reads `efgh` as the next frame. The sensitivity assertion
must fail for the changed bytes, rather than for a compiler or dependency error.
