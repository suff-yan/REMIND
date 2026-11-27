import type { NextRequest } from "next/server";
import { isMentor } from "@/lib/auth";
import { bad, guard, ok } from "@/lib/http";
import { roster } from "@/lib/roster";
import { db } from "@/lib/store";
export const GET = guard(async (req: NextRequest) => {
  if (!isMentor(req)) return bad("Mentor login required.", 401);
  return ok({ rows: await roster(), storage: db.usingSupabase() ? "supabase" : "local-file",
    allowlist_enabled: process.env.ALLOWLIST_ENABLED === "true", allowlist_count: (await db.getAllowlist()).length });
});
