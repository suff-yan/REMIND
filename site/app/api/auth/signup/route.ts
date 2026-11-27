import type { NextRequest } from "next/server";
import { db } from "@/lib/store";
import { PIN_RE, ROLL_RE, STUDENT_COOKIE, cookieOpts, hashPin, normRoll, studentToken } from "@/lib/auth";
import { bad, body, guard, ok } from "@/lib/http";

export const POST = guard(async (req: NextRequest) => {
  const b = await body<{ roll?: string; name?: string; pin?: string }>(req);
  const roll = normRoll(b.roll), name = String(b.name ?? "").trim(), pin = String(b.pin ?? "");
  if (!ROLL_RE.test(roll)) return bad("Roll number should look like 24B0392.");
  if (name.length < 2 || name.length > 80) return bad("Please enter your full name.");
  if (!PIN_RE.test(pin)) return bad("PIN must be exactly 4 digits.");
  if (!(await db.isAllowed(roll))) return bad("This roll number isn't on the selected-mentee list yet. Message your mentors.", 403);
  if (await db.getStudent(roll)) return bad("An account already exists for this roll number. Log in instead.", 409);
  const now = new Date().toISOString();
  await db.createStudent({ roll, name, pin_hash: hashPin(pin), failed_attempts: 0, locked_until: null, created_at: now, last_active: now });
  const res = ok({ roll, name });
  res.cookies.set(STUDENT_COOKIE, studentToken(roll), cookieOpts(60));
  return res;
});
