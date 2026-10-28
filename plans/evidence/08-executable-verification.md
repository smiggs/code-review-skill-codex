# Package 08 executable verification

Date: 27 October 2026. Technical candidate with scoped executable checks and
prepared fixtures. On 28 October 2026 the user supplied
[conditional acceptance](08-pr-approval.md), effective after the current PR head
completes the CodeRabbit and merge gates. The outstanding-checkpoint wording
below describes the state before that conditional decision. The user requested
a handoff and continuation in the existing chat, with one agent. No sub-agents,
model reviewers, external review mutations, commits, or releases were used.

The [initial documentation checkpoint](08-typescript-react-and-vue.md) preserves
its original results and digest. This record supersedes its pending executable
work list. The [handoff](08-handoff.md) records the remaining steps. Package 08's
scope and human checkpoint remain governed by the [plan](../08-typescript-react-and-vue.md).

## Toolchain and method

The isolated [harness](08-executable-checks/README.md) supplies a pinned manifest,
lockfile, extracted-example compiler, Node test suite, fixture sensitivity checks,
and raw results. Framework dependencies remain development evidence outside the
installed skill. Registry access required approved network execution. Packages
were installed with lifecycle scripts disabled. No reviewed code was fetched or
executed from a private project.

| Component | Exercised version or scope |
| --- | --- |
| Host | Linux; Node.js 24.22.1; pnpm 11.25.0; Python 3.14.4; PyYAML 6.0.3. |
| TypeScript | 6.0.3; ES2022; NodeNext modules; DOM library; strict mode and unchecked-index protection. |
| React | React and React DOM 19.3.1; type packages 19.3.0; React Testing Library 16.3.3. |
| Vue | Vue and SFC compiler 3.5.44; Vue Test Utils 2.5.1; boundary comparison with SFC compiler and runtime-dom 3.4.38. |
| Simulated DOM | jsdom 30.1.3; no real browser, layout, hydration, or network transport. |
| TanStack Query | Published `@tanstack/react-query` 5.105.0 source inspected; cached-data refetch failure exercised. |
| Next.js | Version 15 documentation only, as recorded in the initial audit. No Next.js dependency, server-component build, or running application. |

Exact guide code bodies are extracted before compilation. The reader adds an
export adapter after its body; SFC 3.4 generated imports are redirected to its
runtime alias. Vue's SFC compiler and TypeScript transpilation do not establish
full `vue-tsc` type checking. The standalone reader and both request examples
receive strict TypeScript checking. No source example needed a behavioural repair
in this continuation.

## Results and limitations

The framework suite covers input validation, safe type controls, rejection
ownership, required-result aggregation, controlled request replacement, late
success and rejection, current failure, loading state, abort-aware/ignoring
loaders, explicit disposal, and fixed/reactive Vue inputs. Clean controls include
conditional child mounting, conditional React `use(context)`, stable component
identity, props getters, and explicit prop/update events. React DOM form ownership,
action payload order, and Query's cached-data error behaviour also have checks.

Three defective fixtures and their clean bases are prepared. The sensitivity
checks require the defective version to fail the relevant assertion and the
clean version to pass it. They do not use model reviewers or assign severity.
The fixture answer key must be withheld from future reviewers. An agreed model
review protocol, context isolation, and scoring remain separate work.

Initial execution exposed two test-assumption failures in a 23/25 run. A React
Strict Mode wrapper did not replay mount effects in this renderer; an explicitly
configured root did. The 3.4 compiler does not transform the 3.5 fragment's array
default, so missing props caused a render error. The boundary comparison now
supplies props, checks the watcher's snapshot in 3.4 versus reactive tracking in
3.5, and separately checks missing-prop defaults in 3.5. These are harness
corrections, not guide fixes. The 3.4 template still reads changing props even
though its destructured watcher input is a snapshot.

A first attempt ran before the test file existed. The default test subprocess
and nested sensitivity processes also exited without useful diagnostics in the
sandbox. The test runner now uses one-process isolation; nested sensitivity
checks ran through approved execution outside the sandbox. Neither infrastructure
failure counted as a passing or failing behavioural assertion. Original setup
logs and intermediate successful runs remain under `08-executable-checks/results/`.

An initial full Vue 3.4 package alias produced an unused server-renderer peer
mismatch with the root Vue 3.5 dependency. The alias now targets runtime-dom
3.4.38 directly; the final peer check has no issues. An offline re-resolution
attempt lacked cached registry metadata and was retried with approved access.

The root strict-effects test uses React DOM's `unstable_strictMode` root option;
it is scoped renderer evidence, not advice to depend on that option. React can
ignore post-unmount state updates, so its disposal assertions prove cancellation
and unchanged published results, not absence of internal setter calls. Vue's
returned ref also permits direct observation after disposal. No real browser,
Fetch transport, SSR/hydration, Next.js application, optimistic-mutation lifecycle,
or performance benchmark is claimed.

## Human checkpoint and next steps

Outstanding. Review the revised guides, versions, fixture preparation, and stated
limits against the candidate identity below. Record the exact accepted revision
or digest and any accepted limits. Do not mark package 08 complete before that
decision. Any model review evaluation requires separately agreed criteria; no
new review-accuracy claim, reopening of package 05, or release is authorised.

## Final checks

| Command | Result and evidence |
| --- | --- |
| `pnpm install --frozen-lockfile --ignore-scripts --store-dir /tmp/package-08-pnpm-store` in the harness directory | Exit 0; [locked install log](08-executable-checks/results/install-frozen.txt). |
| `pnpm test` in the harness directory | Strict standalone compilation and both SFC compiler modes succeeded; 29/29 framework/runtime checks passed, zero skipped. See the [final output](08-executable-checks/results/framework-final.txt). |
| `pnpm sensitivity` in the harness directory | All three defective heads rejected and all three clean bases accepted; [summary](08-executable-checks/results/sensitivity-final.txt). Per-case assertion logs are compressed losslessly under `results/red-*.txt.gz`; clean results are `results/green-*.txt`. |
| `pnpm peers check` in the harness directory | Exit 0; [no peer issues](08-executable-checks/results/peers-final.txt). |
| `python3 -B -m unittest discover -s tests -v` | 18/18 repository helper/validator tests passed; [output](08-executable-checks/results/repository-unittest.txt). |
| `python3 -B plans/evidence/03-python-examples.py` | 13/13 examples passed; output observed in this chat. |
| `python3 -B scripts/validate-skill.py` | Passed: structure and local Markdown link targets valid. |
| System skill-creator `scripts/quick_validate.py` against the repository | Passed: `Skill is valid!` |
| British house-style lint on the three guides, package plan, handoff, and package 08 evidence Markdown | Zero errors. The proper product names in the existing plan title produce one retained title-case warning. |
| `git diff --check` and `git diff --stat` | Whitespace passed; tracked diff inspected. New untracked evidence files are excluded from Git's unstaged stat; their paths and hashes are captured by the candidate manifest. |
| Checklist scope and route consistency | TypeScript/React/Vue sections route to their guides. Content outside those sections remains unchanged from the base revision; entry-point paths and upstream licence are preserved. |

The [guide source hashes](08-executable-checks/results/source-identities.json)
identify the files extracted by the final run. The
[Query source hashes](08-executable-checks/results/query-source-identities.json)
identify the inspected files in the published 5.105.0 package; its lockfile records
package integrity. These supplement the rolling documentation checked earlier.

## Candidate identity

The candidate was developed on
`94a51011fce025c3db73e6db28224dd1d2e52ac6` and prepared for PR review on
`main` at `29eb9c2341cd00fbc981ee394b22cc9a01180033`. The
[candidate manifest](08-executable-checks/results/candidate-manifest.json) lists
reviewable package files and SHA-256 values, including the harness, fixtures,
lockfile, source identities, and result artefacts. It excludes installed
dependencies, generated files, itself, and this record to avoid self-reference.
The manifest's combined digest uses sorted UTF-8 path, NUL, raw bytes, NUL for
each listed file. Recompute it after any included file changes. Human acceptance
must name that digest or an exact committed revision; no acceptance is recorded.
