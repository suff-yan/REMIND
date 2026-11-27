import type { NextRequest } from "next/server";
import { db } from "@/lib/store";
import { STUDENT_COOKIE, cookieOpts, normRoll, studentToken, verifyPin } from "@/lib/auth";
import { bad, body, guard, ok } from "@/lib/http";

const MAX_FAILS = 5, LOCK_MIN = 15;

export const POST = guard(async (req: NextRequest) => {
  const b = await body<{ roll?: string; pin?: string }>(req);
  const roll = normRoll(b.roll), pin = String(b.pin ?? "");
  const st = await db.getStudent(roll);
  if (!st) return bad("Roll number or PIN is incorrect.", 401);
  if (st.locked_until && new Date(st.locked_until) > new Date()) {
    const mins = Math.ceil((+new Date(st.locked_until) - Date.now()) / 60000);
    return bad(`Too many wrong PINs. Try again in ${mins} min, or use “Forgot PIN”.`, 429);
  }
  if (!verifyPin(pin, st.pin_hash)) {
    const fails = st.failed_attempts + 1;
    await db.updateStudent(roll, fails >= MAX_FAILS
      ? { failed_attempts: 0, locked_until: new Date(Date.now() + LOCK_MIN * 60000).toISOString() }
      : { failed_attempts: fails });
    return bad("Roll number or PIN is incorrect.", 401);
  }
  await db.updateStudent(roll, { failed_attempts: 0, locked_until: null, last_active: new Date().toISOString() });
  const res = ok({ roll, name: st.name });
  res.cookies.set(STUDENT_COOKIE, studentToken(roll), cookieOpts(60));
  return res;
});
