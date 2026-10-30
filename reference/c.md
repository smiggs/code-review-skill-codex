# C review guide

Use this guide under the [review contract](review-contract.md). Ground findings
in reachable inputs, ownership contracts, or platform requirements. Buffer
carrying, macro preferences, and style alone are not defects. A finding that
depends on undefined behaviour must name the trigger; do not rely on a
particular observed result from undefined code.

## Versions and review scope

Read the build configuration for the compiler, the `-std=` flag, warning and
sanitiser options, the target platform, and any compiler extensions used. The
executable audit baseline is GCC 13.3.0 on Linux/x86_64 for C11 and C17;
examples were compiled and exercised there. `_Atomic` and `<stdatomic.h>`
require C11; `gets` was deprecated in C99 TC3 and removed in C11. C23 is the
current standard, but the project's declared mode governs what is available.
See the [reference status](reference-status.md) for verification limits.

## Buffer sizes and copy safety

Buffers passed between functions need an explicit capacity parameter, and the
callee needs a stated contract for truncation, aliasing, and null pointers.
`strcpy`, `sprintf`, and `strcat` are safe when the caller has established the
bound; unbounded variants used on caller-controlled input are the defect
trigger. `gets` no longer exists in a C11 implementation, so its presence
signals a non-conforming mode or an emulation layer. `snprintf` truncates
silently and returns the length the output would have needed, so a caller that
must not truncate has to check the return value.

```c
// Copies without truncation; returns false if src does not fit.
bool copy_name(char *dst, size_t dst_size, const char *src) {
    size_t len = strlen(src);
    if (len + 1 > dst_size) {
        return false;
    }
    memcpy(dst, src, len + 1);
    return true;
}
```

The `len + 1` bound in this contract cannot overflow: a valid string of
length `len` occupies `len + 1` bytes, so `len` is at most `SIZE_MAX - 1`.
State the equivalent contract when adapting the pattern; a caller passing a
non-string buffer or an unverified `dst_size` is outside it.

`memcpy` between overlapping regions is undefined behaviour because the
C standard gives `memcpy` distinct-object semantics (C11 7.24.2.1, a
`restrict` contract since C99). `memmove` is defined for overlap. Reviewing
callers must show that regions cannot overlap; where overlap is legitimate,
such as shifting elements inside one array, `memmove` is the correct
primitive.

## Partial I/O and allocation failure

`fread` returns the number of whole objects read; a short count can mean
either end of file or an error, and the caller must use `feof` and `ferror`
to distinguish them. If a partial element is read, its contents are
indeterminate. An empty input, a truncated final record, and an I/O failure
are different outcomes that a caller may need to handle differently. Writing
loops that treat only "zero objects read" as failure silently accept
truncated data.

Allocation can fail. Check `malloc` and `realloc` results on every path,
including paths that also close files or release other resources. A size
computed from caller input needs an overflow check before the multiplication:
`count > SIZE_MAX / sizeof *p` rejects the wrap-around case, and `calloc`
encodes the check in the library call. Zero-size allocations and
`realloc(ptr, 0)` have implementation-defined results, so a project contract
for them is worth stating.

```c
// Reads the whole file into a caller-freed buffer.
// Returns 0 and sets *out/*len on success, -1 on error.
// An empty file yields *len == 0; short reads without error are
// reported as success so callers can handle truncation themselves.
int load_file(const char *path, unsigned char **out, size_t *len) {
    int rc = -1;
    FILE *f = NULL;
    unsigned char *buf = NULL;
    size_t used = 0;
    size_t cap = 4096;

    f = fopen(path, "rb");
    if (!f) {
        return -1;
    }
    buf = malloc(cap);
    if (!buf) {
        goto cleanup;
    }
    for (;;) {
        size_t got = fread(buf + used, 1, cap - used, f);
        used += got;
        if (used < cap) {
            if (ferror(f)) {
                goto cleanup;
            }
            break; /* end of file */
        }
        {
            unsigned char *grown;
            if (cap > SIZE_MAX / 2) {
                goto cleanup; /* next doubling would overflow size_t */
            }
            grown = realloc(buf, cap * 2);
            if (!grown) {
                goto cleanup;
            }
            buf = grown;
            cap *= 2;
        }
    }
    *out = buf;
    *len = used;
    rc = 0;
    buf = NULL;

cleanup:
    free(buf);
    fclose(f);
    return rc;
}
```

The cleanup path releases the buffer and file on every failure, and the
success path transfers ownership by clearing the local pointer. State the
equivalent ownership rule (who frees what on success and on failure) for
functions you review; conventions differ between projects, and a consistent
local convention is valid.

## Lifetime and undefined behaviour

Undefined behaviour in C includes use-after-free, reads of uninitialised
objects, signed arithmetic overflow, invalid shifts, out-of-bounds access,
and violating library `restrict` contracts (C11 4p2, 3.4.3). The standard
imposes no requirements on such a program, so a review finding should
describe the reachable trigger and its realistic consequences rather than a
guaranteed crash.

Pointer arithmetic may form a pointer exactly one past the last element of
an array, and comparing or subtracting such a pointer is defined. Evaluating
`*p` through it is undefined (C11 6.5.6p8), and arithmetic that goes beyond
one past the end is already undefined before any dereference. Loop idioms
such as `for (p = arr; p <= arr + n; ++p)` dereference the one-past pointer
on the final iteration.

```c
int sum_tail(const int *arr, size_t n) {
    int sum = 0;
    const int *end = arr + n;      /* one past the last element: defined */
    for (const int *p = arr; p != end; ++p) {
        sum += *p;
    }
    return sum;
}
```

Signed overflow is undefined (C11 6.5p5), so `a + b`, `a * b`, and negation
of `INT_MIN` need either value bounds that the caller enforces, unsigned
arithmetic, or checked helpers such as `__builtin_add_overflow` where the
project accepts compiler extensions. Shifts are undefined when the left
operand is negative or not below the width of the promoted type, and when
the right operand is negative or at least that width (C11 6.5.7). Reads of
uninitialised automatic objects are undefined; `malloc` memory must be
written before it is read.

## Error-handling conventions

Check return values of library calls that can fail, and distinguish the
outcomes the caller needs. `fread`, `fgets`, `read`, and `write` all have
partial-transfer semantics; swallowing a short count merges "no data" with
"I/O error". Error conventions (0 or negative, enums, `errno` setting) are
project decisions; the defect trigger is a caller that cannot tell outcomes
apart or a contract that differs between success and failure paths.
Document nullability: for each pointer parameter and result, state whether
NULL is permitted and what it means. Prefer returning a status code where a
NULL result would otherwise be ambiguous with a valid value.

## Concurrency

A data race (two conflicting accesses in different threads, at least one a
write, without synchronisation) is undefined behaviour in C11
(5.1.2.4). `volatile` provides no inter-thread ordering or atomicity; it is
not a substitute for synchronisation.

```c
#include <stdatomic.h>
#include <stdbool.h>

/* stop is shared with worker threads. */
static _Atomic bool stop = false;

bool should_stop(void) {
    return atomic_load(&stop);
}
```

`_Atomic` objects and the `stdatomic.h` operations make single accesses
atomic and give ordering, which the plain `volatile bool` version cannot.
Atomics make accesses race-free; they do not by themselves make a check-then-act
sequence such as test-and-clear a complete synchronisation, and mutexes are
still needed for multi-step invariants on shared state. Holding a lock across
blocking I/O is a liveness trigger worth reporting where the project's
callers can observe it; the project's own locking discipline governs.

## API design and const

`const`-qualified input parameters and explicit sizes make contracts
checkable: `int hash_bytes(const uint8_t *data, size_t len, uint8_t *out);`
states what may be read and written. Macros that evaluate arguments more than
once silently duplicate side effects, and multi-line macros need
`do { } while (0)` wrapping at call sites that use `if` without braces;
a `static inline` function avoids both. These are conditional conventions:
report them when the project's own rules or the observed call sites make the
consequence reachable, not as universal defects.

## Tooling and build checks

Warnings, sanitiser builds, and static analysis are review evidence, not
verdicts. A clean run does not prove the absence of undefined behaviour, and
a diagnostic on unreachable code is not a finding.

```bash
# Warnings and language mode (read-only checks)
gcc -std=c11 -Wall -Wextra -Wconversion -Wshadow -c src.c

# Sanitisers (debug builds)
gcc -std=c11 -fsanitize=address,undefined -fno-omit-frame-pointer -g -c src.c
gcc -std=c11 -fsanitize=thread -fno-omit-frame-pointer -g -c src.c

# Static analysis (read-only)
clang-tidy src.c -- -std=c11
cppcheck --enable=warning,portability src/
```

Formatting rewrites the working tree; propose it as a separate authorised
edit, not as a review check.

## References and checklist routing

Route inspection prompts for C through the
[common bugs checklist](common-bugs-checklist.md). The
[reference status](reference-status.md) records which claims above are
version-verified and the remaining limits. This guide does not establish
review accuracy: evaluation with fixed fixtures and agreed criteria is a
separate process.
