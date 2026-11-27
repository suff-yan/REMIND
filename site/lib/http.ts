import { NextResponse } from "next/server";
import { unstable_rethrow } from "next/navigation";
export const ok = (data: object = {}) => NextResponse.json({ ok: true, ...data });
export const bad = (error: string, status = 400) => NextResponse.json({ ok: false, error }, { status });
export async function body<T = Record<string, unknown>>(req: Request): Promise<T> {
  try { return (await req.json()) as T; } catch { return {} as T; }
}
export function guard(fn: (...a: any[]) => Promise<Response>) {
  return async (...a: any[]) => {
    try { return await fn(...a); }
    catch (e) { unstable_rethrow(e); console.error(e); return bad("Something went wrong on our side. Try again in a minute.", 500); }
  };
}
