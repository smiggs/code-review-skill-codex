# Package 03 verification and decision record

## Status and source revision

Prepared on 18 October 2026 on `codex/package-03-reference-quality`, branched from
`e246f01fa284bde7a59e41c02a3d818670599ffd`. Local `main` was fast-forwarded to
that origin merge before this branch was created. The user confirmed package 02
was merged and requested this package. Its decision record now reflects that
confirmation without inventing a separate review rationale.

The user approved package 03 on 18 October 2026 and requested commit and push.
Package 03 is complete within the recorded scope. The
[reference disposition](../../reference/reference-status.md) records checked scope,
unverified material, and technical deferrals. No helper, installation, or
publishing implementation is included.

## Changed material and upstream divergence

- Rewrote `reference/python.md` in British English, focusing on resource ownership,
  failure propagation, cancellation, mutable state, iterators, filesystem and
  subprocess boundaries, concurrency, versions, and behavioural verification.
- Replaced four topic/process guides with focused review prompts: architecture,
  performance, security, and review practices. Their paths and review roles remain.
  Removed mandatory patterns, numeric gates, automatic priority/merge labels,
  review budgets, split requests, and unqualified implementation recipes. The
  technical scope is the bounded guidance now retained, not the deleted cookbook.
- Consolidated only the Python subsection of `common-bugs-checklist.md` into a
  route to the checked guide. Added an evidence/contract notice to the inherited
  checklist. Other framework examples remain available and unverified. Corrected
  only the CSS guide's count-based blocking feedback and automatic priority
  headings; browser and preprocessor examples were not technically rewritten.
- Added `reference/reference-status.md`, linked from the entry point and relevant
  guides. No language guide was deleted or renamed. Nine non-Python language guides
  are byte-for-byte unchanged; CSS has only the scoped policy corrections above.
- Added a standard-library example-check script and separate synthetic consumer
  fixture. Updated repository instructions and both contribution documents with
  its actual command and environment limits.
- Updated both READMEs, the contract's introductory status, and package records.
  The contract's substantive terms, skill metadata, UI metadata, two assets,
  helper, MIT licence, and upstream attribution remain unchanged.

No multilingual technical audit is claimed. Rewritten guide prose and this
evidence are English only; the Chinese README and contribution notices are aligned.

## Corrections supported by inspection and reproduction

Before replacing the inherited Python guide, a standalone Python reproduction
observed the following:

```text
Await-only worker: CancelledError propagated without an explicit handler.
Translated exception: __context__ was ValueError; __cause__ was None;
                     __suppress_context__ was False.
Generator around fetch_all: all three rows materialised before its first yield.
Literal 257 identity in this CPython run: True.
Separately constructed int("257") identity: False.
```

The literal-identity probe also emitted the expected `SyntaxWarning` for `is`
with a literal. That probe demonstrates implementation dependence, not a portable
integer-cache rule. The guide now directs value contracts to equality.

The inherited claim that a loop awaiting work cannot cancel without an explicit
handler was false. The replacement explains propagation and cleanup separately.
The inherited claim that an exception raised without `from` loses its original
error was false: implicit context remains. The guide now distinguishes context,
explicit cause, and display suppression. Generator wrappers do not themselves
establish incremental database fetching.

Other scoped corrections remove the assumed memory benefit of `fetch_all`,
teardown-after-`yield` without failure handling, a queue sentinel omitted from
completion accounting, and blanket recommendations for annotations, a particular
checker, new syntax, concurrency, string joining, caching, and 80% coverage.
The replacement asks for actual project versions, requirements, and failure paths.

Architecture no longer turns line counts, method counts, coupling values, or a
preferred layering pattern into defects. Performance no longer treats every
nested loop, missing index, large list, or missing cache as blocking. Security
no longer supplies unqualified JWT, path-prefix, shell-quoting, or logging recipes
as universally safe implementations. Review practices no longer require question
phrasing, time budgets, praise, or large-PR splits.

## Executed guide checks

Command from the repository root:

```bash
python3 plans/evidence/03-python-examples.py
```

The script loads the five self-contained Python blocks from the prepared guide
and checks observable outcomes. It is an explicit evidence command, not an
installed test framework, configured CI gate, or test of prose wording. The
reviewed examples and synthetic fixture are trusted local test material; do not
generalise this into executing arbitrary reviewed code.

Environment: Python 3.10.12 on Linux. No Python 3.11–3.14 executable was found
on the shell path, so newer API/version claims were checked in documentation,
not executed. Symlink creation is required for the filesystem check. No packages
were installed and no network service, database, or live PR was used by these checks.

Result: 13 checks passed, with no skipped checks:

- UTF-8 first-line reading, and stream closure when reading raises `OSError`.
- Independent default accumulators and preservation of an explicitly supplied
  empty list.
- One-shot and empty iterators.
- Existing-child resolution, rejection of a sibling traversal, absolute outside
  path, and escaping symlink; missing input raises `FileNotFoundError`.
- Implicit exception context and `from None` display suppression.
- Materialisation before the first yield of a generator wrapping `fetch_all`.
- Cancellation propagation with cleanup, and cancellation of an await-only loop.
- Queue completion remaining pending until the dequeued sentinel is accounted for.
- Existing consumer events preserved by the base writer and lost by the changed
  writer, establishing the fixture's stated regression.

Checks involving intentionally failing behaviour pass by asserting the specific
failure or observed loss. They are not evidence that the changed consumer is
correct. No performance benchmark, interpreter matrix, or independent model
review evaluation was performed.

## Consumer fixture and review report

Prompt exercised manually:

```text
Use code-review-codex to review the change from writer-before.py to
writer-after.py in the supplied consumer. Read its applicable instructions.
```

The separate [consumer instructions](fixtures/03-consumer/AGENTS.md) state that
its event log is append-only: recording a single-line event must retain existing
events and add one newline-terminated event. The only source change is
`path.open("a", encoding="utf-8")` to `path.open("w", encoding="utf-8")` at line 2.
The checker uses temporary files containing `old\n` and calls each version with
`new`. The base produces `old\nnew\n`; the changed writer produces `new\n`.

Report produced:

> [P1] Preserve existing events when recording a new one
>
> `writer-after.py:2`: When the log already contains events, opening it with
> `"w"` truncates that history before writing the new event. This violates the
> consumer's append-only requirement in `AGENTS.md` and loses recorded events
> during normal use. Preserve the append behaviour.
>
> Verification: with initial content `old\n`, the base retained `old\nnew\n`
> after recording `new`; the changed version left only `new\n`. Scope: the
> supplied before/after functions and consumer instructions. No application-wide
> tests or external review actions were performed.

This manually prepared report is not independent forward-testing: the author
knew the intended defect. The executable check establishes actual file-content
loss. The requirement comes from this consumer's `AGENTS.md`; the reusable skill
does not forbid write mode or prescribe an event-log workflow. The base writer
is a clean control for this invariant, not a certification of the whole consumer.

## Primary documentation checked

Sources were opened on 18 October 2026. Versioned links intentionally establish
the APIs relevant to the examples and version boundaries, rather than assuming
the latest `/3/` documentation matches every target. These are API references,
not a recommendation to deploy an old interpreter.

| Claim checked | Primary source |
| --- | --- |
| Generic containers, union forms, Required/NotRequired, and 3.12 type syntax | [Python 3.12 typing](https://docs.python.org/3.12/library/typing.html) |
| Cleanup and failure handling | [Python 3.10 cleanup](https://docs.python.org/3.10/tutorial/errors.html#defining-clean-up-actions), [contextlib](https://docs.python.org/3.10/library/contextlib.html) |
| Implicit context, explicit cause, and suppression | [Python 3.10 raise statement](https://docs.python.org/3.10/reference/simple_stmts.html#the-raise-statement) |
| Defaults, closures, and identity misconceptions | [Python programming FAQ](https://docs.python.org/3.10/faq/programming.html) |
| Iterator consumption and grouping lifetime | [Python iterator HOWTO](https://docs.python.org/3.10/howto/functional.html#iterators), [groupby](https://docs.python.org/3.10/library/itertools.html#itertools.groupby) |
| Cancellation and 3.11 TaskGroup/timeout boundaries | [Python 3.11 tasks](https://docs.python.org/3.11/library/asyncio-task.html), [CancelledError](https://docs.python.org/3.10/library/asyncio-exceptions.html#asyncio.CancelledError) |
| gather, task ownership, and thread offloading | [Python 3.10 tasks](https://docs.python.org/3.10/library/asyncio-task.html) |
| Queue completion | [Python queues](https://docs.python.org/3.10/library/asyncio-queue.html#asyncio.Queue.join) |
| Path resolution, temporary resources, and subprocess limits | [pathlib](https://docs.python.org/3.10/library/pathlib.html#pathlib.Path.resolve), [tempfile](https://docs.python.org/3.10/library/tempfile.html), [subprocess](https://docs.python.org/3.10/library/subprocess.html#security-considerations) |
| Locking and patch lookup | [threading](https://docs.python.org/3.10/library/threading.html#lock-objects), [where to patch](https://docs.python.org/3.10/library/unittest.mock.html#where-to-patch) |
| Scoped authorisation and argument injection | [OWASP authorisation](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [OWASP command injection](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html) |
| Core Web Vitals interpretation | [web.dev Web Vitals](https://web.dev/articles/vitals) |
| Shared/personalised caching and representation validators | [MDN HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) |
| Estimated plans versus statement execution | [PostgreSQL 18 EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html) |

The architecture guide's design prompts are conditional on target-project
requirements; they do not assert a universal pattern or numeric threshold.
Ten other language guides and the non-Python common-bug examples have not been
validated against their frameworks' official documentation in this package.

## Structural and preservation checks

Checks on the prepared working files:

- `git diff --check`: passed; `git diff --stat` inspected. Equivalent whitespace
  checks for the added evidence, example script, status guide, and consumer files
  reported no errors.
- `python3 /home/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/andrew/projects/code-review-skill-codex`:
  passed with `Skill is valid!`. This is an installed system validator, not a
  repository dependency or a review-behaviour test.
- A one-off Markdown scan found 117 internal file-link occurrences and 71 anchors,
  all resolving. Fenced examples and inline code were excluded from link parsing.
  No internal inbound link depended on a removed topic-guide heading. Every
  reference is accounted for in the disposition and routing; paths are preserved.
- Inspection of all retained references found no remaining prescribed review-time
  budgets or automatic large-PR split requests. Runtime cache durations and
  ordinary code/data splitting are distinct from review-process gates.
- Byte comparison against the source revision confirmed 16 protected files are
  unchanged: nine non-Python language guides, licence, helper, UI metadata, two
  templates, and both package 01 evidence records. The common checklist's
  non-Python examples and CSS technical blocks were retained.
- Contract comparison from `## Scope and modes` onward confirmed unchanged
  substantive terms. Parsed discovery metadata is unchanged; only the guide-status
  notice in the entry point changed.
- English and Chinese usage prompts and Bash examples match. Manual inspection
  confirmed aligned current-package status, example-check commands, and translation
  limitations. Installation commands and contribution expectations stay aligned.

SHA-256 fingerprints presented for approval of runtime/reference and example material:

```text
a5bfae81f0eef4976bf2f4cee7e55489078c89fd9ffa79db23fa1fa268e6faaa  SKILL.md
3580172d218a46be37ed8d942b08867dbd5fdd6d3a877f767f386ef85333032b  plans/evidence/03-python-examples.py
620cabb28b238193003c5d90b38d61ac0fba711703cd5baccd8fc6b8b3f18ffe  plans/evidence/fixtures/03-consumer/AGENTS.md
ec2cd4d7e64f80312342d327442f00abc48f72e0b9f6f7c12e7e68b5959dc1a8  plans/evidence/fixtures/03-consumer/writer-after.py
7cfde87e4a1aa8e1ad5329accc29f2a5e9250dbc427a1eb48a2b645f9b686946  plans/evidence/fixtures/03-consumer/writer-before.py
3a6241827d9cf9081174d63ce1ff076dd3000b14c74e5934585a4e1dd3e391c9  reference/architecture-review-guide.md
235756a4e123f6ed0e2e80c9869c831e16c6e173123c1edc90441455db54cbfe  reference/code-review-best-practices.md
f60e5aecc5f410d508003b5d8bda1d083b98e854f5eb52829673f7d349f534dd  reference/common-bugs-checklist.md
e290d683cecce86e299ab10ef0fd288f3cd06caa1415a05fd24d79df5b8f59fe  reference/css-less-sass.md
dc302a355e52615c9120cc125b8499d48ccd13332cf5ecec03111d3829182830  reference/performance-review-guide.md
d3ab70a094d57a005b856b8baca60bc3faa2b1eeee900fd8087bde613af52a03  reference/python.md
55b4bbe7016341ac8c4d77d10433eaa68a5754129092755458db14dbfbc0d90b  reference/reference-status.md
962a67c2f86470dd0c2363ff71701129dd2575542870593ca170fcdda366c7c3  reference/review-contract.md
c780b0a3077a3934227fac9631343afe8f8c231db953b63d28348e9651df8c81  reference/security-review-guide.md
```

Recalculate with `sha256sum` against the listed paths when recording the decision.
After updating only its approval notice, `reference/reference-status.md` has SHA-256
`fd01d6a0a6b9271581006452ddd44852f03a8f439ba81411d5536b7582dd9c5f`.
Restoring its prior notice reproduces the approved fingerprint above. All other
listed material is unchanged; approval-status edits passed whitespace, link,
and structural checks.
Changes to this material require proportionate checks. Structural validity does
not establish review accuracy or multilingual technical correctness. Independent
behavioural evaluation remains package 05 work.

## Human checkpoint

- Checkpoint: package 03 reference quality.
- Evidence: rewritten Python guide, reference disposition, executable checks,
  primary sources, and consumer reproduction above.
- AI recommendation: accept the scoped Python and topic/process changes, with
  explicit technical deferrals for the ten non-Python guides and common-bug
  framework examples. The CSS policy correction does not establish technical
  correctness of its browser or preprocessor examples.
- Human judgement requested: Python scope, the shortened topic guides, retained
  guide disposition, and deferred translations and runtime checks.
- Human decision: approved on 18 October 2026. The user stated "ok approved,
  commit and push so I can review the differential" in this chat. No separate
  rationale or reviewer identity was supplied. No substantive changes were requested.
- Post-decision edits update approval and completion notices only. Technical
  deferrals and validation limits remain unchanged.
- Remaining work: helper validation,
  independent review-behaviour evaluation, installation, and distribution stay
  with their later packages.

The [package plan](../03-python-and-reference-quality.md) and
[human checkpoint policy](../human-ai-checkpoints.md) are satisfied for this
scoped package. Approval does not imply multilingual technical verification,
helper correctness, or completion of the independent behavioural evaluation.
