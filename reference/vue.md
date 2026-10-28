# Vue review guide

Use the [review contract](review-contract.md) with the project's Vue runtime,
`@vue/compiler-sfc`, TypeScript, and build-tool versions. This audit consults
Vue 3 documentation with explicit 3.4 and 3.5 feature boundaries; it does not
establish a general compatibility matrix. Scoped checks use runtime/compiler
3.5.44 and the 3.4.38 runtime/compiler boundary; the
[reference status](reference-status.md) records their limits.
Use the [TypeScript guide](typescript.md) for runtime validation and promises.

## Reactive values and props

Follow the value consumed by a template, watcher, or composable. Destructuring
a primitive property from an ordinary `reactive` object copies its value;
it does not keep a live connection. A destructured nested object may still be
a reactive proxy. `ref`, `reactive`, `toRef`, and `toRefs` are valid designs;
report lost updates only when the consumer requires them. See
[reactivity fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html).

Vue 3.5's compiler transforms access to variables destructured directly from
`defineProps` in the same `<script setup>` block. This does not make a plain
value passed to another function reactive. Pass a getter or ref to a consumer
that supports it, and evaluate the getter inside a tracked effect. For example,
`useUser(() => props.userId)` can track changes; `useUser(props.userId)` may
intentionally take only an initial snapshot. Check that composable's contract.
See [composables](https://vuejs.org/guide/reusability/composables.html).

The following is an illustrative Vue 3.5 single-file component fragment.
Before 3.5, props destructuring is not reactive by default. Destructured array
defaults are values; `withDefaults` instead uses factories for mutable defaults.
A function-valued prop is a different contract:

```vue
<script setup lang="ts">
import { watch } from 'vue';
const { count = 0, items = [] } = defineProps<{
  count?: number;
  items?: string[];
}>();
watch(() => count, value => console.log(value));
</script>
<template><p>{{ count }} / {{ items.length }}</p></template>
```

The exact fragment passed SFC compilation and reactive-prop execution checks
with the declared versions; it has not received full `vue-tsc` checking. It does not
justify requiring a migration from `props.count` or `withDefaults`. See
[`<script setup>`](https://vuejs.org/api/sfc-script-setup.html).

Props bindings are readonly, but nested object/array mutation can affect shared
parent state. Check the intended owner: tightly coupled components may share
mutation deliberately. Type-based and runtime prop/emits declarations are valid;
neither replaces application validation of untrusted data. See
[props](https://vuejs.org/guide/components/props.html).

## Watchers and request ownership

`watch` tracks explicit sources; `watchEffect` tracks synchronous reactive reads,
including those before its first `await`. Passing a primitive property value to
`watch` is different from passing a getter. Check initial execution, scheduling,
and the consumer's DOM requirements before prescribing `immediate`, `deep`, or
`flush: 'post'`. A watcher created synchronously in component setup stops on
unmount; asynchronously created watchers need an explicit owner. See
[watchers](https://vuejs.org/guide/essentials/watchers.html).

`onWatcherCleanup` requires Vue 3.5 and registration during synchronous execution,
before any `await`. Callback `onCleanup` remains a valid alternative. Register
cleanup before starting work so invalidation can dispose it immediately.

Illustrative composable for Vue 3.5 and TypeScript with DOM types. It accepts a
ref, getter, or fixed ID. The caller supplies `load`, which validates its response.
Call it synchronously in component setup so Vue owns the watcher. This fragment
passed strict TypeScript 6.0.3 compilation and controlled request tests with
Vue Test Utils 2.5.1 in jsdom 30.1.3; it exposes no manual refetch operation.

```typescript
import { shallowRef, toValue, watch } from 'vue';
import type { MaybeRefOrGetter } from 'vue';

type User = { name: string };
type LoadUser = (id: string, signal: AbortSignal) => Promise<User>;
type View = { data: User | null; error: unknown; loading: boolean };

export function useUser(id: MaybeRefOrGetter<string>, load: LoadUser) {
  const view = shallowRef<View>({
    data: null, error: null, loading: true,
  });
  const stop = watch(() => toValue(id), async (value, _old, onCleanup) => {
    let active = true;
    const controller = new AbortController();
    onCleanup(() => {
      active = false;
      controller.abort();
    });
    view.value = { data: null, error: null, loading: true };
    try {
      const data = await load(value, controller.signal);
      if (active) view.value = { data, error: null, loading: false };
    } catch (error) {
      if (active) view.value = { data: null, error, loading: false };
    }
  }, { immediate: true });
  return { view, stop };
}
```

Each run owns success, error, and loading publication until invalidation. Abort
limits work; the active guard also covers loaders that finish despite abort.
The async callback consumes failures. Vue batches default watchers, so the
example does not promise immediate replacement on every synchronous mutation.
Scoped checks exercised replacement after the watcher ran, late success and
rejection, and stopping before settlement. A manual `refetch` API would also need ownership
and cleanup across calls; the inherited overlapping `execute()` example did not
provide that guarantee.

## Composable and lifecycle ownership

For changing listener targets, remove a listener from the exact target used
when it was added. Reading the latest target only during unmount can leave the
old listener attached. Watch the target and clean up each registration when the
contract requires target changes. Return refs when consumers need continued
updates; returning a snapshot is valid when documented as such. See
[composables](https://vuejs.org/guide/reusability/composables.html).

`useTemplateRef` (3.5) accepts a string key, not a ref holding a changing key.
Its value can be null before mount or when the element is removed. `useId` (3.5)
supports stable server/client IDs; check actual label associations and hydration.
Neither API is mandatory when the existing design works. See
[Composition API helpers](https://vuejs.org/api/composition-api-helpers.html).

`defineModel` (3.4) is optional; an explicit prop and update event is valid.
A model default can desynchronise parent and child when the parent supplies no
value. See [`<script setup>`](https://vuejs.org/api/sfc-script-setup.html).
With `KeepAlive`, deactivation differs from unmount: work that should pause when
hidden needs the corresponding lifecycle policy. See
[KeepAlive](https://vuejs.org/guide/built-ins/keep-alive.html).

## Templates and derived state

Check keys against actual state preservation during reordering. An index key is
not independently wrong for a static, stateless list. Combining an index into a
key does not repair identity across reordering. On the same node, `v-if` has
priority over `v-for`, so a condition cannot use that loop's variable there.
Filtering first or using a keyed wrapping template are valid alternatives. See
[list rendering](https://vuejs.org/guide/essentials/list.html).

Computed getters should derive values without changing other state or performing
requests. Caching depends on reactive inputs; it does not mean a getter runs on
every access. Trace observable state changes before treating diagnostic logging
as a correctness defect. See
[computed properties](https://vuejs.org/guide/essentials/computed.html).

`Teleport defer` (3.5) resolves its target later in the same mount/update tick;
it does not wait for an arbitrary future element. See
[Teleport](https://vuejs.org/guide/built-ins/teleport.html).

## Performance and clean controls

Require a measured workload before recommending shallow reactivity, `v-memo`,
virtual lists, lazy components, or caching. With shallow state, nested changes
need an appropriate replacement or explicit trigger. A `v-memo` dependency list
must cover changes needed by the rendered subtree or it can hide updates.
Check virtual-list accessibility and item sizing against the selected library's
version. No VueUse API example or compatibility claim is retained by this audit.
See [Vue performance guidance](https://vuejs.org/guide/best-practices/performance.html).

Keep valid alternatives as clean controls: `props.count`, getter-based reactive
inputs, explicit prop/update pairs, synchronously owned watchers, ordinary deep
refs, inline event handlers, and non-virtual lists can all meet requirements.
Pattern recognition alone is insufficient finding evidence.
