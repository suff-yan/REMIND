import { db } from "@/lib/store";
import { allSectionIds } from "@/lib/content";

export async function roster() {
  const [students, progress, subs, cup] = await Promise.all([db.listStudents(), db.getProgress(), db.getSubmissions(), db.getCup()]);
  const sections = allSectionIds();
  const total = sections.length;
  const weekOf = new Map(sections.map((s) => [s.id, s.week]));
  return students.map((s) => {
    const mine = progress.filter((p) => p.roll === s.roll);
    const done = mine.filter((p) => p.completed || p.quiz_passed);
    const quizzes = mine.filter((p) => p.quiz_score !== null);
    const acc = quizzes.length ? Math.round(quizzes.reduce((a, p) => a + (p.quiz_score ?? 0), 0) / quizzes.length) : null;
    const week = mine.length ? Math.max(...mine.map((p) => weekOf.get(p.section_id) ?? 0)) : 0;
    const c = cup.find((x) => x.roll === s.roll);
    const sub = (k: string) => subs.find((x) => x.roll === s.roll && x.kind === k) ?? null;
    const daysIdle = s.last_active ? Math.floor((Date.now() - +new Date(s.last_active)) / 86400000) : null;
    return {
      roll: s.roll, name: s.name, current_week: week, sections_done: done.length, sections_total: total,
      quiz_accuracy: acc, videos_watched: mine.filter((p) => p.video_watched).length,
      code_done: mine.filter((p) => p.code_completed).length,
      last_active: s.last_active, days_idle: daysIdle, locked: !!(s.locked_until && new Date(s.locked_until) > new Date()),
      midterm: sub("midterm"), endterm: sub("endterm"), cup_score: c?.score ?? null,
    };
  });
}
