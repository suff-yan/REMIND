import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { getWeeks } from "@/lib/content";
import { SectionList, WeekBar } from "@/components/Progress";

export default function Home() {
  const weeks = getWeeks();
  const totalMin = weeks.flatMap((w) => w.sections).reduce((a, s) => a + s.minutes, 0);
  return (
    <div className="mx-auto grid max-w-[1200px] gap-12 px-6 pt-10 lg:grid-cols-[220px_1fr]">
      <aside className="hidden lg:block">
        <div className="sticky top-32">
          <p className="eyebrow mb-3">Contents</p>
          <ul className="grid gap-1 text-sm">
            {weeks.map((w) => (
              <li key={w.n}><a href={`#week-${w.n}`} className="flex gap-2 text-slate no-underline hover:text-ink"><span className="w-4 font-mono">{w.n}</span>{w.title}</a></li>
            ))}
            <li className="mt-3 border-t border-rule pt-3"><Link href="/midterm" className="text-slate no-underline hover:text-ink">Mid-term brief</Link></li>
            <li><Link href="/endterm" className="text-slate no-underline hover:text-ink">End-term brief</Link></li>
            <li><Link href="/cup" className="text-slate no-underline hover:text-ink">Re-Mind Cup</Link></li>
          </ul>
        </div>
      </aside>

      <div>
        <p className="eyebrow">Syllabus · Winter in Data Science 6.0 · Analytics Club, IIT Bombay</p>
        <h1 className="mt-2 max-w-[22ch] font-serif text-[2.6rem] font-semibold leading-[1.1] tracking-tight">Re-Mind: an agentic AI tutor that learns when you’ll forget</h1>
        <div className="mt-5 grid gap-8 md:grid-cols-[1fr_260px]">
          <p className="max-w-[62ch] text-[17px] text-slate">
            Six weeks, from your first line of Python to a working study companion that answers questions, decides on its own when to test you,
            and uses reinforcement learning to get better at that decision. No prior ML or RL is assumed. Every section has an animation,
            a self-check quiz and code you can run right here in the browser.
          </p>
          <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 self-start border-l border-rule pl-4 text-sm">
            <dt className="text-slate">Length</dt><dd className="font-mono">{weeks.length} weeks</dd>
            <dt className="text-slate">Effort</dt><dd className="font-mono">~7 h / week</dd>
            <dt className="text-slate">Reading</dt><dd className="font-mono">{Math.round(totalMin / 60)} h guided</dd>
            <dt className="text-slate">Mentors</dt><dd>M. Sufiyan, A. Gupta</dd>
          </dl>
        </div>

        <ol className="mt-14 border-t border-ink">
          {weeks.map((w) => (
            <li key={w.n} id={`week-${w.n}`} className="grid scroll-mt-32 gap-6 border-b border-rule py-8 md:grid-cols-[140px_1fr_1fr]">
              <div>
                <p className="font-mono text-xs text-slate">Week {w.n}</p>
                <p className="mt-1 font-mono text-xs text-slate">{w.hours} h</p>
                <div className="mt-3"><WeekBar ids={w.sections.map((s) => s.id)} /></div>
              </div>
              <div>
                <p className="eyebrow text-amber">{w.kicker}</p>
                <h2 className="mt-1 font-serif text-2xl font-semibold leading-snug">
                  <Link href={`/week/${w.n}`} className="text-ink no-underline hover:text-cobalt">{w.title}</Link>
                </h2>
                <p className="mt-2 text-[15px] text-slate">{w.summary}</p>
                <p className="mt-3 text-sm"><span className="text-slate">Deliverable · </span>{w.deliverable}</p>
                {w.sections[0] && (
                  <Link href={`/week/${w.n}/${w.sections[0].slug}`} className="mt-4 inline-flex items-center gap-1 text-sm no-underline">
                    Start week {w.n} <ArrowRight size={14} strokeWidth={1.5} />
                  </Link>
                )}
              </div>
              <SectionList sections={w.sections.map((s) => ({ id: s.id, title: s.title, href: `/week/${w.n}/${s.slug}` }))} />
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
