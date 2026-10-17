# Python review guide

Use this guide for Python behaviour under the [review contract](review-contract.md).
Start with the target's supported interpreter versions, dependency versions,
project instructions, and recorded checks. The [reference status](reference-status.md)
describes the audit limits. These prompts do not impose a formatter, type checker,
docstring convention, or coverage percentage.

## Versions and annotations

Check the minimum interpreter and how annotations are consumed before recommending
syntax or imports. The version boundaries below come from the
[Python typing reference](https://docs.python.org/3.12/library/typing.html):

| Feature | Standard-library availability |
| --- | --- |
| Built-in generics such as `list[str]` | Python 3.9 |
| Unions such as `str \| None` | Python 3.10 |
| `typing.Required` and `typing.NotRequired` | Python 3.11 |
| Type-parameter syntax such as `def first[T](...)` and the `type` statement | Python 3.12 |

Earlier targets can use compatible `typing` forms or an appropriate installed
backport. Postponing annotation evaluation does not make newer statement syntax
parseable on an older interpreter. Type hints do not validate runtime inputs;
check actual validation at untrusted boundaries. Respect the project's chosen
checker and settings. A missing annotation or use of `Any` alone is not a defect.

## Resource ownership and failure paths

Trace who owns each file, connection, subprocess, and temporary artifact, including
early returns and exceptions. A context manager can make cleanup explicit:

```python
from pathlib import Path


def read_first_line(path: Path) -> str:
    with path.open(encoding="utf-8") as stream:
        return stream.readline().rstrip("\n")
```

Check that context managers release resources on the failure paths that matter.
A `return` in `finally` can suppress a pending exception. In a generator-based
manager, code after `yield` alone does not guarantee cleanup if the body raises;
use a suitable `try/finally`. Transaction rollback and resource release are separate
obligations: inspect the actual driver's contract. See
[cleanup semantics](https://docs.python.org/3.10/tutorial/errors.html#defining-clean-up-actions)
and [context manager helpers](https://docs.python.org/3.10/library/contextlib.html).

## Exceptions and cancellation

Catch errors at a boundary that can recover, translate them, or report failure.
A broad handler can be legitimate there; demonstrate the error it mishandles
before reporting a defect. Raising during an active handler retains implicit
`__context__`; `raise ... from exc` records an explicit `__cause__`. `from None`
suppresses the displayed context without erasing it. Logging an exception and
returning a success-shaped default can conceal a failure when callers rely on
that distinction. See the [raise statement](https://docs.python.org/3.10/reference/simple_stmts.html#the-raise-statement).

Cancellation can propagate through an awaited operation without an explicit
handler. The following worker records cleanup as cancellation leaves the task:

```python
import asyncio


async def worker(started: asyncio.Event, cleaned: list[str]) -> None:
    try:
        started.set()
        await asyncio.Event().wait()
    finally:
        cleaned.append("released")
```

Check whether cleanup preserves cancellation rather than swallowing it.
`asyncio.CancelledError` derives from `BaseException` on the versions considered
here (3.8 onward), so `except Exception` does not catch it. Ordinary cancellation
is cooperative, not forced termination of arbitrary blocking code. See
[task cancellation](https://docs.python.org/3.11/library/asyncio-task.html#task-cancellation).

## Mutable state and identity

Defaults and class attributes can share mutable objects across calls or instances.
Sharing is a defect only when the intended ownership requires isolation. For
per-call accumulation, preserve an explicitly supplied empty container:

```python
def append_value(value: int, values: list[int] | None = None) -> list[int]:
    if values is None:
        values = []
    values.append(value)
    return values
```

Check shallow copies, nested containers, and callbacks that capture a loop variable.
Use value equality when the contract compares values; object identity has a
different meaning. Do not infer portable identity behaviour from integer interning
or constant folding. See the [Python programming FAQ](https://docs.python.org/3.10/faq/programming.html#why-are-default-values-shared-between-objects).

## Iterators and data lifetime

An iterator is consumed as it advances. Check callers that traverse it twice,
inspect it for membership before processing, or return a lazy reader after closing
its resource. This function consumes its input exactly once:

```python
from collections.abc import Iterable


def total(values: Iterable[int]) -> int:
    return sum(values)
```

A generator around `fetch_all()` still allows that call to materialise every row;
streaming requires a source that actually fetches incrementally. Check the driver,
batch size, resource lifetime, and early termination. `itertools.groupby` groups
adjacent matching keys and its groups share an underlying iterator; do not assume
SQL-style grouping or independent retained groups. See
[iterators](https://docs.python.org/3.10/howto/functional.html#iterators) and
[groupby](https://docs.python.org/3.10/library/itertools.html#itertools.groupby).

## Filesystem and subprocess boundaries

Establish the allowed root, naming rules, and whether another process can change
the directory tree. Textual prefix checks can confuse sibling paths. This helper
checks an existing path in a stable tree, resolving symlinks before containment:

```python
from pathlib import Path


def existing_child(root: Path, name: str) -> Path:
    resolved_root = root.resolve(strict=True)
    candidate = (resolved_root / name).resolve(strict=True)
    candidate.relative_to(resolved_root)
    return candidate
```

It raises for a missing path or one outside the root. It does not prevent a
symlink replacement between validation and use. Where hostile concurrent changes
are possible, inspect the platform's descriptor-based operations and ownership
model. Check overwrite and partial-write behaviour against the target's recovery
requirements. Prefer managed temporary resources over predictable shared names.
See [path resolution](https://docs.python.org/3.10/library/pathlib.html#pathlib.Path.resolve)
and [temporary files](https://docs.python.org/3.10/library/tempfile.html).

For subprocesses, trace executable selection, argument boundaries, exit status,
timeouts, and output size. Argument lists with `shell=False` avoid shell parsing
in ordinary direct executable launches; they do not stop the target program
interpreting an attacker-controlled option. Use an option terminator only when
that program supports it. Windows batch files have different shell behaviour;
check the target platform. `shlex.quote` is not portable sanitisation. See
[subprocess security considerations](https://docs.python.org/3.10/library/subprocess.html#security-considerations).

## Concurrency and performance

Check task ownership, pending exceptions, cancellation, and bounds on in-flight
work. In Python 3.11+, `TaskGroup` waits for its tasks and cancels siblings when a
non-cancellation exception occurs; `asyncio.timeout` is also a 3.11+ API.
`gather` with its default settings propagates the first exception without
cancelling other submitted awaitables. Do not treat these APIs as interchangeable.
See [task groups](https://docs.python.org/3.11/library/asyncio-task.html#task-groups)
and [gather](https://docs.python.org/3.10/library/asyncio-task.html#asyncio.gather).

A semaphore can bound active work without bounding the number of tasks already
created. An `asyncio.Queue` consumer using `join` needs matching `task_done` calls
for every dequeued item, including a sentinel, when completion is counted that way.
See [queue completion](https://docs.python.org/3.10/library/asyncio-queue.html#asyncio.Queue.join).

Trace shared read-modify-write operations across threads or across `await` points;
do not assume the GIL or an async function makes a compound operation atomic.
Inspect lock ownership and ordering using the
[threading reference](https://docs.python.org/3.10/library/threading.html#lock-objects).
Moving a blocking call to a thread does not give it forced cancellation when its
awaiter is cancelled. Neither async, caching, parallelism, a set conversion, nor
string `join` is a universal improvement. Establish workload, memory cost,
ordering, hashability, and observable consequences first.

## Behavioural verification

Use the project's checks to exercise a concrete scenario: independent calls,
empty or exhausted iterators, cleanup after failure, cancellation propagation,
path escape, or a supported input boundary. Verify that a failing test fails for
the claimed reason. Avoid assertions that only mirror implementation details.
When patching a dependency, patch the name where the caller looks it up; see
[where to patch](https://docs.python.org/3.10/library/unittest.mock.html#where-to-patch).
Async fixture and test execution depend on the target's runner and plugin setup;
an async decorator alone does not establish that a test runs.

A coverage number or lack of new tests is not independently a finding. Report
an evidenced failure or explicit testing-requirement violation, with the contract's
location, trigger, impact, and priority. State interpreter versions actually
exercised and any version-specific APIs checked only against documentation.
