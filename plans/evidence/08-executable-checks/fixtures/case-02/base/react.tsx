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
