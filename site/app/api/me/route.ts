import type { NextRequest } from "next/server";
import { db } from "@/lib/store";
import { getRoll } from "@/lib/auth";
import { guard, ok } from "@/lib/http";

export const GET = guard(async (req: NextRequest) => {
  const roll = getRoll(req);
  if (!roll) return ok({ user: null });
  const st = await db.getStudent(roll);
  if (!st) return ok({ user: null });
  const [progress, submissions, cup] = await Promise.all([db.getProgress(roll), db.getSubmissions(roll), db.getCup()]);
  return ok({ user: { roll, name: st.name }, progress, submissions, cup: cup.find((c) => c.roll === roll) ?? null });
});
