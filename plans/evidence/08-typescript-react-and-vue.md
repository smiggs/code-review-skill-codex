# Package 08: documentation audit and continuation record

Date: 27 October 2026. This record preserves the initial documentation checkpoint.
Executable verification and fixture preparation were subsequently implemented in
the [execution record](08-executable-verification.md); human acceptance remains
outstanding. Pending items and command results below describe that initial
checkpoint unless explicitly stated otherwise.
The user authorised work on [package 08](../08-typescript-react-and-vue.md),
noting that the remaining hour window might require stopping before tests.
This record does not claim package completion or acceptance of validation limits.

## Revision and scope

Work began from `94a51011fce025c3db73e6db28224dd1d2e52ac6` with a clean working tree.
The candidate is an uncommitted diff. The content digest below identifies the
three guides, common-bug checklist, reference status, provenance, plan, and plan
index, excluding this self-referential evidence record. A later edit to those
files requires a fresh digest and proportionate checks.

The upstream baseline and MIT attribution in [provenance](../../reference/provenance.md)
remain unchanged. This is a local adaptation, not a check of upstream's latest
state. The skill name, entry point, selective routing, and singular `reference/`
paths remain intact. No helper or installation behaviour changed.

## Corrections and upstream divergence

| Area | Inherited problem | Candidate correction |
| --- | --- | --- |
| Runtime types | An existence check asserted that a field was a string; a string `.length` example falsely claimed failure. | Check the field's actual runtime type; retain string/array length as a clean control. Separate assertions, generic types, and compiler checks from validation. |
| Compiler and lint policy | Mandatory strictness, no `any`, generic reuse, and lint presets were treated as correctness requirements. | Inspect project configuration and unsafe consumers; keep indexed-access, aliasing, and generic-contract prompts without imposing tool or style choices. |
| Async ownership | Local catch/rethrow and `allSettled` were presented as universal fixes; `void` implied rejection handling. | Trace the awaiting owner, terminal handlers, required-result semantics, and the fact that aggregate rejection does not cancel work. |
| Requests | The TypeScript abort chain rethrew into a detached promise; Vue's concurrent `execute()` calls shared data, error, and loading without ownership. | Route TypeScript to framework examples. React and Vue fragments guard result and error publication after cleanup and consume failure. Vue has one watcher-owned run and no manual refetch claim. Execution remains pending. |
| React Hooks and identity | Blanket Hook rules omitted `use`; inline references, prop forwarding, and component size became findings. | Distinguish ordinary Hooks from `use`, conditional children from conditional Hooks, and type/key state reset from style. Require workload evidence for performance claims. |
| React 19 and integrations | Explicit form state, client API calls, and manual cache updates were marked bad; optimistic updates lacked action context; client wrappers supposedly converted all visual descendants. | Preserve valid alternatives, check action/form ownership and authoritative updates, and distinguish module boundaries from passed server-rendered children. Separate Next.js and Query APIs. |
| Suspense and Query | `useMemo` was suggested as a suspending promise cache; Query errors were described as always null; arbitrary production defaults were prescribed. | Describe resource ownership, initial-suspension cache limits, cached-data refetch errors, query keys, and documented cancellation limits. No pinned Query patch compatibility claim. |
| Vue version boundaries | Destructured array defaults were function-valued; `useTemplateRef` accepted a ref key; cleanup could appear valid after `await`; deferred Teleport implied arbitrary waiting. | Distinguish 3.5 compiler transforms, value defaults versus factories, string template-ref keys, synchronous cleanup registration, and same-tick Teleport target resolution. |
| Vue ownership and performance | Latest-target cleanup could miss an old listener; snapshots and nested props mutation were universally condemned; shallow refs and virtualisation were mandatory. | Trace actual listener registrations and reactive consumers, parent/child ownership, deactivation, and workload requirements. Remove unverified VueUse API recipes. |
| Checklist | TypeScript, React, and Vue examples duplicated conflicting recipes. | Consolidate only those sections into routed inspection prompts and clean controls. Python and later sections retain their prior content. |

Rewrites use the Google variant of British house style. They are English only;
Chinese guide translation and bilingual technical validation are not complete.
English and Chinese installation/contribution companions are unchanged because
shared installation and usage behaviour did not change. No language guide was
removed or renamed. Other language audits remain outside this package.

## Primary sources and version limits

All sources below were accessed on 27 October 2026. The guides link claims at
point of use. These are documentation checks, not executable compatibility results.

| Source family | Declared scope | Primary references |
| --- | --- | --- |
| TypeScript | Documentation includes TypeScript 6.0; example target is 6.0, ES2022, `strict`, and `noUncheckedIndexedAccess`. No compiler installed or exercised. | [Everyday types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html), [narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html), [indexed access option](https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html), [generics](https://www.typescriptlang.org/docs/handbook/2/generics.html), [object types](https://www.typescriptlang.org/docs/handbook/2/objects.html). |
| JavaScript and Fetch | Living standards, with no tested browser or Node.js matrix. | [ECMAScript promise algorithms](https://tc39.es/ecma262/multipage/control-abstraction-objects.html#sec-promise.all), [WHATWG Fetch](https://fetch.spec.whatwg.org/#fetch-method). |
| typescript-eslint | Rolling rule documentation only; no lint preset or package version mandated or executed. | [no-floating-promises](https://typescript-eslint.io/rules/no-floating-promises/). |
| React and React DOM | Retrieved documentation labelled 19.3. Retained examples use React 19 APIs; no installed React/DOM/type-package versions or execution. | [Hook rules](https://react.dev/reference/rules/rules-of-hooks), [`use`](https://react.dev/reference/react/use), [effects](https://react.dev/reference/react/useEffect), [state identity](https://react.dev/learn/preserving-and-resetting-state), [memoisation](https://react.dev/reference/react/useMemo), [Suspense](https://react.dev/reference/react/Suspense), [error boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary), [action state](https://react.dev/reference/react/useActionState), [form status](https://react.dev/reference/react-dom/hooks/useFormStatus), [optimistic state](https://react.dev/reference/react/useOptimistic), [client directive](https://react.dev/reference/rsc/use-client). |
| Next.js | Version 15 App Router pages labelled 15.5.28; not generic React routing behaviour. | [Server/client components](https://nextjs.org/docs/15/app/getting-started/server-and-client-components), [fetching and streaming](https://nextjs.org/docs/15/app/getting-started/fetching-data), [updating data](https://nextjs.org/docs/15/app/getting-started/updating-data). |
| TanStack Query | Requested v5 URLs redirect to rolling `latest` pages. Two attempted v5.90.5 tagged GitHub/raw documentation paths returned cache-miss errors. No pinned v5 patch audit established; these remain version-check prompts. | [Query keys](https://tanstack.com/query/v5/docs/framework/react/guides/query-keys), [defaults](https://tanstack.com/query/v5/docs/framework/react/guides/important-defaults), [Suspense API](https://tanstack.com/query/v5/docs/framework/react/reference/useSuspenseQuery), [Suspense errors](https://tanstack.com/query/v5/docs/framework/react/guides/suspense), [cancellation](https://tanstack.com/query/v5/docs/framework/react/guides/query-cancellation). |
| Vue | Vue 3 rolling docs with explicit 3.4/3.5 boundaries. Runtime and `@vue/compiler-sfc` patch versions have not been installed or exercised. | [Reactivity](https://vuejs.org/guide/essentials/reactivity-fundamentals.html), [script setup](https://vuejs.org/api/sfc-script-setup.html), [props](https://vuejs.org/guide/components/props.html), [watchers](https://vuejs.org/guide/essentials/watchers.html), [composables](https://vuejs.org/guide/reusability/composables.html), [helpers](https://vuejs.org/api/composition-api-helpers.html), [lists](https://vuejs.org/guide/essentials/list.html), [computed](https://vuejs.org/guide/essentials/computed.html), [Teleport](https://vuejs.org/guide/built-ins/teleport.html), [KeepAlive](https://vuejs.org/guide/built-ins/keep-alive.html), [performance](https://vuejs.org/guide/best-practices/performance.html). |

The older Next.js loading/streaming and server-action documentation paths were
unavailable through the browser tool. Retained links use the accessible version
15 getting-started pages instead. No claim relies on an inaccessible page.

## Checks and environment

The shell had no `node` or `tsc` on PATH. The bundled Node package directory also
lacked `typescript`, `react`, `react-dom`, `vue`, `@vue/compiler-sfc`, `jsdom`,
`@testing-library/react`, and `@vue/test-utils`. No packages were installed.
PyYAML 6.0.3 is available to the system Python. Structural validation does not
require a new environment in this session.

The first structural run reported the evidence link missing while this record
was being prepared. The system quick validator passed. Final check results and
candidate identity are recorded below after this record exists.

## Continuation and executable acceptance cases

Do these checks against the exact candidate before marking the guides verified.
Pin and record the toolchain in an isolated evidence workspace; avoid adding a
JavaScript runtime dependency to the installed skill. Use the installed TDD
workflow for executable harness behaviour, with failing reproductions before
repair where the inherited defect can be exercised.

| Target | Known defect or failure path | Clean control and required observation |
| --- | --- | --- |
| TypeScript value reader | Missing field, null, primitive, numeric `value`. | Accept a string field; compile the exact guide block under declared settings and record diagnostics. Exercise actual returned values, not prose matches. |
| TypeScript type boundaries | An asserted JSON shape reaches a string-only operation; absent indexed entry is used. | String/array `.length`, guarded lookups, and caller-owned rejection remain valid. Record compiler settings separately from runtime behaviour. |
| React request Hook | Resolve B before A, reject A after B, reject the current request, change `load`, and unmount before settlement. | Only the current run publishes data/error/loading after cleanup; test abort-aware and abort-ignoring loaders. Use a real React renderer and controlled promises. |
| React Hooks and identity | Conditional ordinary Hook ordering and nested component type reset. | Conditional child mounting and conditional React 19 `use` remain valid. Record the renderer and DOM environment separately from compilation. |
| Vue request composable | Change a ref/getter input, complete B before A, late reject A, reject current B, stop/unmount during work. | Fixed input runs once; reactive input reruns after scheduling. No obsolete success/error/loading write after cleanup; abort-aware and abort-ignoring loaders. Use Vue test tools and controlled promises. |
| Vue compiler boundary | Compile/run the exact SFC with matched Vue runtime/compiler versions around 3.4/3.5. | Reactive props destructuring changes only in the declared compiler mode; ordinary `props.count`, getters, array value defaults, and explicit model events remain valid. |
| Lifecycle and integrations | Changing listener target, Suspense refetch error, wrong form owner, or action without context. | Clean ownership alternatives remain valid; pin the particular React DOM, Next.js, and Query patch when exercising their APIs. |

These are a preparation matrix, not completed fixture files or an agreed model
review batch. Prepare distributable defect fixtures and clean controls next.
Agree evaluation acceptance criteria before model runs, keep answer keys out of
reviewer contexts, and record misses, false positives, and evidence quality
separately. No behavioural evaluation was run here; package 05 remains complete
under its accepted limits and is not reopened.

## Human checkpoint

Outstanding. The user has not approved the technical candidate, supported
versions, translation limits, or omitted executable checks. Record the exact
accepted commit or candidate digest and any explicitly accepted limits after
review. Package 08 remains incomplete. No release or publication is authorised.

## Documentation checkpoint results

System Python: 3.14.4; PyYAML: 6.0.3. Final documentation checks:

| Command or check | Result |
| --- | --- |
| `python3 -B scripts/validate-skill.py` | Passed after this evidence file was created: skill structure and local link targets valid. |
| `python3 -B /home/andrew/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/andrew/projects/code-review-skill-codex` | Passed: `Skill is valid!` |
| `python3 /home/andrew/.codex/skills/british-house-style/scripts/lint_house_style.py reference/typescript.md reference/react.md reference/vue.md plans/08-typescript-react-and-vue.md plans/evidence/08-typescript-react-and-vue.md` | Zero errors; one title-case warning for proper product names in the existing package title, retained deliberately. |
| `git diff --check` | Passed. |
| `git diff --stat` | Inspected: eight tracked files, 463 insertions and 3048 deletions. This new evidence file is untracked and therefore excluded from that stat. |
| Checklist boundary comparison | Passed: content before the TypeScript section and from the Python section onwards is byte-for-byte unchanged from the base revision. |
| Routing and semantic consistency | Inspected: entry-point links retain their paths, corresponding checklist sections route to the guides, and status/provenance/plan records disclose pending execution. |
| TypeScript compilation; React/Vue framework or browser tests | Not run; toolchain setup and executable verification remain outstanding. |
| Existing helper unit tests and Python example suite | Not run for this documentation-only change; helper behaviour was not modified. |
| Independent model review evaluation | Not run; no new evaluation batch or accepted review-accuracy claim. |

Candidate SHA-256:
`a82963e6086e8808f55f48fd235ada09e06f8bea6512d60c1c2edeb8c2f426eb`.
Reproduce by sorting the eight paths named in `git diff --name-only` at this
checkpoint, then hashing each UTF-8 path, a NUL byte, its raw file bytes, and
another NUL byte with SHA-256. The evidence record is excluded. This digest is
an identity aid, not a human approval or behavioural test result.
