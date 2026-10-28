import { shallowRef, toValue, watch } from 'vue';
import type { MaybeRefOrGetter } from 'vue';

type User = { name: string };
type LoadUser = (id: string, signal: AbortSignal) => Promise<User>;
type View = { data: User | null; error: unknown; loading: boolean };

export function useUser(id: MaybeRefOrGetter<string>, load: LoadUser) {
  const view = shallowRef<View>({
    data: null, error: null, loading: true,
  });
  const initialId = toValue(id);
  const stop = watch(() => initialId, async (value, _old, onCleanup) => {
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
