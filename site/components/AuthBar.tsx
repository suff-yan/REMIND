"use client";
import { useState } from "react";
import { KeyRound, LogOut, UserPlus } from "lucide-react";
import { postJSON, useSession } from "./Session";

type Mode = "login" | "signup" | "forgot" | "reset";

export function AuthBar({ totalSections }: { totalSections: number }) {
  const { user, loading, progress, refresh } = useSession();
  const [mode, setMode] = useState<Mode>("login");
  const [f, setF] = useState({ roll: "", name: "", pin: "", code: "" });
  const [msg, setMsg] = useState<{ t: string; err?: boolean } | null>(null);
  const [busy, setBusy] = useState(false);
  const up = (k: keyof typeof f) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setF({ ...f, [k]: k === "roll" ? e.target.value.toUpperCase().replace(/\s/g, "") : k === "pin" || k === "code" ? e.target.value.replace(/\D/g, "") : e.target.value });

  async function submit(e: React.FormEvent) {
    e.preventDefault(); setBusy(true); setMsg(null);
    const url = { login: "/api/auth/login", signup: "/api/auth/signup", forgot: "/api/auth/forgot", reset: "/api/auth/reset" }[mode];
    const d = await postJSON(url, f);
    setBusy(false);
    if (!d.ok) return setMsg({ t: d.error, err: true });
    if (mode === "forgot") { setMode("reset"); return setMsg({ t: d.message }); }
    setF({ roll: "", name: "", pin: "", code: "" }); await refresh();
  }

  if (loading) return <div className="h-11 border-b border-rule bg-stone" />;

  if (user) {
    const done = Object.values(progress).filter((p) => p.completed || p.quiz_passed).length;
    return (
      <div className="border-b border-rule bg-stone">
        <div className="mx-auto flex h-11 max-w-[1200px] items-center gap-4 px-6 text-sm">
          <span className="font-mono text-ink">{user.roll}</span>
          <span className="text-slate">{user.name}</span>
          <span className="ml-auto flex items-center gap-3 text-slate">
            <span className="font-mono">{done}/{totalSections}</span> sections
            <span className="bar w-28"><span style={{ width: `${(100 * done) / totalSections}%` }} /></span>
          </span>
          <button className="flex items-center gap-1 text-slate hover:text-ink" onClick={async () => { await postJSON("/api/auth/logout", {}); refresh(); }}>
            <LogOut size={14} strokeWidth={1.5} /> Log out
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="border-b border-rule bg-stone">
      <form onSubmit={submit} className="mx-auto flex max-w-[1200px] flex-wrap items-center gap-2 px-6 py-2 text-sm">
        <span className="mr-1 text-slate">
          {mode === "signup" ? "Create your profile" : mode === "forgot" ? "Reset PIN: we’ll email a code to your LDAP inbox" : mode === "reset" ? "Enter the code from your LDAP inbox" : "Track your progress"}
        </span>
        <input className="input w-28" placeholder="24B0392" value={f.roll} onChange={up("roll")} aria-label="IITB roll number" maxLength={7} required />
        {mode === "signup" && <input className="input w-44 font-sans" placeholder="Full name" value={f.name} onChange={up("name")} aria-label="Full name" required />}
        {mode === "reset" && <input className="input w-24" placeholder="6-digit code" value={f.code} onChange={up("code")} inputMode="numeric" maxLength={6} aria-label="Reset code" required />}
        {mode !== "forgot" && <input className="input w-24" type="password" placeholder={mode === "reset" ? "new PIN" : "PIN"} value={f.pin} onChange={up("pin")} inputMode="numeric" maxLength={4} aria-label="4-digit PIN" required />}
        <button className="btn btn-primary" disabled={busy}>
          {mode === "signup" ? <><UserPlus size={14} strokeWidth={1.5} /> Create</> : mode === "forgot" ? "Send code" : mode === "reset" ? "Set PIN" : <><KeyRound size={14} strokeWidth={1.5} /> Log in</>}
        </button>
        <span className="ml-1 flex gap-3 text-slate">
          {mode !== "login" && <button type="button" className="underline" onClick={() => { setMode("login"); setMsg(null); }}>Log in</button>}
          {mode !== "signup" && <button type="button" className="underline" onClick={() => { setMode("signup"); setMsg(null); }}>New here?</button>}
          {mode === "login" && <button type="button" className="underline" onClick={() => { setMode("forgot"); setMsg(null); }}>Forgot PIN</button>}
        </span>
        {msg && <span className={`w-full text-xs ${msg.err ? "text-amber" : "text-slate"}`} role="status">{msg.t}</span>}
      </form>
    </div>
  );
}
