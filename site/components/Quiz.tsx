"use client";
import { useState } from "react";
import { Check, RotateCcw, X } from "lucide-react";
import { useSession } from "./Session";
import type { QuizQ } from "@/lib/content";
import { InlineMd } from "./InlineMd";

// Stable per-question shuffle so the correct answer isn't always in the same slot.
function shuffled(q: QuizQ): QuizQ {
  let h = 2166136261;
  for (const c of q.q) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  const idx = q.options.map((_, i) => i);
  for (let i = idx.length - 1; i > 0; i--) { h = Math.imul(h ^ (h >>> 13), 1274126177); const j = Math.abs(h) % (i + 1); [idx[i], idx[j]] = [idx[j], idx[i]]; }
  return { ...q, options: idx.map((i) => q.options[i]), answer: idx.indexOf(q.answer) };
}

export function Quiz({ sectionId, questions: raw }: { sectionId: string; questions: QuizQ[] }) {
  const questions = raw.map(shuffled);
  const { save, progress } = useSession();
  const [pick, setPick] = useState<(number | null)[]>(questions.map(() => null));
  const [done, setDone] = useState(false);
  const [note, setNote] = useState<string | null>(null);
  const best = progress[sectionId]?.quiz_score;
  const score = Math.round((100 * pick.filter((p, i) => p === questions[i].answer).length) / questions.length);

  async function submit() {
    setDone(true);
    setNote(await save(sectionId, { quiz_score: score }));
  }
  return (
    <section className="my-12 rounded-md border border-rule bg-white" aria-label="Self-check quiz">
      <header className="flex items-baseline justify-between border-b border-rule px-5 py-3">
        <h2 className="font-serif text-xl font-semibold">Self-check</h2>
        <span className="font-mono text-xs text-slate">{questions.length} questions · pass at 70%{best != null ? ` · best ${best}%` : ""}</span>
      </header>
      <ol className="divide-y divide-rule">
        {questions.map((q, i) => (
          <li key={i} className="px-5 py-4">
            <p className="mb-2 font-medium"><span className="mr-2 font-mono text-slate">{i + 1}.</span><InlineMd>{q.q}</InlineMd></p>
            <div className="grid gap-1.5">
              {q.options.map((o, j) => {
                const chosen = pick[i] === j, right = j === q.answer;
                const tone = !done ? (chosen ? "border-cobalt bg-[#EEF2FD]" : "border-rule hover:border-[#C9C6BA]")
                  : right ? "border-[#2F7D4F] bg-[#EDF6F0]" : chosen ? "border-amber bg-[#FDF3E6]" : "border-rule opacity-70";
                return (
                  <button key={j} type="button" disabled={done} onClick={() => setPick(pick.map((p, k) => (k === i ? j : p)))}
                    className={`flex items-start gap-2 rounded border px-3 py-2 text-left text-[15px] ${tone}`}>
                    <span className="mt-0.5 font-mono text-xs text-slate">{String.fromCharCode(65 + j)}</span>
                    <span className="flex-1"><InlineMd>{o}</InlineMd></span>
                    {done && right && <Check size={16} strokeWidth={1.5} className="mt-1 text-[#2F7D4F]" aria-label="correct answer" />}
                    {done && chosen && !right && <X size={16} strokeWidth={1.5} className="mt-1 text-amber" aria-label="your answer, incorrect" />}
                  </button>
                );
              })}
            </div>
            {done && <p className="mt-2 border-l-2 border-amber pl-3 text-sm text-slate"><InlineMd>{q.explain}</InlineMd></p>}
          </li>
        ))}
      </ol>
      <footer className="flex items-center gap-3 border-t border-rule px-5 py-3">
        {!done ? (
          <button className="btn btn-primary" disabled={pick.some((p) => p === null)} onClick={submit}>Check answers</button>
        ) : (
          <>
            <span className="font-mono text-sm">{score}%</span>
            <span className={`text-sm ${score >= 70 ? "text-[#2F7D4F]" : "text-amber"}`}>{score >= 70 ? "Passed" : "Not yet: re-read the flagged parts and retry"}</span>
            <button className="btn ml-auto" onClick={() => { setDone(false); setPick(questions.map(() => null)); setNote(null); }}><RotateCcw size={14} strokeWidth={1.5} /> Retry</button>
          </>
        )}
        {note && <span className="text-xs text-slate">{note}</span>}
      </footer>
    </section>
  );
}
