"use client";
import { useEffect, useState } from "react";
import { Upload } from "lucide-react";
import { useSession } from "@/components/Session";

type Row = { who: string; score: number | null; retention: number | null; reviews: number | null; exam_pass: number | null; error: string | null; uploaded_at: string; evaluated_at: string | null };

export function CupBoard() {
  const { user, cup, post, refresh } = useSession();
  const [rows, setRows] = useState<Row[]>([]);
  const [msg, setMsg] = useState<{ t: string; err?: boolean } | null>(null);
  const load = () => fetch("/api/cup", { cache: "no-store" }).then((r) => r.json()).then((d) => setRows(d.rows ?? []));
  useEffect(() => { load(); }, []);
  return (
    <div className="mt-10 grid gap-8">
      <div className="panel flex flex-wrap items-center gap-3 px-5 py-4 text-sm">
        {user ? (
          <>
            <label className="btn btn-primary cursor-pointer"><Upload size={14} strokeWidth={1.5} /> Upload entry.json
              <input type="file" accept=".json,application/json" className="hidden" onChange={async (e) => {
                const file = e.target.files?.[0]; if (!file) return;
                let entry; try { entry = JSON.parse(await file.text()); } catch { return setMsg({ t: "That file isn't valid JSON.", err: true }); }
                const d = await post("/api/cup", { entry });
                setMsg(d.ok ? { t: d.message } : { t: d.error, err: true }); if (d.ok) { refresh(); load(); }
              }} /></label>
            <span className="text-slate">{cup ? `Your entry: uploaded ${new Date(cup.uploaded_at).toLocaleString("en-IN")}${cup.score != null ? ` · score ${cup.score}` : " · awaiting tonight’s scoring"}` : "No entry yet."}</span>
          </>
        ) : <span className="text-slate">Log in to upload an entry.</span>}
        {msg && <span className={`w-full ${msg.err ? "text-amber" : "text-slate"}`}>{msg.t}</span>}
      </div>
      <table className="w-full text-sm">
        <thead><tr className="border-b border-ink text-left">
          <th className="py-2 pr-3 font-medium">#</th><th className="pr-3 font-medium">Entrant</th><th className="pr-3 text-right font-medium">Score</th>
          <th className="pr-3 text-right font-medium">Recall %</th><th className="pr-3 text-right font-medium">Reviews</th><th className="text-right font-medium">Exam pass %</th>
        </tr></thead>
        <tbody>
          {rows.length === 0 && <tr><td colSpan={6} className="py-6 text-center text-slate">No entries yet. The leaderboard opens in Week 5.</td></tr>}
          {rows.map((r, i) => (
            <tr key={r.who} className="border-b border-rule">
              <td className="py-2 pr-3 font-mono text-slate">{r.score != null ? i + 1 : "–"}</td>
              <td className="pr-3">{r.who}{r.error && <span className="ml-2 text-xs text-amber">{r.error}</span>}</td>
              <td className="pr-3 text-right font-mono font-semibold">{r.score ?? "pending"}</td>
              <td className="pr-3 text-right font-mono">{r.retention ?? "–"}</td>
              <td className="pr-3 text-right font-mono">{r.reviews ?? "–"}</td>
              <td className="text-right font-mono">{r.exam_pass ?? "–"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
