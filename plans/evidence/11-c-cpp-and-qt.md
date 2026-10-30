# Package 11: C, C++, and Qt audit evidence

Date: 30 October 2026. Technical audit candidate prepared at the user's
request under [the plan](../11-c-cpp-and-qt.md); human acceptance follows
the PR review and merge gates under the user's standing workflow (branch,
PR, `pr-coderabbit-loop` until clean, guarded merge commit). This work does
not reopen package 05, authorise publication, or establish review accuracy
for the changed guides. The [package 03
method](03-python-and-reference-quality.md) and the shared audit
requirements in [the plans README](../README.md) govern scope.

## Candidate and changes

Work began on `main` at `8c1a2ea` (the package 10 merge). The working
candidate is identified by the
[manifest](11-executable-checks/results/candidate-manifest.json) built the
same way as package 09's: SHA-256 of the sorted concatenation of each
file's UTF-8 path, NUL, SHA-256 hex digest of the file bytes, and NUL. It
covers the three guides, checklist, disposition, provenance, plan
documents, harness, fixtures, and result records; it excludes this
narrative, the manifest itself, and generated sources, caches, and
toolchains. The human checkpoint should name the manifest's combined
digest or an exact committed revision.

`reference/c.md`, `reference/cpp.md`, and `reference/qt.md` were rewritten
in British English using the Google documentation variant of the house
style. Their existing paths, core selective routing, skill identity, MIT
attribution, and the code-review contract links remain. A combined
C/C++/Qt routing section was added to the common-bug checklist (the
inherited checklist had no C, C++, or Qt sections to consolidate); no other
checklist section changed. Reference disposition and provenance now
describe this scoped candidate.

| Area | Correction and resulting contract |
| --- | --- |
| C buffer and copy safety | The inherited `strcpy` blanket ban became a stated-contract rule: bounded variants are safe when the caller establishes the bound, `snprintf` truncates silently and returns the needed length, and `gets` no longer exists in C11 (deprecated C99 TC3, removed C11). The retained `copy_name` contract states non-overlap, terminator, and capacity bounds, with the `len + 1` overflow bound shown to be unreachable for valid strings. |
| C partial I/O | The inherited cleanup example treated a zero read as failure and merged error with end of file. The replacement reads whole files with growth, distinguishes `ferror` from end of file, leaves a truncated final read to caller policy, and frees the buffer and file on every path. `fread`'s indeterminate partial element is quoted from its documented contract. |
| C undefined behaviour | The inherited "avoid pointer arithmetic past the object" heading was wrong: forming exactly one past the last element is defined, evaluating `*p` through it is undefined (C11 6.5.6p8), and going beyond it is already undefined. Signed overflow and shift triggers are stated conditionally on values (C11 6.5p5, 6.5.7); the data-race rule quotes 5.1.2.4 and `volatile` remains excluded from synchronisation. |
| C tooling | `clang-format -i` was removed from suggested review checks; formatting is a separate authorised edit. Warning and sanitiser commands are read-only. |
| C++ moved-owning types | The inherited `Socket` with `~Socket() { close(); }` and `Socket(Socket&&) noexcept = default;` was a defect: a defaulted move copies the raw handle, so source and destination both close it. The replacement defines transfer-and-reset moves (or deletion) with the close-once contract demonstrated by tests; the rule-of-zero `Buffer` remains the preferred shape, and the deprecated-but-generated implicit copies with a user-declared destructor are stated per [depr.impldec] and [class.copy.ctor]. |
| C++ negative-count reserve | The inherited "good" `reserve(static_cast<size_t>(n))` example converts a negative count into a huge request and throws `std::length_error` (guaranteed by [vector.capacity] for sizes above `max_size()`). The replacement validates the input contract first and the test asserts `std::invalid_argument` rather than the implicit length error. |
| C++ views and captures | `std::string_view` and `std::span` non-ownership, the dangling-return example, and reference-capture escapes are stated with the programmer responsibility quoted from the standard-library documentation. |
| C++ vocabulary types | `std::expected` is marked C++23 against the declared C++17/20 baselines; `std::stoi`'s `invalid_argument`/`out_of_range` mapping is exercised. |
| C++ performance advice | `reserve` and string-building stay conditional on measured workload impact; allocation patterns alone are not defects. |
| Qt parent ownership | The inherited example's confused manual-`setParent` framing became the documented ownership contract: the parent's destructor destroys children, stack or global children with a heap parent crash, unparented heap objects need a stated owner, `std::shared_ptr` plus parent ownership can double-destroy, and `QPointer` is a guard rather than an owner. |
| Qt thread affinity | The documented rules replace folklore: all QObjects live in the same thread as their parent, `setParent()` fails across threads, `moveToThread()` fails with a parent, a QObject lives in its creating thread, and creating QObjects before `QApplication` is unsupported. |
| Qt deferred deletion | `deleteLater()` now carries its documented edges: deletion when control returns to the loop that called it, no nested-loop trigger, thread-safety, deletion when a loopless thread finishes, and no deletion after the main loop stops. Direct `delete` from a slot that the object's own signal invoked remains the trigger for the deferred form. |
| Qt QThread subclassing | The blanket rejection was replaced with the documented conditions: subclassing `run()` is valid, slots on the subclass run in the creating thread ("new slots should not be implemented directly into a subclassed QThread"), `run()` without `exec()` has no event loop for queued delivery, deleting a running `QThread` crashes, and `QThread` methods are creating-thread-only unless documented. The worker-object pattern gained the full lifecycle (`quit`, `finished` → `deleteLater` for both objects). |
| Qt connections | Connection types now match the Qt 6.12 documentation, including the `BlockingQueuedConnection` same-thread deadlock warning, queued argument metatype registration, `UniqueConnection`, and `SingleShotConnection` (6.0+). The lambda context-object auto-disconnect contract is stated with the documented capture-lifetime warning; the string-based connect trigger is the runtime-only failure, not style. |
| Qt strings and containers | `u"..."_s` and `u"..."_L1` are marked Qt 6.4+ in the `Qt::Literals::StringLiterals` namespace; `const char*` comparisons convert UTF-8 at runtime with `QT_NO_CAST_FROM_ASCII` as the opt-out; Qt 6 `QList` is an alias of `QVector` while Qt 5 carried the `QVector` recommendation; implicit sharing, detach-on-mutate, and `at()` are conditional prompts. |
| Qt widgets | The inherited "NEVER" framing became the documented rule (GUI classes, notably `QWidget` and all subclasses, are not reentrant and can only be used from the main thread) with queued signals as the fix, and the blocking-event-loop advice kept as a user-visible-consequence trigger. |

## Sources and version boundaries

Primary sources were accessed on 29–30 October 2026. Qt's online
documentation serves the current Qt 6.12 pages; the retained Qt 5.15
differences are documented only. The C standard text was verified through
the WG14 C11 draft (N1570) and C23 working draft (N3047) where the fetch
pipeline could read them; clause citations for 6.5.6p8, 6.5.7, and 5.1.2.4
were corroborated through the standard-draft text where machine-readable
and recorded as clause-level citations otherwise.

| Claims checked | Primary sources |
| --- | --- |
| C library and language rules | [memcpy overlap](https://en.cppreference.com/w/c/string/byte/memcpy) (C11 7.24.2.1), [fread](https://en.cppreference.com/w/c/io/fread) (short reads, `feof`/`ferror`, indeterminate partial element), [gets removal](https://en.wikipedia.org/wiki/C11_(C_standard_revision)) and the [C11 feature list](https://en.cppreference.com/c/11) (`_Atomic`, removal of `gets`), N1570 4p2/3.4.3 (undefined behaviour), 6.5.6p8 (one-past-the-end), 6.5p5 (signed overflow), 6.5.7 (shifts), 5.1.2.4 (data races). |
| C++ library and language rules | [vector.capacity](https://eel.is/c++draft/vector.capacity) (`length_error` above `max_size()`), [depr.impldec](https://eel.is/c++draft/depr.impldec) (deprecated implicit copies with a user-declared destructor), [class.copy.ctor](https://eel.is/c++draft/class.copy.ctor) (conditions for implicit moves), [std::string_view ownership](https://en.cppreference.com/w/cpp/string/basic_string_view), [std::expected](https://en.cppreference.com/cpp/utility/expected) (C++23), [std::stoi](https://en.cppreference.com/w/cpp/string/basic_string/stol) (documented exceptions). |
| Qt object model and threads | [QObject](https://doc.qt.io/qt-6/qobject.html) (parent ownership, destructor destroys children, same-thread parent rule, `moveToThread` constraints, `deleteLater` contract and thread-safety, `~QObject` deferred-deletion note), [QThread](https://doc.qt.io/qt-6/qthread.html) (lifecycle, deleting a running thread, subclassing `run()`, worker-object pattern, `finished` → `deleteLater`), [Threads and QObjects](https://doc.qt.io/qt-6/threads-qobject.html) (GUI classes main-thread-only, single-thread object use, QApplication creation order), [Signals and Slots](https://doc.qt.io/qt-6/signalsandslots.html) (context-object lambda disconnection, destruction delivery caveat), [ConnectionType enum](https://doc.qt.io/qt-6/qt.html#ConnectionType-enum) (all five documented types), [QPointer](https://doc.qt.io/qt-6/qpointer.html), [QScopedPointer](https://doc.qt.io/qt-6/qscopedpointer.html), [QList](https://doc.qt.io/qt-6/qlist.html) (Qt 5 `QVector` recommendation, implicit sharing), [QString](https://doc.qt.io/qt-6/qstring.html) (`u"..."_s` since 6.4, `_L1`, UTF-8 conversion cost, `QT_NO_CAST_FROM_ASCII`). |

## Executable verification

The [harness](11-executable-checks/README.md) records portable commands,
exact extraction, captured results, fixture contracts, and dependency
identities. Baselines: Linux/x86_64; GCC 13.3.0 (conda-forge
`gcc_impl_linux-64` with binutils 2.46.1, glibc 2.39 sysroot, ICU 78.3,
OpenSSL 3.6.5 and their runtime libraries, all extracted without system
installation); Qt 6.12.0 (`qt6-main` from conda-forge) with the offscreen
widget platform; Python and PyYAML versions appear in the
[validation log](11-executable-checks/results/validation.txt). Sanitiser
runs execute under `setarch -R` because this kernel's address-space
randomisation prevents the sanitisers' shadow mappings; this is a runner
detail, not a project requirement.

Fence classification is checked loudly: the runner fails when a guide's
fence count or marked bodies change. The C++ units and tests compile as
one translation unit because they share types; the Socket's `close` call
is redirected to a recording stub and the worker fence's unqualified
`connect` resolves to the static `QObject::connect` by macro, both without
touching extracted bytes, and both documented in the harness README.

| Check | Observed result |
| --- | --- |
| C, four variants (address+undefined sanitiser, `-O2`, thread sanitiser on C11; address+undefined sanitiser on C17) | All 20 contract checks passed in each variant: copy bounds (exact fit, truncation, empty, zero capacity), whole-file reading (small, grown, empty, missing, directory read failure) with cleanup on every path, one-past-the-end iteration, atomic stop flag with two threaded readers. [Output](11-executable-checks/results/run-checks.txt). |
| C++, five variants (C++20 and C++17 sanitisers, C++20 thread sanitiser, C++17/C++20 `-O2`) | All 20 contract checks passed in each variant: `make_foo` success/failure, `fclose` wrapper open and failed-open, caller-owned views, value-captured lambda, rule-of-zero buffer copy, the corrected Socket move contract (no close on move, exactly one close, assignment releases the old handle, copies rejected), `stoi` mapping, eight-thread atomic counter, guarded eight-thread vector, negative-count rejection. |
| Qt 6.12.0 adapters | 18 checks passed across five adapters: parent destruction deletes the child (offscreen widgets platform); `qobject_cast` returns the object or null and `QPointer` clears on destruction; the context-object lambda disconnects when its context dies; the guarded setter skips duplicate emissions; the worker-object pattern runs, quits, and both worker and thread are deleted through `finished` → `deleteLater` within bounded waits. |
| Fixture sensitivity | Each defective variant fails its expectation and each clean control passes: C partial-I/O (defect exits 0 with four records including the mixed stale bytes; clean exits 3 with a truncation report), C++ double close (2 versus 1 recorded closes), Qt context lambda (2 versus 1 invocations, none dereferencing a destroyed object). |
| Evidence integrity | The regression re-runs extraction and the C/C++ checks in an isolated checkout with a prose edit: recorded files unchanged, fresh output byte-for-byte equal to the recorded run ([README](11-executable-checks/README.md)). |

The initial technical verification used no private code, model-review run,
external comment, commit, PR, repository setting change, skill
installation, or publication. Known setup errors during toolchain assembly
(wrong conda subdir URLs, a stale binutils selection, missing Qt runtime
libraries) were corrected before the recorded runs; none is counted as a
passing or failing assertion.

## Documentation checks and human decision

The [validation log](11-executable-checks/results/validation.txt) records
18 passing repository helper/validator tests, `git diff --check`, diff
statistics, the repository structural validator, the system skill-creator
quick validator, and house-style lint with zero errors and zero warnings on
each changed document. The inherited checklist's Testing section carries
two pre-existing lint findings outside this package's scope; they are
recorded rather than silently fixed. These checks establish mechanical
consistency within their scope; they do not establish useful review
behaviour.

Human decision: acceptance follows the PR review and merge gates under the
user's standing workflow (clean current-head CodeRabbit review, resolved
threads, dispositions for review-body findings, passing checks, guarded
merge commit). The Chinese installation and contribution documents need no
shared-behaviour change: this work changes reference guidance only. The
rewritten guides and evidence are English only, with no bilingual technical
validation. Any model review evaluation requires separately agreed prompts,
withheld answer keys, criteria, and raw reports; the prepared
[fixtures](11-executable-checks/fixtures/README.md) document the answer-key
boundary. No package 11 accuracy claim or release is authorised.
