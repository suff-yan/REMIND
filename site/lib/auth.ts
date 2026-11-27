import crypto from "node:crypto";
import type { NextRequest } from "next/server";

export const ROLL_RE = /^[0-9]{2}[A-Z][0-9]{4}$/; // e.g. 24B0392
export const PIN_RE = /^[0-9]{4}$/;
export const normRoll = (r: unknown) => String(r ?? "").trim().toUpperCase();
export const ldapEmail = (roll: string) => `${roll.toLowerCase()}@iitb.ac.in`;

const secret = () => {
  const s = process.env.SESSION_SECRET;
  if (!s && process.env.NODE_ENV === "production") throw new Error("SESSION_SECRET is not set");
  return s || "dev-only-secret";
};

export function hashPin(pin: string) {
  const salt = crypto.randomBytes(16).toString("hex");
  const h = crypto.scryptSync(pin, salt, 32).toString("hex");
  return `scrypt$${salt}$${h}`;
}
export function verifyPin(pin: string, stored: string) {
  const [, salt, h] = stored.split("$");
  if (!salt || !h) return false;
  const got = crypto.scryptSync(pin, salt, 32);
  return crypto.timingSafeEqual(got, Buffer.from(h, "hex"));
}

function sign(payload: object) {
  const body = Buffer.from(JSON.stringify(payload)).toString("base64url");
  const mac = crypto.createHmac("sha256", secret()).update(body).digest("base64url");
  return `${body}.${mac}`;
}
function unsign<T>(token?: string): T | null {
  if (!token) return null;
  const [body, mac] = token.split(".");
  if (!body || !mac) return null;
  const want = crypto.createHmac("sha256", secret()).update(body).digest("base64url");
  if (want.length !== mac.length || !crypto.timingSafeEqual(Buffer.from(want), Buffer.from(mac))) return null;
  const p = JSON.parse(Buffer.from(body, "base64url").toString()) as T & { exp: number };
  return p.exp > Date.now() ? p : null;
}

const DAY = 86400_000;
export const STUDENT_COOKIE = "remind_s";
export const MENTOR_COOKIE = "remind_m";
export const cookieOpts = (days: number) => ({
  httpOnly: true, sameSite: "lax" as const, secure: process.env.NODE_ENV === "production", path: "/", maxAge: days * 86400,
});

export const studentToken = (roll: string) => sign({ roll, exp: Date.now() + 60 * DAY });
export const mentorToken = () => sign({ mentor: true, exp: Date.now() + 7 * DAY });
export const getRoll = (req: NextRequest) => unsign<{ roll: string }>(req.cookies.get(STUDENT_COOKIE)?.value)?.roll ?? null;
export const isMentor = (req: NextRequest) => !!unsign<{ mentor: boolean }>(req.cookies.get(MENTOR_COOKIE)?.value)?.mentor;

export function checkMentorPasscode(p: string) {
  const want = process.env.MENTOR_PASSCODE || (process.env.NODE_ENV === "production" ? "" : "mentor");
  if (!want) return false;
  const a = crypto.createHash("sha256").update(p).digest();
  const b = crypto.createHash("sha256").update(want).digest();
  return crypto.timingSafeEqual(a, b);
}
