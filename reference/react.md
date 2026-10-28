# React review guide

Apply the [review contract](review-contract.md) with the target's React,
React DOM, compiler, framework, and data-library versions. This audit consults
React documentation labelled 19.3, Next.js 15 App Router documentation (labelled 15.5.28), and
TanStack Query v5 documentation URLs. Executable checks use React/React DOM
19.3.1 and Query 5.105.0 in jsdom 30.1.3. Next.js was checked against documentation
only; there is no server-component or browser compatibility matrix.
See [reference status](reference-status.md) for validation limits and the
[TypeScript guide](typescript.md) for input and promise boundaries.

## Hooks, state, and component identity

Ordinary Hooks must run in a consistent order at the top level of a component
or custom Hook, before conditional returns. A parent may conditionally render a
child that calls Hooks unconditionally. React 19's `use` API permits conditions
and loops, but must run during a component or Hook render and cannot be wrapped
in `try/catch`. Do not apply the ordinary ordering rule to it. See
[Hook rules](https://react.dev/reference/rules/rules-of-hooks) and
[`use`](https://react.dev/reference/react/use).

Trace state ownership, stable keys, and component type at each tree position.
A component function defined during its parent's render creates a different
type on later renders and can reset child state. Changing a key can intentionally
reset a form. Index keys need a concrete reorder, insertion, or deletion that
misassociates state before they become a finding. See
[state preservation](https://react.dev/learn/preserving-and-resetting-state).
Props, context, reducers, local state, and component composition can all be valid;
component length and prop forwarding alone do not establish a defect.

## Effects and request ownership

Check each Effect's external synchronisation, reactive dependencies, and cleanup.
React cleans up before rerunning with changed dependencies and on unmount;
development Strict Mode also probes setup and cleanup. Missing dependencies
matter when a changed value leaves synchronisation stale. Deriving a filtered
list during render is often simpler, but an extra Effect needs demonstrated
impact to become a finding. See [`useEffect`](https://react.dev/reference/react/useEffect).

Illustrative TypeScript Hook for React 19. The caller supplies a stable `load`
function that validates its response and accepts a signal. `id` or `load` changes
replace the request. The example clears old data while loading; applications
may deliberately retain previous data with a separate freshness indicator.
The exact fragment passed strict TypeScript 6.0.3 compilation and controlled
request tests in React Testing Library 16.3.3 with jsdom 30.1.3.

```tsx
import { useEffect, useState } from 'react';

type User = { name: string };
type LoadUser = (id: string, signal: AbortSignal) => Promise<User>;
type View = { data: User | null; error: unknown; loading: boolean };

export function useUser(id: string, load: LoadUser): View {
  const [view, setView] = useState<View>({
    data: null, error: null, loading: true,
  });
  useEffect(() => {
    let active = true;
    const controller = new AbortController();
    setView({ data: null, error: null, loading: true });
    async function run() {
      try {
        const data = await load(id, controller.signal);
        if (active) setView({ data, error: null, loading: false });
      } catch (error) {
        if (active) setView({ data: null, error, loading: false });
      }
    }
    void run();
    return () => {
      active = false;
      controller.abort();
    };
  }, [id, load]);
  return view;
}
```

The guard protects both result and error publication after cleanup, including
loaders that finish despite cancellation. The async function consumes rejection;
`void` alone would not. Scoped checks exercised out-of-order completion,
rejection, dependency replacement, and unmount. Effects
run after commit, so this fragment does not promise that prior data is never
visible during the render before replacement setup.

## Memoisation and rendering cost

Use measured render cost, interaction latency, or a demonstrated workload.
`useMemo` and `useCallback` can help expensive calculations, memoised children,
or dependencies of other Hooks. They are not restricted to `React.memo` users.
Inline objects and callbacks are valid unless identity causes an actual problem.
Do not rely on memo caches to preserve correctness: React may discard them.
Check whether React Compiler is enabled before prescribing manual memoisation.
See [`useMemo`](https://react.dev/reference/react/useMemo).
Virtual lists need workload and accessibility evidence; no fixed list length
or component size is a correctness threshold.

## Suspense and error recovery

Suspense handles supported suspending resources, not an arbitrary fetch started
inside an Effect. A promise read during client rendering needs the resource
identity and cache lifetime required by the installed integration. `useMemo`
is not a general cache for an initial render that suspends. Loading boundaries
control reveal behaviour; one boundary or several can both satisfy the design.
See [Suspense](https://react.dev/reference/react/Suspense).

Check error recovery at the boundary that owns it. An Error Boundary does not
catch ordinary event-handler or detached async failures. A rejected resource
read by `use` can reach an Error Boundary. A missing local boundary alone is
not evidence that the application has no recovery. See
[Error Boundary limits](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary).

## React 19 actions and forms

`useActionState` passes previous state before the action payload. Check initial
and returned state shapes, validation failures, and action ownership. Passing
its dispatcher to a form action establishes the action context; manual dispatch
needs the documented transition context. See
[`useActionState`](https://react.dev/reference/react/useActionState).
`useFormStatus` comes from `react-dom` and reads a parent form; calling it in the
component that creates that same form does not observe the form's pending state.
See [`useFormStatus`](https://react.dev/reference/react-dom/hooks/useFormStatus).

Optimistic updates must run in an Action or Transition. Check success updates
to the authoritative value, failure presentation, and overlapping submissions.
`useOptimistic` does not persist a server result or implement application error
reporting. Explicit pending/error state and waiting for success are valid
alternatives. See [`useOptimistic`](https://react.dev/reference/react/useOptimistic).

## Server and client boundaries

In a React Server Components integration, `'use client'` marks a module dependency
boundary. Server-rendered children passed through a client wrapper remain a valid
pattern; the visual descendant tree does not all become client code. Check
browser-only APIs, state, boundary serialisation, and secret-bearing imports
against the integration. See [`'use client'`](https://react.dev/reference/rsc/use-client).

Next.js 15 App Router route defaults and conventions belong to Next.js, not every
React application. Check the exact route and boundary before making streaming
claims: an awaited operation does not itself establish a visible fallback. See
[Next.js data fetching and streaming](https://nextjs.org/docs/15/app/getting-started/fetching-data).
Client API requests and Server Actions are both valid designs. See
[Next.js server/client components](https://nextjs.org/docs/15/app/getting-started/server-and-client-components).
`revalidatePath` is a Next.js API, and server mutations still need input validation
and authorisation. See [Next.js server actions](https://nextjs.org/docs/15/app/getting-started/updating-data).

## TanStack Query v5 inspection scope

Confirm the installed patch before applying these prompts. This audit inspected
the published 5.105.0 source and exercised a cached-data Suspense refetch error
in that version. Its v5 documentation links redirect to rolling pages; other
Query patches and cancellation integrations remain untested. React itself does
not define these APIs.

- Include data-changing inputs in query keys. Object keys are hashed by value;
  a fresh filter object alone does not prove a cache miss. See
  [query keys](https://tanstack.com/query/v5/docs/framework/react/guides/query-keys).
- Default staleness, retry, refetch, and garbage-collection policies need the
  application's freshness and load requirements. A default `QueryClient` is
  valid; `gcTime` and `staleTime` govern different things. See
  [defaults](https://tanstack.com/query/v5/docs/framework/react/guides/important-defaults).
- `useSuspenseQuery` omits `enabled`, `placeholderData`, and configurable
  `throwOnError`. Conditional child rendering can gate it without conditional
  Hook calls. See the [API](https://tanstack.com/query/v5/docs/framework/react/reference/useSuspenseQuery).
- Cached data can remain visible with a refetch error; `error` is not always
  null, and not every error is automatically thrown. See
  [Suspense error handling](https://tanstack.com/query/v5/docs/framework/react/guides/suspense).
- Check signal consumption for ordinary queries. Suspense query cancellation
  has documented limits; do not promise that passing a signal repairs it. See
  [cancellation](https://tanstack.com/query/v5/docs/framework/react/guides/query-cancellation).

Manual cache updates and mutation-variable optimistic UI have different consumers
and ownership. Neither is intrinsically wrong. Check concurrent mutations,
rollback, and invalidation against the installed API and application behaviour.
