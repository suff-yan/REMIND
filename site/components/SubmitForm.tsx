"use client";
import { useState } from "react";
import { Send } from "lucide-react";
import { useSession } from "./Session";

export function SubmitForm({ kind }: { kind: "midterm" | "endterm" }) {
  const { user, submissions, post, refresh } = useSession();
  const mine = submissions.find((s) => s.kind === kind);
  const [f, setF] = useState({ repo_url: mine?.repo_url ?? "", video_url: mine?.video_url ?? "", report_url: mine?.report_url ?? "" });
  const [msg, setMsg] = useState<{ t: string; err?: boolean } | null>(null);
  if (!user) return <p className="panel px-5 py-4 text-sm text-slate">Log in with your roll number (top of the page) to submit.</p>;
  return (
    <form className="panel grid gap-3 px-5 py-4" onSubmit={async (e) => {
      e.preventDefault();
      const d = await post("/api/submissions", { kind, ...f });
      setMsg(d.ok ? { t: "Submitted. You can resubmit until the deadline; the latest one counts." } : { t: d.error, err: true });
      if (d.ok) refresh();
    }}>
      <p className="font-serif text-lg font-semibold">Submit your {kind === "midterm" ? "mid-term" : "end-term"}</p>
      {mine && <p className="font-mono text-xs text-slate">Last submitted {new Date(mine.submitted_at).toLocaleString("en-IN")}</p>}
      <label className="grid gap-1 text-sm">GitHub repository <input className="input" placeholder={`https://github.com/you/remind-${kind}-${user.roll.toLowerCase()}`} value={f.repo_url} onChange={(e) => setF({ ...f, repo_url: e.target.value })} required /></label>
      <label className="grid gap-1 text-sm">Demo video link <input className="input" placeholder="https://youtu.be/… (unlisted) or Drive link" value={f.video_url} onChange={(e) => setF({ ...f, video_url: e.target.value })} required /></label>
      {kind === "endterm" && <label className="grid gap-1 text-sm">Report PDF link <input className="input" placeholder="https://github.com/…/report/report.pdf" value={f.report_url} onChange={(e) => setF({ ...f, report_url: e.target.value })} required /></label>}
      <div className="flex items-center gap-3"><button className="btn btn-primary"><Send size={14} strokeWidth={1.5} /> {mine ? "Resubmit" : "Submit"}</button>
        {msg && <span className={`text-sm ${msg.err ? "text-amber" : "text-slate"}`}>{msg.t}</span>}</div>
    </form>
  );
}
