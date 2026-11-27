"use client";
import { createContext, useCallback, useContext, useEffect, useState } from "react";

export type Prog = { section_id: string; video_watched: boolean; quiz_score: number | null; quiz_passed: boolean; code_completed: boolean; completed: boolean };
type Sub = { kind: string; repo_url: string; video_url: string | null; report_url: string | null; submitted_at: string };
type Ctx = {
  loading: boolean;
  user: { roll: string; name: string } | null;
  progress: Record<string, Prog>;
  submissions: Sub[];
  cup: { score: number | null; uploaded_at: string; evaluated_at: string | null; error: string | null } | null;
  refresh: () => Promise<void>;
  save: (section_id: string, patch: Partial<Prog>) => Promise<string | null>;
  post: (url: string, data: object) => Promise<any>;
};
const C = createContext<Ctx | null>(null);
export const useSession = () => useContext(C)!;

export async function postJSON(url: string, data: object) {
  const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
  return r.json().catch(() => ({ ok: false, error: "Network error" }));
}

export function SessionProvider({ children }: { children: React.ReactNode }) {
  const [state, set] = useState<Omit<Ctx, "refresh" | "save" | "post">>({ loading: true, user: null, progress: {}, submissions: [], cup: null });
  const refresh = useCallback(async () => {
    try {
      const d = await fetch("/api/me", { cache: "no-store" }).then((r) => r.json());
      set({ loading: false, user: d.user, submissions: d.submissions ?? [], cup: d.cup ?? null,
        progress: Object.fromEntries((d.progress ?? []).map((p: Prog) => [p.section_id, p])) });
    } catch { set((s) => ({ ...s, loading: false })); }
  }, []);
  useEffect(() => { refresh(); }, [refresh]);
  const save = useCallback(async (section_id: string, patch: Partial<Prog>) => {
    if (!state.user) return "Log in (top of the page) to save your progress.";
    const d = await postJSON("/api/progress", { section_id, ...patch });
    if (!d.ok) return d.error;
    set((s) => ({ ...s, progress: { ...s.progress, [section_id]: d.progress } }));
    return null;
  }, [state.user]);
  return <C.Provider value={{ ...state, refresh, save, post: postJSON }}>{children}</C.Provider>;
}
