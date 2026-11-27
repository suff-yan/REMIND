import fs from "node:fs";
import path from "node:path";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight, ExternalLink } from "lucide-react";
import { getSection, getWeeks } from "@/lib/content";
import { Markdown, headings } from "@/components/Markdown";
import { Video } from "@/components/Video";
import { Quiz } from "@/components/Quiz";
import { Checkpoint } from "@/components/Checkpoint";
import { MarkComplete, SectionList } from "@/components/Progress";

export function generateStaticParams() {
  return getWeeks().flatMap((w) => w.sections.map((s) => ({ w: String(w.n), slug: s.slug })));
}
export async function generateMetadata({ params }: { params: Promise<{ w: string; slug: string }> }) {
  const p = await params; const r = getSection(Number(p.w), p.slug);
  return { title: r ? r.section.title : "Section" };
}

export default async function SectionPage({ params }: { params: Promise<{ w: string; slug: string }> }) {
  const p = await params;
  const r = getSection(Number(p.w), p.slug);
  if (!r) notFound();
  const { week, section: s, prev, next } = r;
  const toc = headings(s.body);
  const hasVideo = !!s.video && fs.existsSync(path.join(process.cwd(), "public", "videos", `${s.video}.mp4`));
  const href = (x: { week: number; slug: string }) => `/week/${x.week}/${x.slug}`;
  return (
    <div className="mx-auto grid max-w-[1200px] gap-12 px-6 pt-8 lg:grid-cols-[240px_1fr]">
      <aside className="hidden lg:block">
        <div className="sticky top-32 max-h-[calc(100vh-9rem)] overflow-y-auto pb-8">
          <p className="eyebrow mb-2"><Link href={`/week/${week.n}`} className="text-slate no-underline">Week {week.n} · {week.title}</Link></p>
          <SectionList current={s.id} sections={week.sections.map((x) => ({ id: x.id, title: x.title, href: href(x) }))} />
          {toc.length > 1 && (
            <>
              <p className="eyebrow mb-2 mt-6">On this page</p>
              <ul className="grid gap-1 border-l border-rule pl-3 text-[13px]">
                {toc.map((h) => <li key={h.id}><a href={`#${h.id}`} className="text-slate no-underline hover:text-ink">{h.title}</a></li>)}
                {s.video && <li><a href="#animation" className="text-slate no-underline hover:text-ink">Animation</a></li>}
                {s.checkpoint && <li><a href="#checkpoint" className="text-slate no-underline hover:text-ink">Checkpoint</a></li>}
                {s.quiz.length > 0 && <li><a href="#quiz" className="text-slate no-underline hover:text-ink">Self-check</a></li>}
              </ul>
            </>
          )}
        </div>
      </aside>

      <article className="min-w-0 max-w-[760px]">
        <p className="eyebrow"><Link href="/" className="text-slate no-underline">Syllabus</Link> / <Link href={`/week/${week.n}`} className="text-slate no-underline">Week {week.n}</Link> / {s.order}</p>
        <h1 className="mt-3 font-serif text-[2.3rem] font-semibold leading-tight tracking-tight">{s.title}</h1>
        <p className="mt-2 font-mono text-xs text-slate">{s.minutes} min{s.video ? " · animation" : ""}{s.checkpoint ? " · checkpoint" : ""}{s.quiz.length ? ` · ${s.quiz.length}-question self-check` : ""}</p>
        <div className="mt-8"><Markdown>{s.body}</Markdown></div>
        {s.video && <div id="animation" className="scroll-mt-32"><Video sectionId={s.id} src={s.video} title={s.videoTitle ?? s.title} hasFile={hasVideo} /></div>}
        {s.checkpoint && <div id="checkpoint" className="scroll-mt-32"><Checkpoint sectionId={s.id} cp={s.checkpoint} /></div>}
        {s.quiz.length > 0 && <div id="quiz" className="scroll-mt-32"><Quiz sectionId={s.id} questions={s.quiz} /></div>}
        {s.resources.length > 0 && (
          <section className="my-10">
            <h2 className="font-serif text-xl font-semibold">Go further</h2>
            <ul className="mt-3 divide-y divide-rule border-y border-rule">
              {s.resources.map((x) => (
                <li key={x.url} className="flex items-baseline gap-3 py-2 text-[15px]">
                  <ExternalLink size={13} strokeWidth={1.5} className="shrink-0 translate-y-0.5 text-slate" />
                  <a href={x.url} target="_blank" rel="noreferrer">{x.label}</a>
                  {x.note && <span className="text-sm text-slate">{x.note}</span>}
                </li>
              ))}
            </ul>
          </section>
        )}
        <div className="mt-10 flex flex-wrap items-center gap-3 border-t border-rule pt-6">
          <MarkComplete id={s.id} />
          <span className="ml-auto flex gap-4 text-sm">
            {prev && <Link href={href(prev)} className="inline-flex items-center gap-1 no-underline"><ArrowLeft size={14} strokeWidth={1.5} /> {prev.title}</Link>}
            {next && <Link href={href(next)} className="inline-flex items-center gap-1 no-underline">{next.title} <ArrowRight size={14} strokeWidth={1.5} /></Link>}
          </span>
        </div>
      </article>
    </div>
  );
}
