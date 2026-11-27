import type { NextRequest } from "next/server";
import { db } from "@/lib/store";
import { getRoll } from "@/lib/auth";
import { bad, body, guard, ok } from "@/lib/http";

const isUrl = (u: string) => { try { return ["http:", "https:"].includes(new URL(u).protocol); } catch { return false; } };

export const POST = guard(async (req: NextRequest) => {
  const roll = getRoll(req);
  if (!roll) return bad("Log in to submit.", 401);
  const b = await body<{ kind?: string; repo_url?: string; video_url?: string; report_url?: string }>(req);
  const kind = b.kind === "endterm" ? "endterm" : b.kind === "midterm" ? "midterm" : null;
  if (!kind) return bad("Unknown submission type.");
  const repo = String(b.repo_url ?? "").trim();
  if (!/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+\/?$/.test(repo)) return bad("Repo link should look like https://github.com/you/remind-midterm-24b0392");
  const video = String(b.video_url ?? "").trim() || null, report = String(b.report_url ?? "").trim() || null;
  if (!video || !isUrl(video)) return bad("Add a link to your demo video.");
  if (kind === "endterm" && (!report || !isUrl(report))) return bad("Add a link to your report PDF.");
  const row = { roll, kind, repo_url: repo, video_url: video, report_url: report, submitted_at: new Date().toISOString() } as const;
  await db.upsertSubmission(row);
  return ok({ submission: row });
});
