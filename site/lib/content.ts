import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

export type QuizQ = { q: string; options: string[]; answer: number; explain: string };
export type Checkpoint = {
  kind: "browser" | "local";
  title: string;
  prompt?: string;
  starter?: string;
  tests?: string;
  modules?: boolean; // load the remind package into Pyodide
  steps?: string[];
};
export type Resource = { label: string; url: string; note?: string };
export type Section = {
  id: string; // e.g. "3-bandits"
  week: number;
  slug: string;
  order: number;
  title: string;
  minutes: number;
  video?: string;
  videoTitle?: string;
  checkpoint?: Checkpoint;
  quiz: QuizQ[];
  resources: Resource[];
  body: string;
};
export type Week = {
  n: number;
  title: string;
  kicker: string;
  summary: string;
  hours: number;
  deliverable: string;
  slides?: string;
  sections: Section[];
};

const ROOT = path.join(process.cwd(), "content");
let cache: Week[] | null = null;

export function getWeeks(): Week[] {
  if (cache) return cache;
  const meta = JSON.parse(fs.readFileSync(path.join(ROOT, "weeks.json"), "utf8")) as Omit<Week, "sections">[];
  cache = meta.map((w) => {
    const dir = path.join(ROOT, `w${w.n}`);
    const files = fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => f.endsWith(".md")).sort() : [];
    const sections = files.map((f) => {
      const { data, content } = matter(fs.readFileSync(path.join(dir, f), "utf8"));
      const m = f.match(/^(\d+)-(.+)\.md$/);
      if (!m) throw new Error(`bad section file name ${f}`);
      return {
        id: `${w.n}-${m[2]}`,
        week: w.n,
        slug: m[2],
        order: Number(m[1]),
        title: data.title,
        minutes: data.minutes ?? 20,
        video: data.video,
        videoTitle: data.videoTitle,
        checkpoint: data.checkpoint,
        quiz: data.quiz ?? [],
        resources: data.resources ?? [],
        body: content,
      } as Section;
    });
    return { ...w, sections };
  });
  return cache;
}

export function getWeek(n: number) {
  return getWeeks().find((w) => w.n === n);
}

export function getSection(n: number, slug: string) {
  const w = getWeek(n);
  const i = w?.sections.findIndex((s) => s.slug === slug) ?? -1;
  if (!w || i < 0) return null;
  const all = getWeeks().flatMap((x) => x.sections);
  const gi = all.findIndex((s) => s.id === w.sections[i].id);
  return { week: w, section: w.sections[i], prev: all[gi - 1] ?? null, next: all[gi + 1] ?? null };
}

export function allSectionIds() {
  return getWeeks().flatMap((w) => w.sections.map((s) => ({ id: s.id, week: w.n, title: s.title })));
}
