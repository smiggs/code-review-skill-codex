# Package 11 review fixtures

Synthetic, distributable code fixtures prepared for a separately agreed
behavioural evaluation of the C, C++, and Qt guidance. Each directory holds
one known-defect variant and one clean control whose difference is the
review finding under test. Sensitivity of the paired assertions is
demonstrated in [the harness](../README.md); model detection, false
positives, and severity calibration are not measured here.

| Directory | Area | Defect variant | Clean control |
| --- | --- | --- | --- |
| `c-partial-io` | `fread` partial-transfer handling | treats the requested count as read, silently emitting a truncated final record mixed with stale buffer bytes and ignoring the error/end-of-file distinction | uses the returned count, reports I/O failure separately, and makes truncation an explicit, caller-visible outcome |
| `cpp-move-close` | defaulted moves against a closing destructor | `Conn(Conn&&) noexcept = default;` copies the owning handle, so the same handle is closed twice | the move transfers the handle and resets the source, so each handle closes exactly once |
| `qt-context-lambda` | lambda connections without a context object | the connection outlives the logical owner and the lambda still runs after the owner is destroyed | a context object disconnects the lambda with the owner |

The defect variants are designed so that their wrong outputs are produced
through defined behaviour only (the C fixture's stale bytes come from the
program's own buffer prefill; the C++ fixture counts closes through a
program-side registry; the Qt fixture observes invocation, never
dereferences a destroyed object). They do not rely on undefined-behaviour
symptoms.

Answer-key hygiene: the `defect`/`clean` file names, this table, the
harness, the audit narrative, and the recorded outputs are the answer key.
A future review exercise must present the fixture sources under neutral
names, without this README, the harness, or recorded logs.
