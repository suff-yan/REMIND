import { STUDENT_COOKIE } from "@/lib/auth";
import { ok } from "@/lib/http";
export async function POST() {
  const res = ok();
  res.cookies.delete(STUDENT_COOKIE);
  return res;
}
