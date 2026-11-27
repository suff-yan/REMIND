"use client";
import Link from "next/link";
import { Check, Circle, CircleDot } from "lucide-react";
import { useSession } from "./Session";

type S = { id: string; title: string; href: string };

export function Tick({ id }: { id: string }) {
  const { progress } = useSession();
  const p = progress[id];
  if (p?.completed || p?.quiz_passed) return <Check size={14} strokeWidth={1.5} className="shrink-0 text-cobalt" aria-label="done" />;
  if (p) return <CircleDot size={12} strokeWidth={1.5} className="shrink-0 text-amber" aria-label="started" />;
  return <Circle size={12} strokeWidth={1.5} className="shrink-0 text-rule" aria-label="not started" />;
}

export function WeekBar({ ids }: { ids: string[] }) {
  const { progress, user } = useSession();
  if (!user) return null;
  const done = ids.filter((id) => progress[id]?.completed || progress[id]?.quiz_passed).length;
  return (
    <span className="flex items-center gap-2 font-mono text-xs text-slate">
      {done}/{ids.length}<span className="bar w-16"><span style={{ width: `${(100 * done) / ids.length}%` }} /></span>
    </span>
  );
}

export function SectionList({ sections, current }: { sections: S[]; current?: string }) {
  return (
    <ul className="grid gap-0.5">
      {sections.map((s) => (
        <li key={s.id}>
          <Link href={s.href} className={`flex items-center gap-2 rounded px-2 py-1 text-[13.5px] no-underline ${current === s.id ? "bg-white text-ink shadow-[inset_2px_0_0_var(--color-cobalt)]" : "text-slate hover:text-ink"}`}>
            <Tick id={s.id} /> <span>{s.title}</span>
          </Link>
        </li>
      ))}
    </ul>
  );
}

export function MarkComplete({ id }: { id: string }) {
  const { progress, save } = useSession();
  const done = progress[id]?.completed;
  return (
    <button className={`btn ${done ? "" : "btn-primary"}`} disabled={done} onClick={() => save(id, { completed: true })}>
      <Check size={14} strokeWidth={1.5} /> {done ? "Section complete" : "Mark section complete"}
    </button>
  );
}
