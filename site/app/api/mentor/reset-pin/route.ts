import type { NextRequest } from "next/server";
import { PIN_RE, hashPin, isMentor, normRoll } from "@/lib/auth";
import { bad, body, guard, ok } from "@/lib/http";
import { db } from "@/lib/store";
export const POST = guard(async (req: NextRequest) => {
  if (!isMentor(req)) return bad("Mentor login required.", 401);
  const b = await body<{ roll?: string; pin?: string }>(req);
  const roll = normRoll(b.roll), pin = String(b.pin ?? "");
  if (!PIN_RE.test(pin)) return bad("Temporary PIN must be 4 digits.");
  if (!(await db.getStudent(roll))) return bad("No such student.", 404);
  await db.updateStudent(roll, { pin_hash: hashPin(pin), failed_attempts: 0, locked_until: null });
  return ok({ message: `PIN for ${roll} reset. Tell the student their temporary PIN and ask them to change it via “Forgot PIN” if they like.` });
});
