import type { NextRequest } from "next/server";
import { MENTOR_COOKIE, checkMentorPasscode, cookieOpts, mentorToken } from "@/lib/auth";
import { bad, body, ok } from "@/lib/http";
export async function POST(req: NextRequest) {
  const { passcode } = await body<{ passcode?: string }>(req);
  await new Promise((r) => setTimeout(r, 400)); // slow down guessing
  if (!checkMentorPasscode(String(passcode ?? ""))) return bad("Wrong passcode.", 401);
  const res = ok();
  res.cookies.set(MENTOR_COOKIE, mentorToken(), cookieOpts(7));
  return res;
}
