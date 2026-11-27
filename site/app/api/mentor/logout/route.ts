import { MENTOR_COOKIE } from "@/lib/auth";
import { ok } from "@/lib/http";
export async function POST() { const r = ok(); r.cookies.delete(MENTOR_COOKIE); return r; }
