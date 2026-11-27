"use client";
import { useCallback, useEffect, useMemo, useState } from "react";
import { ArrowDownUp, Download, KeyRound, LogOut, Search, Upload } from "lucide-react";
import { postJSON } from "@/components/Session";

type Row = {
  roll: string; name: string; current_week: number; sections_done: number; sections_total: number; quiz_accuracy: number | null;
  videos_watched: number; code_done: number; last_active: string | null; days_idle: number | null; locked: boolean;
  midterm: { repo_url: string; video_url: string | null } | null; endterm: { repo_url: string; video_url: string | null; report_url: string | null } | null; cup_score: number | null;
};
type Data = { rows: Row[]; storage: string; allowlist_enabled: boolean; allowlist_count: number };
const cols: [keyof Row, string][] = [["roll", "Roll"], ["name", "Name"], ["current_week", "Week"], ["sections_done", "Sections"], ["quiz_accuracy", "Quiz %"], ["videos_watched", "Videos"], ["code_done", "Code"], ["last_active", "Last active"], ["cup_score", "Cup"]];

export function Dashboard() {
  const [data, setData] = useState<Data | null>(null);
  const [authed, setAuthed] = useState<boolean | null>(null);
  const [pass, setPass] = useState("");
  const [err, setErr] = useState("");
  const [q, setQ] = useState("");
  const [sort, setSort] = useState<{ k: keyof Row; dir: 1 | -1 }>({ k: "roll", dir: 1 });
  const [reset, setReset] = useState<{ roll: string; pin: string; msg?: string } | null>(null);
  const [csv, setCsv] = useState(""); const [alMsg, setAlMsg] = useState("");

  const load = useCallback(async () => {
    const r = await fetch("/api/mentor/data", { cache: "no-store" });
    if (r.status === 401) return setAuthed(false);
    setData(await r.json()); setAuthed(true);
  }, []);
  useEffect(() => { load(); }, [load]);

  const rows = useMemo(() => {
    const t = q.trim().toLowerCase();
    return (data?.rows ?? []).filter((r) => !t || r.roll.toLowerCase().includes(t) || r.name.toLowerCase().includes(t))
      .sort((a, b) => { const x = a[sort.k] ?? -1, y = b[sort.k] ?? -1; return (x > y ? 1 : x < y ? -1 : 0) * sort.dir; });
  }, [data, q, sort]);

  if (authed === null) return <div className="mx-auto max-w-[1200px] px-6 pt-10 text-sm text-slate">Loading…</div>;
  if (!authed) return (
    <form className="mx-auto max-w-sm px-6 pt-16" onSubmit={async (e) => { e.preventDefault(); const d = await postJSON("/api/mentor/login", { passcode: pass }); if (d.ok) { setErr(""); load(); } else setErr(d.error); }}>
      <h1 className="font-serif text-3xl font-semibold">Mentor dashboard</h1>
      <p className="mt-2 text-sm text-slate">Enter the mentor passcode.</p>
      <div className="mt-4 flex gap-2"><input className="input flex-1" type="password" value={pass} onChange={(e) => setPass(e.target.value)} autoFocus aria-label="Mentor passcode" />
        <button className="btn btn-primary"><KeyRound size={14} strokeWidth={1.5} /> Enter</button></div>
      {err && <p className="mt-2 text-sm text-amber">{err}</p>}
    </form>
  );

  const d = data!;
  const active7 = d.rows.filter((r) => r.days_idle !== null && r.days_idle <= 7).length;
  const avg = (f: (r: Row) => number | null) => { const v = d.rows.map(f).filter((x): x is number => x !== null); return v.length ? Math.round(v.reduce((a, b) => a + b, 0) / v.length) : null; };
  return (
    <div className="mx-auto max-w-[1300px] px-6 pt-8">
      <div className="flex flex-wrap items-end gap-6">
        <div><p className="eyebrow">Mentors</p><h1 className="font-serif text-3xl font-semibold">Cohort progress</h1></div>
        <dl className="flex gap-6 text-sm">
          <div><dt className="text-slate">Students</dt><dd className="font-mono text-lg">{d.rows.length}</dd></div>
          <div><dt className="text-slate">Active · 7 d</dt><dd className="font-mono text-lg">{active7}</dd></div>
          <div><dt className="text-slate">Avg quiz</dt><dd className="font-mono text-lg">{avg((r) => r.quiz_accuracy) ?? "–"}%</dd></div>
          <div><dt className="text-slate">Mid-term in</dt><dd className="font-mono text-lg">{d.rows.filter((r) => r.midterm).length}</dd></div>
          <div><dt className="text-slate">End-term in</dt><dd className="font-mono text-lg">{d.rows.filter((r) => r.endterm).length}</dd></div>
        </dl>
        <div className="ml-auto flex gap-2">
          <a className="btn no-underline" href="/api/mentor/export"><Download size={14} strokeWidth={1.5} /> CSV</a>
          <button className="btn" onClick={async () => { await postJSON("/api/mentor/logout", {}); setAuthed(false); }}><LogOut size={14} strokeWidth={1.5} /> Exit</button>
        </div>
      </div>
      {d.storage !== "supabase" && <p className="mt-4 rounded border border-amber bg-[#FDF3E6] px-3 py-2 text-sm">Storage: local file (Supabase variables not set). Data here is not shared across deployments.</p>}

      <div className="mt-6 flex items-center gap-2">
        <Search size={15} strokeWidth={1.5} className="text-slate" />
        <input className="input w-64 font-sans" placeholder="Filter by roll or name" value={q} onChange={(e) => setQ(e.target.value)} />
        <span className="text-xs text-slate">Idle more than 5 days is flagged in amber. PINs are stored hashed: use Reset to set a temporary one.</span>
      </div>

      <div className="mt-3 overflow-x-auto rounded-md border border-rule bg-white">
        <table className="w-full text-[13px]">
          <thead><tr className="border-b border-rule bg-stone text-left">
            {cols.map(([k, l]) => (
              <th key={k} className="px-3 py-2 font-medium">
                <button className="inline-flex items-center gap-1" onClick={() => setSort({ k, dir: sort.k === k ? (-sort.dir as 1 | -1) : 1 })}>{l}<ArrowDownUp size={11} strokeWidth={1.5} className="text-slate" /></button>
              </th>))}
            <th className="px-3 py-2 font-medium">Mid</th><th className="px-3 py-2 font-medium">End</th><th className="px-3 py-2 font-medium">PIN</th>
          </tr></thead>
          <tbody>
            {rows.length === 0 && <tr><td colSpan={12} className="px-3 py-8 text-center text-slate">No students yet.</td></tr>}
            {rows.map((r) => (
              <tr key={r.roll} className="border-b border-rule last:border-0">
                <td className="px-3 py-2 font-mono">{r.roll}</td>
                <td className="px-3">{r.name}</td>
                <td className="px-3 font-mono">{r.current_week}</td>
                <td className="px-3"><span className="flex items-center gap-2 font-mono">{r.sections_done}/{r.sections_total}<span className="bar w-14"><span style={{ width: `${(100 * r.sections_done) / r.sections_total}%` }} /></span></span></td>
                <td className="px-3 font-mono">{r.quiz_accuracy ?? "–"}</td>
                <td className="px-3 font-mono">{r.videos_watched}</td>
                <td className="px-3 font-mono">{r.code_done}</td>
                <td className={`px-3 font-mono ${r.days_idle !== null && r.days_idle > 5 ? "text-amber" : ""}`}>{r.last_active ? `${new Date(r.last_active).toLocaleDateString("en-IN")} (${r.days_idle} d)` : "–"}</td>
                <td className="px-3 font-mono">{r.cup_score ?? "–"}</td>
                <td className="px-3">{r.midterm ? <a href={r.midterm.repo_url} target="_blank" rel="noreferrer">repo</a> : <span className="text-slate">–</span>}</td>
                <td className="px-3">{r.endterm ? <a href={r.endterm.repo_url} target="_blank" rel="noreferrer">repo</a> : <span className="text-slate">–</span>}</td>
                <td className="px-3">
                  {reset?.roll === r.roll ? (
                    <form className="flex items-center gap-1" onSubmit={async (e) => { e.preventDefault(); const x = await postJSON("/api/mentor/reset-pin", { roll: r.roll, pin: reset.pin }); setReset({ ...reset, msg: x.ok ? "done" : x.error }); load(); }}>
                      <input className="input w-16 py-0.5" placeholder="0000" maxLength={4} inputMode="numeric" value={reset.pin} onChange={(e) => setReset({ roll: r.roll, pin: e.target.value.replace(/\D/g, "") })} autoFocus aria-label="Temporary PIN" />
                      <button className="btn py-0.5">Set</button>{reset.msg && <span className="text-xs text-slate">{reset.msg}</span>}
                    </form>
                  ) : (
                    <span className="flex items-center gap-2"><span className="font-mono text-slate">••••</span>{r.locked && <span className="text-xs text-amber">locked</span>}
                      <button className="text-xs underline" onClick={() => setReset({ roll: r.roll, pin: "" })}>Reset</button></span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <section className="mt-10 grid gap-3 md:grid-cols-[1fr_1fr]">
        <div>
          <h2 className="font-serif text-xl font-semibold">Selected-mentee allowlist</h2>
          <p className="mt-1 text-sm text-slate">
            {d.allowlist_enabled ? "Enforced: only these roll numbers can sign up." : "Not enforced yet (ALLOWLIST_ENABLED is not \"true\"). Anyone can sign up."} {d.allowlist_count} roll numbers saved.
          </p>
          <p className="mt-2 text-sm text-slate">Paste CSV lines <code className="font-mono">roll,name</code>. Saving replaces the whole list.</p>
        </div>
        <form onSubmit={async (e) => { e.preventDefault(); const x = await postJSON("/api/mentor/allowlist", { csv }); setAlMsg(x.ok ? `Saved ${x.saved}.${x.skipped.length ? ` Skipped: ${x.skipped.join(" | ")}` : ""}` : x.error); load(); }}>
          <textarea className="input h-32 w-full" placeholder={"roll,name\n24B0392,Asha Rao"} value={csv} onChange={(e) => setCsv(e.target.value)} />
          <div className="mt-2 flex items-center gap-3"><button className="btn"><Upload size={14} strokeWidth={1.5} /> Save allowlist</button><span className="text-xs text-slate">{alMsg}</span></div>
        </form>
      </section>
    </div>
  );
}
