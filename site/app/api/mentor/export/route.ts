import type { NextRequest } from "next/server";
import { isMentor } from "@/lib/auth";
import { roster } from "@/lib/roster";
export async function GET(req: NextRequest) {
  if (!isMentor(req)) return new Response("Mentor login required", { status: 401 });
  const rows = await roster();
  const head = ["roll", "name", "current_week", "sections_done", "sections_total", "quiz_accuracy", "videos_watched", "code_done", "last_active", "midterm_repo", "endterm_repo", "cup_score"];
  const esc = (v: unknown) => { const s = v == null ? "" : String(v); return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
  const lines = rows.map((r) => [r.roll, r.name, r.current_week, r.sections_done, r.sections_total, r.quiz_accuracy, r.videos_watched, r.code_done, r.last_active, r.midterm?.repo_url, r.endterm?.repo_url, r.cup_score].map(esc).join(","));
  return new Response([head.join(","), ...lines].join("\n"), {
    headers: { "Content-Type": "text/csv; charset=utf-8", "Content-Disposition": `attachment; filename="remind-progress-${new Date().toISOString().slice(0, 10)}.csv"` },
  });
}
