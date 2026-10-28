# Package 08 executable checks

This isolated development harness compiles the code extracted from the three
review guides and exercises its observable behaviour. It is excluded from the
installed skill. It does not run model reviewers or establish review accuracy.

## Reproduce

Use Node.js 24.22.1 and pnpm 11.25.0 for the recorded environment. Other versions
are untested. From this directory, install the lockfile and run the checks:

```bash
pnpm install --frozen-lockfile --ignore-scripts
pnpm test
pnpm sensitivity
pnpm peers check
```

Installation needs registry access or a complete local package store. Dependency
lifecycle scripts are disabled. The lockfile records exact transitive versions
and integrity values. No globally installed framework or TypeScript is required.
If Node.js is bundled rather than on PATH, prepend its `bin` directory before
running the commands. A sandbox can require an approved execution path for
nested Node test processes; an empty subprocess failure is not a test result.

## Coverage and adaptations

`prepare.mjs` extracts fenced code from `reference/typescript.md`,
`reference/react.md`, and `reference/vue.md`. It compiles their bodies with
TypeScript 6.0.3, ES2022, DOM libraries, `strict`, and
`noUncheckedIndexedAccess`. The reader receives an export adapter after its
unchanged body so tests can call it. The React and Vue composables already
export their entry points. Generated sources, emitted JavaScript, compiler
configuration, and source hashes are local files under `.generated/`.

The Vue SFC is parsed and compiled with matched compiler/runtime versions:
3.5.44 and 3.4.38. The 3.4 runtime alias uses `@vue/runtime-dom`, avoiding an
unused server-renderer peer mismatch. Generated 3.4 imports are redirected to
that alias; the source SFC is unchanged. SFC TypeScript is transpiled, not checked
with `vue-tsc`; this is distinct from strict checking of the standalone examples.
The 3.4 check supplies the optional props and demonstrates the watcher snapshot;
the exact 3.5 example also exercises its defaults without supplied props.

`checks.test.mjs` uses the Node test runner in one process, jsdom 30.1.3,
React Testing Library 16.3.3, and Vue Test Utils 2.5.1. Controlled promises cover
late success, late rejection, current failure, loading ownership, abort-aware
and abort-ignoring loaders, input replacement, stopping, and unmounting. Additional
checks cover valid Hook patterns, state identity, form ownership, action payloads,
and a cached-data Suspense refetch error in TanStack Query 5.105.0.
The strict-effects test explicitly configures the React DOM root's
`unstable_strictMode` option; a wrapper alone did not replay initial effects in
the exercised renderer. That test setup is not a public API recommendation.

No real browser, network Fetch, hydration, server-component bundler, Next.js
application, optimistic mutation lifecycle, virtual-list benchmark, or compiler
matrix beyond the stated versions was exercised. React ignores state updates
after unmount: its disposal assertion observes cancellation and the retained
published result, rather than proving no setter invocation internally. Vue's
exposed ref permits observing whether a late callback changes it after disposal.

## Defect fixtures and controls

The fixtures are synthetic adaptations of this repository's MIT-licensed guides.
The root licence and upstream attribution continue to apply. Each case supplies
project requirements, a clean `base` version, and a defective `head` version.
The [answer key](fixtures/answer-key.json) is for maintainers only. A future
reviewer must receive only its assigned source, comparison, and project context,
with the key, harness assertions, and prior reports withheld.

`sensitivity.mjs` runs selected behavioural assertions against each defective
head and requires an assertion failure, then runs the same assertions against
the clean base and requires success. These are technical sensitivity checks,
not model review scores. Routine red and green output is written under ignored
`.generated/results/`; it does not overwrite the recorded `results/` evidence or
its candidate manifest. `evidence-integrity.test.mjs` reproduces routine execution
in an isolated workspace and verifies that recorded bytes remain unchanged.
Preparing fresh recorded evidence requires an explicit copy and manifest update.
Expected-failure TAP output is stored as `.txt.gz` to
preserve its whitespace without introducing patch whitespace errors; use
`gzip -dc .generated/results/red-react.txt.gz` to read a failure. The acceptance criteria and execution of a separate
model review batch still need agreement. See the
[execution record](../08-executable-verification.md) for results and limits.
