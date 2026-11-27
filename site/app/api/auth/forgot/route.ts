import crypto from "node:crypto";
import type { NextRequest } from "next/server";
import { db } from "@/lib/store";
import { hashPin, ldapEmail, normRoll } from "@/lib/auth";
import { body, guard, ok } from "@/lib/http";
import { sendMail } from "@/lib/mail";

export const POST = guard(async (req: NextRequest) => {
  const roll = normRoll((await body<{ roll?: string }>(req)).roll);
  const st = await db.getStudent(roll);
  if (st) {
    const code = String(crypto.randomInt(100000, 1000000));
    await db.setPinReset({ roll, code_hash: hashPin(code), expires_at: new Date(Date.now() + 15 * 60000).toISOString() });
    await sendMail(ldapEmail(roll), "Your Re-Mind PIN reset code",
      `Hi ${st.name},\n\nYour Re-Mind reset code is ${code}. It expires in 15 minutes.\n\nIf you didn't ask for this, ignore this email.\n\n- Re-Mind mentors, WiDS 6.0`);
  }
  // Same answer either way, so nobody can probe which roll numbers have accounts.
  return ok({ message: `If ${roll} has an account, a code was sent to ${ldapEmail(roll)}.` });
});
