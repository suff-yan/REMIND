import type { NextRequest } from "next/server";
import { ROLL_RE, isMentor, normRoll } from "@/lib/auth";
import { bad, body, guard, ok } from "@/lib/http";
import { db } from "@/lib/store";
export const GET = guard(async (req: NextRequest) => {
  if (!isMentor(req)) return bad("Mentor login required.", 401);
  return ok({ rows: await db.getAllowlist() });
});
// CSV: roll,name  (header optional). Replaces the whole list.
export const POST = guard(async (req: NextRequest) => {
  if (!isMentor(req)) return bad("Mentor login required.", 401);
  const { csv } = await body<{ csv?: string }>(req);
  const rows: { roll: string; name: string | null }[] = [], badLines: string[] = [];
  for (const line of String(csv ?? "").split(/\r?\n/)) {
    if (!line.trim() || /^roll/i.test(line.trim())) continue;
    const [r, ...rest] = line.split(",");
    const roll = normRoll(r);
    if (ROLL_RE.test(roll)) rows.push({ roll, name: rest.join(",").trim() || null }); else badLines.push(line);
  }
  const uniq = [...new Map(rows.map((x) => [x.roll, x])).values()];
  await db.setAllowlist(uniq);
  return ok({ saved: uniq.length, skipped: badLines.slice(0, 20) });
});
