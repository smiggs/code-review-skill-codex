import { test, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { JSDOM } from 'jsdom';
const dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'https://package-08.example/' });
for (const key of ['window', 'document', 'HTMLElement', 'Element', 'SVGElement', 'Node',
  'Event', 'MouseEvent', 'FormData', 'MutationObserver']) {
  Object.defineProperty(globalThis, key, { value: dom.window[key], configurable: true });
}
Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });
globalThis.IS_REACT_ACT_ENVIRONMENT = true;
const React = await import('react');
const { renderHook, render, act, fireEvent, cleanup } = await import('@testing-library/react');
const Vue = await import('vue');
const { mount, flushPromises } = await import('@vue/test-utils');
const { useUser: reactUser } = await import(process.env.P08_REACT ?? './.generated/react.js');
const { useUser: vueUser } = await import(process.env.P08_VUE ?? './.generated/vue.js');
const { readValue } = await import(process.env.P08_READER ?? './.generated/reader.js');
const types = await import('./.generated/type-controls.js');
const wrappers = new Set();
afterEach(() => { cleanup(); for (const w of wrappers) w.unmount(); wrappers.clear(); });
function deferred() {
  let resolve, reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}
function transport(abortAware = false) {
  const requests = [];
  function load(id, signal) {
    const request = { id, signal, ...deferred() };
    requests.push(request);
    if (abortAware) signal.addEventListener('abort', () => {
      request.reject(new DOMException('Aborted', 'AbortError'));
    }, { once: true });
    return request.promise;
  }
  return { load, requests };
}
async function settle(action) {
  await act(async () => { action(); await flushPromises(); });
  await Vue.nextTick();
}
function harness(framework, service, inputKind = 'ref') {
  if (framework === 'React') {
    const hook = renderHook(({ id, load }) => reactUser(id, load), {
      initialProps: { id: 'A', load: service.load },
    });
    return {
      state: () => hook.result.current,
      change: async id => { hook.rerender({ id, load: service.load }); },
      dispose: () => hook.unmount(),
      replaceLoader: load => hook.rerender({ id: 'A', load }),
    };
  }
  const id = Vue.ref('A');
  let result;
  const wrapper = mount({
    setup() {
      result = vueUser(inputKind === 'fixed' ? 'A' :
        inputKind === 'getter' ? () => id.value : id, service.load);
      return () => Vue.h('p', result.view.value.data?.name ?? 'empty');
    },
  });
  wrappers.add(wrapper);
  return {
    state: () => result.view.value,
    change: async value => { id.value = value; await Vue.nextTick(); },
    dispose: () => { wrapper.unmount(); wrappers.delete(wrapper); },
    stop: () => result.stop(), text: () => wrapper.text(),
  };
}
function stateEquals(subject, data, error, loading) {
  assert.deepEqual(subject.state(), { data, error, loading });
}
test('value reader accepts strings and rejects malformed external values', () => {
  assert.equal(readValue({ value: 'ready' }), 'ready');
  assert.equal(readValue({ value: '' }), '');
  for (const value of [null, undefined, 4, 'text', {}, { value: 4 }, { value: null }]) {
    assert.throws(() => readValue(value), /Expected a string value/);
  }
});
test('type controls distinguish safe length, unchecked access, and assertions', () => {
  assert.equal(types.length('abc'), 3);
  assert.equal(types.length(['a', 'b']), 2);
  assert.equal(types.first([]), undefined);
  assert.equal(types.guarded([]), undefined);
  assert.throws(() => types.unsafe([]), TypeError);
  assert.throws(() => types.assertOnly({ value: 4 }).value.toUpperCase(), TypeError);
});
test('returned rejection has an awaiting owner and Promise.all does not cancel work', async () => {
  const failure = new Error('failed');
  async function propagate() { return Promise.reject(failure); }
  await assert.rejects(propagate(), error => error === failure);
  const outstanding = deferred();
  let completed = false;
  const other = outstanding.promise.then(() => { completed = true; });
  await assert.rejects(Promise.all([Promise.reject(failure), other]), error => error === failure);
  outstanding.resolve(); await other;
  assert.equal(completed, true);
});
for (const framework of ['React', 'Vue']) {
  for (const abortAware of [false, true]) {
    test(`${framework}: latest completion wins with abortAware=${abortAware}`, async () => {
      const service = transport(abortAware);
      const subject = harness(framework, service);
      await subject.change('B');
      assert.equal(service.requests[0].signal.aborted, true);
      assert.deepEqual(service.requests.map(r => r.id), ['A', 'B']);
      await settle(() => service.requests[1].resolve({ name: 'B' }));
      stateEquals(subject, { name: 'B' }, null, false);
      await settle(() => service.requests[0].resolve({ name: 'A' }));
      stateEquals(subject, { name: 'B' }, null, false);
    });
  }
  test(`${framework}: obsolete rejection cannot replace current success`, async () => {
    const service = transport(); const subject = harness(framework, service);
    await subject.change('B');
    await settle(() => service.requests[1].resolve({ name: 'B' }));
    await settle(() => service.requests[0].reject(new Error('obsolete')));
    stateEquals(subject, { name: 'B' }, null, false);
  });
  test(`${framework}: obsolete settlement cannot clear current loading`, async () => {
    const service = transport(); const subject = harness(framework, service);
    await subject.change('B');
    await settle(() => service.requests[0].resolve({ name: 'A' }));
    stateEquals(subject, null, null, true);
    const failure = new Error('current');
    await settle(() => service.requests[1].reject(failure));
    stateEquals(subject, null, failure, false);
  });
  for (const outcome of ['resolve', 'reject']) {
    test(`${framework}: disposal before ${outcome} aborts and consumes settlement`, async () => {
      const service = transport(); const subject = harness(framework, service);
      const before = subject.state(); subject.dispose();
      assert.equal(service.requests[0].signal.aborted, true);
      await settle(() => service.requests[0][outcome](outcome === 'resolve' ?
        { name: 'late' } : new Error('late')));
      assert.equal(subject.state(), before);
    });
  }
}
test('React: replacing loader invalidates the previous request', async () => {
  const previous = transport(); const replacement = transport();
  const subject = harness('React', previous);
  subject.replaceLoader(replacement.load);
  assert.equal(previous.requests[0].signal.aborted, true);
  await settle(() => replacement.requests[0].resolve({ name: 'replacement' }));
  await settle(() => previous.requests[0].resolve({ name: 'previous' }));
  stateEquals(subject, { name: 'replacement' }, null, false);
});
test('React: root strict-effects cleanup leaves only its final request active', async () => {
  const { createRoot } = await import('react-dom/client');
  const service = transport(true);
  const host = document.createElement('div');
  const root = createRoot(host, { unstable_strictMode: true });
  let view;
  function Subject() { view = reactUser('A', service.load); return null; }
  try {
    await act(async () => { root.render(React.createElement(Subject)); });
    assert.equal(service.requests.length, 2);
    assert.equal(service.requests[0].signal.aborted, true);
    await settle(() => service.requests[1].resolve({ name: 'active' }));
    assert.equal(view.data.name, 'active');
  } finally { await act(async () => root.unmount()); }
});
test('React: conditional child and conditional use(context) are clean controls', () => {
  const context = React.createContext('context');
  function Child() { const [count] = React.useState(1); return React.createElement('p', null, count); }
  function Parent({ show }) {
    const value = show ? React.use(context) : 'hidden';
    return React.createElement('section', null, value, show ? React.createElement(Child) : null);
  }
  const ui = render(React.createElement(Parent, { show: false }));
  assert.equal(ui.container.textContent, 'hidden');
  ui.rerender(React.createElement(Parent, { show: true }));
  assert.equal(ui.container.textContent, 'context1');
  ui.rerender(React.createElement(Parent, { show: false }));
  assert.equal(ui.container.textContent, 'hidden');
});
test('React: nested types reset local state while stable types preserve it', () => {
  function Stable() {
    const [value, setValue] = React.useState(0);
    return React.createElement('button', { onClick: () => setValue(value + 1) }, value);
  }
  function Parent({ nested }) {
    function Nested() { return React.createElement(Stable); }
    return React.createElement(nested ? Nested : Stable);
  }
  for (const nested of [false, true]) {
    const ui = render(React.createElement(Parent, { nested }));
    fireEvent.click(ui.getByRole('button'));
    assert.equal(ui.container.textContent, '1');
    ui.rerender(React.createElement(Parent, { nested }));
    assert.equal(ui.container.textContent, nested ? '0' : '1'); ui.unmount();
  }
});
for (const kind of ['getter', 'fixed']) {
  test(`Vue: ${kind} input obeys its declared reactive contract`, async () => {
    const service = transport(); const subject = harness('Vue', service, kind);
    await subject.change('B');
    assert.equal(service.requests.length, kind === 'getter' ? 2 : 1);
    const latest = service.requests.at(-1);
    await settle(() => latest.resolve({ name: latest.id }));
    assert.equal(subject.text(), kind === 'getter' ? 'B' : 'A');
  });
}
test('Vue: explicit stop prevents a late result from changing the exposed ref', async () => {
  const service = transport(); const subject = harness('Vue', service);
  subject.stop(); const before = subject.state();
  assert.equal(service.requests[0].signal.aborted, true);
  await settle(() => service.requests[0].resolve({ name: 'late' }));
  assert.equal(subject.state(), before);
});
for (const label of ['34', '35']) {
  test(`Vue ${label}: exact props SFC reflects the compiler boundary`, async () => {
    const runtime = await import(label === '34' ? 'vue34' : 'vue');
    const component = (await import(`./.generated/props${label}.js`)).default;
    const count = runtime.ref(1); const host = document.createElement('div');
    const app = runtime.createApp({ render: () => runtime.h(component, { count: count.value, items: [] }) });
    const observations = []; const originalLog = console.log;
    console.log = value => observations.push(value);
    try {
      app.mount(host); assert.equal(host.textContent, '1 / 0');
      count.value = 2; await runtime.nextTick();
      assert.equal(host.textContent, '2 / 0');
      assert.deepEqual(observations, label === '35' ? [2] : []);
    } finally { app.unmount(); console.log = originalLog; }
  });
}
test('Vue: props getter and explicit prop/update event remain valid designs', async () => {
  const wrapper = mount({
    props: ['modelValue'], emits: ['update:modelValue'],
    setup(props, { emit }) {
      const value = Vue.computed(() => props.modelValue);
      return () => Vue.h('button', { onClick: () => emit('update:modelValue', value.value + 1) }, value.value);
    },
  }, { props: { modelValue: 1 } });
  wrappers.add(wrapper); await wrapper.setProps({ modelValue: 2 });
  assert.equal(wrapper.text(), '2'); await wrapper.trigger('click');
  assert.deepEqual(wrapper.emitted('update:modelValue'), [[3]]);
});

test('Vue 3.5: destructured array defaults render without supplied props', async () => {
  const component = (await import('./.generated/props35.js')).default;
  const wrapper = mount(component);
  wrappers.add(wrapper);
  assert.equal(wrapper.text(), '0 / 0');
});

test('React DOM: form status observes a parent form, not a form created by its caller', async () => {
  const { useFormStatus } = await import('react-dom');
  const pending = deferred();
  let ownPending, childPending;
  function Submit() {
    childPending = useFormStatus().pending;
    return React.createElement('button', { type: 'submit' }, childPending ? 'pending' : 'ready');
  }
  function Form() {
    ownPending = useFormStatus().pending;
    return React.createElement('form', { action: async () => { await pending.promise; } }, React.createElement(Submit));
  }
  const ui = render(React.createElement(Form));
  await act(async () => { fireEvent.submit(ui.container.querySelector('form')); });
  assert.equal(ownPending, false);
  assert.equal(childPending, true);
  await settle(() => pending.resolve());
  assert.equal(childPending, false);
});
test('React: action state receives previous state before the payload', async () => {
  const pending = deferred(); const seen = [];
  const hook = renderHook(() => React.useActionState(async (previous, payload) => {
    seen.push([previous, payload.get('amount')]);
    await pending.promise;
    return previous + Number(payload.get('amount'));
  }, 3));
  const payload = new FormData(); payload.set('amount', '2');
  await act(async () => { React.startTransition(() => hook.result.current[1](payload)); });
  assert.equal(hook.result.current[2], true);
  await settle(() => pending.resolve());
  assert.deepEqual(seen, [[3, '2']]);
  assert.equal(hook.result.current[0], 5);
  assert.equal(hook.result.current[2], false);
});
test('Query v5: refetch error coexists with cached data in a Suspense query', async () => {
  const { QueryClient, QueryClientProvider, useSuspenseQuery } = await import('@tanstack/react-query');
  const client = new QueryClient({ defaultOptions: { queries: { retry: false, gcTime: Infinity } } });
  const failure = new Error('refetch failed');
  const pending = deferred();
  client.setQueryData(['user', 'A'], { name: 'cached' });
  const hook = renderHook(() => useSuspenseQuery({
    queryKey: ['user', 'A'], queryFn: () => pending.promise,
    staleTime: Infinity,
  }), { wrapper: ({ children }) => React.createElement(QueryClientProvider, { client }, children) });
  assert.equal(hook.result.current.data.name, 'cached');
  let completion;
  await act(async () => {
    completion = hook.result.current.refetch();
    pending.reject(failure);
    await completion;
    await new Promise(resolve => setTimeout(resolve, 0));
  });
  assert.equal(hook.result.current.data.name, 'cached');
  assert.equal(hook.result.current.error, failure);
  hook.unmount(); client.clear();
});
