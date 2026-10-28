# TypeScript and JavaScript review guide

Use the [review contract](review-contract.md) and the target's compiler, runtime,
`tsconfig`, and lint configuration. Record TypeScript, Node.js or browser, and
library versions before applying version-sensitive advice. This audit uses the
TypeScript 6.0 documentation; it does not establish a supported compiler matrix.
The [reference status](reference-status.md) records the exercised versions and remaining limits.

## Types and runtime boundaries

Type annotations, assertions (`as T`, `!`), and generic response types do not
validate external data. Follow untrusted JSON, storage, and message inputs to
their first use. Check the actual fields needed by the consumer. For example,
testing that `value` exists does not prove that it is a string:

```typescript
function readValue(data: unknown): string {
  if (typeof data !== 'object' || data === null ||
      !('value' in data) || typeof data.value !== 'string') {
    throw new Error('Expected a string value');
  }
  return data.value;
}
```

This standalone example targets TypeScript 6.0 with `strict: true`,
`noUncheckedIndexedAccess: true`, and `target: ES2022`. Compilation and runtime
checks passed on TypeScript 6.0.3 and Node.js 24.22.1. It validates one field,
not a complete application schema.
`unknown` forces inspection; a truthful type guard or schema validator must still
establish its claimed type. An intentional `any` at an integration boundary is
not independently a defect. Identify an unsafe consumer or violated project rule.
See [everyday types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
and [narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html).

For unions, check that narrowing matches the operation: both `string` and
`string[]` have `.length`, so reading that property is a valid clean control.
An array-only operation such as `.push()` requires different evidence. Check
null, missing discriminants, and exhaustive handling where the input contract
requires them. Compile-time exhaustiveness cannot establish the shape of JSON.

## Indexed access, generics, and compiler settings

An empty array or absent dictionary key can produce `undefined`. Inspect the
lookup's bounds and caller guarantees even when the compiler reports a plain
value type. `noUncheckedIndexedAccess` adds `undefined` to unchecked indexed
reads; a tuple with a known element has different guarantees. See the
[compiler option](https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html).
Do not prescribe `strict` or extra flags as universal correctness gates.

Check that generics preserve a real relation between inputs and outputs.
`K extends keyof T` constrains a typed key, but does not validate an arbitrary
runtime string. Mapped, conditional, and template literal types remain
compile-time descriptions. Prefer the project's working design over a rewrite
for generic reuse. See [generics](https://www.typescriptlang.org/docs/handbook/2/generics.html).

`readonly`, `Readonly<T>`, and `as const` do not freeze runtime objects.
Readonly properties also do not make nested objects immutable. Trace shared
aliases and ownership before calling mutation a defect; copying an array leaves
its elements shared. See [object types](https://www.typescriptlang.org/docs/handbook/2/objects.html).

## Promise rejection and task ownership

Trace each promise to an awaiting caller, returned chain, or terminal rejection
handler. An async function may correctly propagate failure to its caller without
local `try/catch`. Conversely, throwing inside a detached `.catch()` creates a
new rejected promise. `void task()` discards a value; it does not handle rejection.
Lint configuration and intentional background work need the project's contract.
See [no-floating-promises](https://typescript-eslint.io/rules/no-floating-promises/).

`forEach(async ...)` does not wait for its callbacks. If completion matters,
check that the owner awaits sequential work or a collected promise set.
`Promise.all` is valid when every result is required: early rejection does not
cancel the other operations. `allSettled` is appropriate when independent
outcomes must all be observed. Neither choice alone is a bug. See the
[ECMAScript promise algorithms](https://tc39.es/ecma262/multipage/control-abstraction-objects.html#sec-promise.all).

## Fetch, cancellation, and stale results

Fetch resolves on HTTP error responses; inspect `response.ok` when success is
required, then validate the body for the consumer. Cancellation can reject fetch
or body consumption. It does not undo a server mutation or cancel arbitrary
post-processing. See the [Fetch standard](https://fetch.spec.whatwg.org/#fetch-method).

For a latest-request-wins interface, trace success, error, and loading writes.
An obsolete request must not publish any of them after replacement or disposal.
Pair cancellation with an ownership check when continuations can outlive the
request. An abort-only chain that rethrows other errors without an owner is not
a complete repair. See the illustrative [React effect](react.md#effects-and-request-ownership)
and [Vue watcher](vue.md#watchers-and-request-ownership); both have scoped checks under the versions recorded in the reference status.

Use controlled promises to finish B before A, reject A after B succeeds, dispose
before settlement, and change reactive input. Check both a transport that honours
abort and one whose work is already completing. Avoid network timing as evidence.
