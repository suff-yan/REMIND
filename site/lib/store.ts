/**
 * Data layer. Uses Supabase (service role, server-only) when SUPABASE_URL is set,
 * otherwise a local JSON file (.data/dev-db.json) so the site runs with zero setup.
 */
import fs from "node:fs";
import path from "node:path";
import { createClient, SupabaseClient } from "@supabase/supabase-js";

export type Student = {
  roll: string; name: string; pin_hash: string;
  failed_attempts: number; locked_until: string | null;
  created_at: string; last_active: string | null;
};
export type Progress = {
  roll: string; section_id: string; video_watched: boolean; quiz_score: number | null;
  quiz_passed: boolean; code_completed: boolean; completed: boolean; updated_at: string;
};
export type Submission = { roll: string; kind: "midterm" | "endterm"; repo_url: string; video_url: string | null; report_url: string | null; submitted_at: string };
export type CupEntry = { roll: string; entry: unknown; uploaded_at: string; score: number | null; retention: number | null; reviews: number | null; exam_pass: number | null; error: string | null; evaluated_at: string | null };
export type PinReset = { roll: string; code_hash: string; expires_at: string };
type Tables = { students: Student[]; progress: Progress[]; submissions: Submission[]; cup_entries: CupEntry[]; allowlist: { roll: string; name: string | null }[]; pin_resets: PinReset[] };

let sb: SupabaseClient | null = null;
function supa() {
  if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_ROLE_KEY) return null;
  sb ??= createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY, { auth: { persistSession: false } });
  return sb;
}

// ---------- local JSON fallback ----------
const FILE = path.join(process.cwd(), ".data", "dev-db.json");
function load(): Tables {
  try { return JSON.parse(fs.readFileSync(FILE, "utf8")); }
  catch { return { students: [], progress: [], submissions: [], cup_entries: [], allowlist: [], pin_resets: [] }; }
}
function save(t: Tables) { fs.mkdirSync(path.dirname(FILE), { recursive: true }); fs.writeFileSync(FILE, JSON.stringify(t, null, 1)); }

function check<T>(r: { data: T; error: { message: string } | null }): T {
  if (r.error) throw new Error(r.error.message);
  return r.data;
}

export const db = {
  usingSupabase: () => !!supa(),

  async getStudent(roll: string): Promise<Student | null> {
    const s = supa();
    if (s) return check(await s.from("students").select("*").eq("roll", roll).maybeSingle()) as Student | null;
    return load().students.find((x) => x.roll === roll) ?? null;
  },
  async createStudent(st: Student) {
    const s = supa();
    if (s) return void check(await s.from("students").insert(st));
    const t = load(); t.students.push(st); save(t);
  },
  async updateStudent(roll: string, patch: Partial<Student>) {
    const s = supa();
    if (s) return void check(await s.from("students").update(patch).eq("roll", roll));
    const t = load(); const x = t.students.find((y) => y.roll === roll); if (x) Object.assign(x, patch); save(t);
  },
  async listStudents(): Promise<Student[]> {
    const s = supa();
    if (s) return check(await s.from("students").select("*").order("roll")) as Student[];
    return load().students;
  },

  async isAllowed(roll: string): Promise<boolean> {
    if (process.env.ALLOWLIST_ENABLED !== "true") return true;
    const s = supa();
    if (s) return !!check(await s.from("allowlist").select("roll").eq("roll", roll).maybeSingle());
    return load().allowlist.some((a) => a.roll === roll);
  },
  async setAllowlist(rows: { roll: string; name: string | null }[]) {
    const s = supa();
    if (s) { check(await s.from("allowlist").delete().neq("roll", "")); if (rows.length) check(await s.from("allowlist").insert(rows)); return; }
    const t = load(); t.allowlist = rows; save(t);
  },
  async getAllowlist() {
    const s = supa();
    if (s) return check(await s.from("allowlist").select("*").order("roll")) as { roll: string; name: string | null }[];
    return load().allowlist;
  },

  async getProgress(roll?: string): Promise<Progress[]> {
    const s = supa();
    if (s) { let q = s.from("progress").select("*"); if (roll) q = q.eq("roll", roll); return check(await q) as Progress[]; }
    return load().progress.filter((p) => !roll || p.roll === roll);
  },
  async upsertProgress(p: Progress) {
    const s = supa();
    if (s) return void check(await s.from("progress").upsert(p, { onConflict: "roll,section_id" }));
    const t = load(); const i = t.progress.findIndex((x) => x.roll === p.roll && x.section_id === p.section_id);
    if (i >= 0) t.progress[i] = p; else t.progress.push(p); save(t);
  },

  async getSubmissions(roll?: string): Promise<Submission[]> {
    const s = supa();
    if (s) { let q = s.from("submissions").select("*"); if (roll) q = q.eq("roll", roll); return check(await q) as Submission[]; }
    return load().submissions.filter((x) => !roll || x.roll === roll);
  },
  async upsertSubmission(x: Submission) {
    const s = supa();
    if (s) return void check(await s.from("submissions").upsert(x, { onConflict: "roll,kind" }));
    const t = load(); const i = t.submissions.findIndex((y) => y.roll === x.roll && y.kind === x.kind);
    if (i >= 0) t.submissions[i] = x; else t.submissions.push(x); save(t);
  },

  async getCup(): Promise<CupEntry[]> {
    const s = supa();
    if (s) return check(await s.from("cup_entries").select("*")) as CupEntry[];
    return load().cup_entries;
  },
  async upsertCup(roll: string, entry: unknown) {
    const row = { roll, entry, uploaded_at: new Date().toISOString(), score: null, retention: null, reviews: null, exam_pass: null, error: null, evaluated_at: null };
    const s = supa();
    if (s) return void check(await s.from("cup_entries").upsert(row, { onConflict: "roll" }));
    const t = load(); t.cup_entries = t.cup_entries.filter((c) => c.roll !== roll); t.cup_entries.push(row); save(t);
  },

  async setPinReset(r: PinReset) {
    const s = supa();
    if (s) return void check(await s.from("pin_resets").upsert(r, { onConflict: "roll" }));
    const t = load(); t.pin_resets = t.pin_resets.filter((x) => x.roll !== r.roll); t.pin_resets.push(r); save(t);
  },
  async takePinReset(roll: string): Promise<PinReset | null> {
    const s = supa();
    if (s) {
      const r = check(await s.from("pin_resets").select("*").eq("roll", roll).maybeSingle()) as PinReset | null;
      if (r) check(await s.from("pin_resets").delete().eq("roll", roll));
      return r;
    }
    const t = load(); const r = t.pin_resets.find((x) => x.roll === roll) ?? null;
    t.pin_resets = t.pin_resets.filter((x) => x.roll !== roll); save(t); return r;
  },
};
