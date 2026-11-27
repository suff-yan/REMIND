import Link from "next/link";
import { notFound } from "next/navigation";
import { getWeek, getWeeks } from "@/lib/content";
import { SectionList, WeekBar } from "@/components/Progress";

export function generateStaticParams() { return getWeeks().map((w) => ({ w: String(w.n) })); }

export async function generateMetadata({ params }: { params: Promise<{ w: string }> }) {
  const w = getWeek(Number((await params).w));
  return { title: w ? `Week ${w.n}: ${w.title}` : "Week" };
}

export default async function WeekPage({ params }: { params: Promise<{ w: string }> }) {
  const w = getWeek(Number((await params).w));
  if (!w) notFound();
  return (
    <div className="mx-auto max-w-[900px] px-6 pt-10">
      <p className="eyebrow"><Link href="/" className="text-slate no-underline">Syllabus</Link> / Week {w.n}</p>
      <p className="eyebrow mt-6 text-amber">{w.kicker}</p>
      <h1 className="mt-1 font-serif text-4xl font-semibold tracking-tight">Week {w.n} · {w.title}</h1>
      <p className="mt-4 max-w-[62ch] text-[17px] text-slate">{w.summary}</p>
      <div className="mt-6 flex flex-wrap items-center gap-6 border-y border-rule py-3 text-sm">
        <span><span className="text-slate">Effort </span><span className="font-mono">{w.hours} h</span></span>
        <span><span className="text-slate">Deliverable </span>{w.deliverable}</span>
        {w.slides && <a href={w.slides} target="_blank" rel="noreferrer">Meeting slides</a>}
        <span className="ml-auto"><WeekBar ids={w.sections.map((s) => s.id)} /></span>
      </div>
      <div className="mt-8">
        <SectionList sections={w.sections.map((s) => ({ id: s.id, title: `${s.title} · ${s.minutes} min`, href: `/week/${w.n}/${s.slug}` }))} />
      </div>
    </div>
  );
}
