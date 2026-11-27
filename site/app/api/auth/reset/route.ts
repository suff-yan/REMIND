import type { NextRequest } from "next/server";
import { db } from "@/lib/store";
import { PIN_RE, STUDENT_COOKIE, cookieOpts, hashPin, normRoll, studentToken, verifyPin } from "@/lib/auth";
import { bad, body, guard, ok } from "@/lib/http";

export const POST = guard(async (req: NextRequest) => {
  const b = await body<{ roll?: string; code?: string; pin?: string }>(req);
  const roll = normRoll(b.roll), code = String(b.code ?? "").trim(), pin = String(b.pin ?? "");
  if (!PIN_RE.test(pin)) return bad("New PIN must be exactly 4 digits.");
  const r = await db.takePinReset(roll);
  if (!r || new Date(r.expires_at) < new Date() || !verifyPin(code, r.code_hash)) return bad("That code is wrong or expired. Request a new one.", 401);
  await db.updateStudent(roll, { pin_hash: hashPin(pin), failed_attempts: 0, locked_until: null });
  const st = await db.getStudent(roll);
  const res = ok({ roll, name: st?.name });
  res.cookies.set(STUDENT_COOKIE, studentToken(roll), cookieOpts(60));
  return res;
});
