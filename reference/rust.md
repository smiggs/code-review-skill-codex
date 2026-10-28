# Rust review guide

Use this guide under the [review contract](review-contract.md). Ground findings
in reachable failure conditions, unsafe invariants, or project requirements.
Ownership choices, preferred crates, formatting, and allocation patterns alone
are not defects.

## Versions and review scope

Read `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, feature flags, target,
edition, minimum supported Rust version (MSRV), and CI commands. The executable
audit baseline is Rust 1.85.0 on Linux/x86_64 with editions 2021 and 2024 and
Tokio pinned to 1.48.0. This is a reproducibility baseline, not a universal MSRV
or an instruction to change project versions. Check dependency APIs and feature
availability against the actual lockfile. See the
[reference status](reference-status.md) for verification limits.

## Ownership, borrowing, and panic paths

Borrowed fields and explicit lifetimes are valid when the source outlives the
consumer. Cloning can provide necessary ownership for a task; `Arc` shares an
allocation but does not make its contents safe for unsynchronised mutation.
`Rc`, `RefCell`, `Cow`, and owned values need their actual access and lifetime
contracts. Compiler rejection of use-after-move is different from a reachable
runtime bug in compiling code. See [lifetime contracts](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html).

This complete fragment is a valid borrowed-field control and a justified
`expect`: the literal parse invariant is independent of caller input.

```rust
pub struct Parser<'a> {
    pub input: &'a str,
}

pub fn built_in_port() -> u16 {
    "8080".parse().expect("built-in port should fit u16")
}
```

Trace `unwrap`, `expect`, indexing, integer arithmetic, and lock poisoning to
inputs and the project's panic policy. Parsing untrusted input with `unwrap`
can terminate a task or process; a proven invariant, test assertion, or explicit
fail-fast policy can justify a panic. An `expect` message does not establish its
invariant. Preserve useful error sources when recovery or diagnosis requires
them. Structured public errors help callers match failures; `thiserror` and
`anyhow` are choices, and `anyhow` supports downcasting. See
[`Option` panic behaviour](https://doc.rust-lang.org/std/option/enum.Option.html#method.expect)
and [anyhow's error API](https://docs.rs/anyhow/1.0.100/anyhow/struct.Error.html).

## Unsafe invariants and safe boundaries

Check validity, alignment, initialisation, bounds, aliasing, provenance,
allocation layout, ownership transfer, and destruction for each operation.
Trace the safe callers and mutations that maintain those invariants. A safety
comment is evidence only when the code establishes what it claims. FFI wrappers
also depend on the foreign function's actual contract. Rust's
[undefined-behaviour list](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)
is not an exhaustive formal memory model.

A `debug_assert!` cannot establish release-build bounds for a safe wrapper around
`get_unchecked`. Use a release-mode check or a safe operation. This fragment
shows a safe alternative and a separately unsafe API with an explicit caller
obligation; callers of the latter must prove bounds.

```rust
pub fn checked_byte(bytes: &[u8], index: usize) -> Option<u8> {
    bytes.get(index).copied()
}

/// Returns the byte at the caller-validated index.
///
/// # Safety
///
/// The caller must ensure that index is less than bytes.len().
pub unsafe fn unchecked_byte(bytes: &[u8], index: usize) -> u8 {
    // SAFETY: The caller guarantees an in-bounds index into a valid slice.
    unsafe { *bytes.get_unchecked(index) }
}
```

[`get_unchecked`](https://doc.rust-lang.org/std/primitive.slice.html#method.get_unchecked)
requires bounds even when its result is unused. Generic `transmute<T, U>` is not
a general conversion recipe: the compiler must establish size compatibility and
the programmer must establish destination validity and ownership. Prefer safe
conversions when available; see [`transmute`](https://doc.rust-lang.org/std/mem/fn.transmute.html).
Edition 2024 warns by default about unsafe operations inside unsafe functions
without an explicit unsafe block; older editions can enable the same lint.
See [the edition rule](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-op-in-unsafe-fn.html).

## Tokio I/O cancellation

For Tokio 1.48.0, `AsyncReadExt::read` is cancel safe: when another `select!`
branch wins, the losing read has consumed no bytes. `read_exact` and multi-byte
numeric reads can consume partial input before cancellation. Restarting them
from scratch can corrupt framing. Check each operation's documented guarantee;
these are distinct from memory safety. See the
[versioned I/O source and cancellation contracts](https://docs.rs/tokio/1.48.0/src/tokio/io/util/async_read_ext.rs.html).

A cancel-safe primitive does not make a multi-step message reader transactional.
Progress kept only in a dropped future can disappear. This fixed four-byte
reader retains its buffer and offset in an object that must survive cancellation.
After an interrupted call, resume with the same reader and state. Completion
resets the offset for the next frame; EOF or I/O failure requires a caller policy
for the incomplete frame. No timeout, rollback, or reconnection recovery is
implied. The fields are private so safe callers cannot create an invalid offset.

```rust
use tokio::io::{self, AsyncRead, AsyncReadExt};

#[derive(Default)]
pub struct FourBytes {
    bytes: [u8; 4],
    filled: usize,
}

impl FourBytes {
    pub async fn read<R: AsyncRead + Unpin>(&mut self, reader: &mut R)
        -> io::Result<[u8; 4]>
    {
        while self.filled < self.bytes.len() {
            let n = reader.read(&mut self.bytes[self.filled..]).await?;
            if n == 0 {
                return Err(io::ErrorKind::UnexpectedEof.into());
            }
            self.filled += n;
        }
        self.filled = 0;
        Ok(self.bytes)
    }
}
```

Keeping and polling the same pinned future can preserve its internal progress;
recreating it cannot. Pinning alone does not make arbitrary work cancel safe.
`BufReader` alone does not preserve a parser's discarded message state. Treat
claims of atomic receive/acknowledge or commit/acknowledge as unverified until
the protocol and database guarantees establish failure, drop, and retry behaviour.
There is no generic transaction API that proves this for an arbitrary connection.

## Task ownership and shutdown

Dropping a Tokio `JoinHandle` detaches the task. It does not cancel it. Awaiting
`JoinHandle<Result<T, E>>` has two failure layers: `JoinError` and the task's `E`.
Define who observes both and who owns shutdown if the supervisor itself is
cancelled. A task's `'static` bound requires that captured borrows do not expire;
it does not require the task to run forever. Moving owned data or sharing an
`Arc` can satisfy the bound. See [JoinHandle ownership](https://docs.rs/tokio/1.48.0/tokio/task/struct.JoinHandle.html).

For ordinary yielding async tasks, abort requests cancellation; awaiting their
handles observes termination and destructor completion. This helper requests
all aborts before joining, and collects every join failure, including expected
cancellation. Its owner must keep driving it to completion. An already completed
task may return normally; an unyielding task can prevent completion.

```rust
use tokio::task::{JoinError, JoinHandle};

pub async fn stop_tasks(handles: Vec<JoinHandle<()>>) -> Vec<JoinError> {
    for handle in &handles {
        handle.abort();
    }
    let mut failures = Vec::new();
    for handle in handles {
        if let Err(error) = handle.await {
            failures.push(error);
        }
    }
    failures
}
```

`try_join!` runs its branch futures concurrently on the same task and returns on
the first error. Dropping direct branch futures stops polling them; earlier
side effects remain. Joining spawned handles does not acquire ownership of
cancelling the underlying tasks, and an `Ok(Err(E))` is not an outer join error.
Direct `await`, `join!`, supervised tasks, and deliberate background services
are valid choices with different lifetimes. See
[`try_join!`](https://docs.rs/tokio/1.48.0/tokio/macro.try_join.html).

Blocking or long CPU work can starve executor threads. `spawn_blocking` moves
work off those threads but does not bound CPU concurrency for the application.
Once started, blocking tasks cannot be stopped by handle abort; use cooperative
stopping and a workload bound. Runtime shutdown may wait for them. See
[`spawn_blocking`](https://docs.rs/tokio/1.48.0/tokio/task/fn.spawn_blocking.html).

Short critical sections with `std::sync::Mutex` can be valid in async code.
Holding a blocking lock across an await can deadlock under the actual scheduler
and access pattern, or make a spawned future fail `Send` checking. An async mutex
permits awaiting while locked but does not prevent lock cycles or excessive
serialisation. See [Tokio's mutex guidance](https://docs.rs/tokio/1.48.0/tokio/sync/struct.Mutex.html).

## Traits, allocation, and checks

Native async trait methods and return-position `impl Trait` in traits require
Rust 1.75+. Consider callers' `Send` needs and dynamic dispatch compatibility;
boxed futures can deliberately provide a dyn-compatible API. Traits and generics
have different API and code-size trade-offs, without universal performance
rankings. See [the stabilisation and limitations](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/).

`String + &str` consumes the left string and can reuse its storage. It does not
necessarily allocate on every iteration. `push_str`, `join`, `Cow`, preallocation,
and lazy iterators need workload and ownership evidence. An intermediate
collection can be intentional. Check arithmetic bounds before summing capacities.
See [`String` storage and addition](https://doc.rust-lang.org/std/string/struct.String.html).

Run the project's format, Clippy, and test gates under supported features and
versions. Use controlled readers for partial I/O and cancellation, bounded waits
for shutdown, release checks for unsafe wrappers, and clean controls for valid
borrowing and intentional panics. Miri and sanitiser results cover exercised
paths and supported targets; missing runs must be disclosed. A successful build
or example test does not establish review accuracy or soundness of all unsafe
code.
