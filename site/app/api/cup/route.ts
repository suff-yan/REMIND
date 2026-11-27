import type { NextRequest } from "next/server";
import { db } from "@/lib/store";
import { getRoll } from "@/lib/auth";
import { bad, body, guard, ok } from "@/lib/http";

const STATES = 18, ACTIONS = 6;
function validate(e: any): string | null {
  if (e && Array.isArray(e.policy)) {
    return e.policy.length === STATES && e.policy.every((a: unknown) => Number.isInteger(a) && (a as number) >= 0 && (a as number) < ACTIONS)
      ? null : `"policy" must be ${STATES} integers between 0 and ${ACTIONS - 1}.`;
  }
  if (e && Array.isArray(e.q)) {
    return e.q.length === STATES && e.q.every((r: unknown) => Array.isArray(r) && r.length === ACTIONS && r.every((v) => typeof v === "number" && isFinite(v)))
      ? null : `"q" must be ${STATES} rows of ${ACTIONS} numbers.`;
  }
  return 'The file needs a "q" (18×6 Q-table) or a "policy" (18 actions).';
}
const mask = (roll: string) => roll.slice(0, 3) + "••" + roll.slice(-2);

export const GET = guard(async () => {
  const [entries, students] = await Promise.all([db.getCup(), db.listStudents()]);
  const names = new Map(students.map((s) => [s.roll, s.name.split(" ")[0]]));
  const rows = entries.map((e) => ({
    who: `${names.get(e.roll) ?? "?"} · ${mask(e.roll)}`, score: e.score, retention: e.retention, reviews: e.reviews,
    exam_pass: e.exam_pass, error: e.error ? "invalid entry" : null, uploaded_at: e.uploaded_at, evaluated_at: e.evaluated_at,
  })).sort((a, b) => (b.score ?? -1e9) - (a.score ?? -1e9));
  return ok({ rows });
});

export const POST = guard(async (req: NextRequest) => {
  const roll = getRoll(req);
  if (!roll) return bad("Log in to enter the Cup.", 401);
  const { entry } = await body<{ entry?: unknown }>(req);
  if (JSON.stringify(entry ?? null).length > 20000) return bad("File too large.");
  const err = validate(entry);
  if (err) return bad(err);
  await db.upsertCup(roll, entry);
  return ok({ message: "Entry saved. It will be scored on hidden students tonight." });
});
