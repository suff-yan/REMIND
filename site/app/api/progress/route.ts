import type { NextRequest } from "next/server";
import { db } from "@/lib/store";
import { getRoll } from "@/lib/auth";
import { bad, body, guard, ok } from "@/lib/http";
import { allSectionIds } from "@/lib/content";

export const POST = guard(async (req: NextRequest) => {
  const roll = getRoll(req);
  if (!roll) return bad("Log in to save progress.", 401);
  const b = await body<{ section_id?: string; video_watched?: boolean; quiz_score?: number; code_completed?: boolean; completed?: boolean }>(req);
  const sid = String(b.section_id ?? "");
  if (!allSectionIds().some((s) => s.id === sid)) return bad("Unknown section.");
  const prev = (await db.getProgress(roll)).find((p) => p.section_id === sid);
  const score = typeof b.quiz_score === "number" ? Math.max(0, Math.min(100, Math.round(b.quiz_score))) : null;
  const best = score === null ? prev?.quiz_score ?? null : Math.max(score, prev?.quiz_score ?? 0);
  const row = {
    roll, section_id: sid,
    video_watched: !!(prev?.video_watched || b.video_watched),
    quiz_score: best,
    quiz_passed: (best ?? 0) >= 70,
    code_completed: !!(prev?.code_completed || b.code_completed),
    completed: !!(prev?.completed || b.completed),
    updated_at: new Date().toISOString(),
  };
  await db.upsertProgress(row);
  await db.updateStudent(roll, { last_active: row.updated_at });
  return ok({ progress: row });
});
