"use client";
import { useEffect, useRef, useState } from "react";
import { CheckSquare, Play, RotateCcw, Square, TerminalSquare } from "lucide-react";
import { useSession } from "./Session";
import type { Checkpoint as CP } from "@/lib/content";

declare global { interface Window { loadPyodide?: (o: object) => Promise<any>; __pyo?: Promise<any> } }

function getPyodide(withModules: boolean) {
  if (!window.__pyo) {
    window.__pyo = new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = "/pyodide/pyodide.js";
      s.onload = async () => {
        try {
          const py = await window.loadPyodide!({ indexURL: "/pyodide/" });
          const files: string[] = await fetch("/py/manifest.json").then((r) => r.json());
          for (const f of files) {
            const txt = await fetch(`/py/${f}`).then((r) => r.text());
            py.FS.mkdirTree("/home/pyodide/" + f.split("/").slice(0, -1).join("/"));
            py.FS.writeFile("/home/pyodide/" + f, txt);
          }
          py.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
          resolve(py);
        } catch (e) { reject(e); }
      };
      s.onerror = () => reject(new Error("Could not load the Python runtime"));
      document.head.appendChild(s);
    });
  }
  void withModules;
  return window.__pyo;
}

export function Checkpoint({ sectionId, cp }: { sectionId: string; cp: CP }) {
  const { save, progress } = useSession();
  const done = progress[sectionId]?.code_completed;
  return (
    <section className="my-12 rounded-md border border-rule bg-white" aria-label="Code checkpoint">
      <header className="flex items-center gap-2 border-b border-rule px-5 py-3">
        <TerminalSquare size={18} strokeWidth={1.5} className="text-cobalt" />
        <h2 className="font-serif text-xl font-semibold">{cp.title}</h2>
        <span className="ml-auto font-mono text-xs text-slate">{cp.kind === "browser" ? "runs in your browser" : "on your laptop"}{done ? " · completed" : ""}</span>
      </header>
      {cp.prompt && <p className="px-5 pt-4 text-[15px] text-slate">{cp.prompt}</p>}
      {cp.kind === "browser" ? <Runner sectionId={sectionId} cp={cp} onPass={() => save(sectionId, { code_completed: true })} />
        : <Steps sectionId={sectionId} steps={cp.steps ?? []} done={!!done} onDone={() => save(sectionId, { code_completed: true })} />}
    </section>
  );
}

function Runner({ sectionId, cp, onPass }: { sectionId: string; cp: CP; onPass: () => Promise<string | null> }) {
  const key = `remind-code-${sectionId}`;
  const [code, setCode] = useState(cp.starter ?? "");
  const [out, setOut] = useState<string>("");
  const [state, setState] = useState<"idle" | "loading" | "running" | "pass" | "fail">("idle");
  const [note, setNote] = useState<string | null>(null);
  const ta = useRef<HTMLTextAreaElement>(null);
  useEffect(() => { const s = localStorage.getItem(key); if (s) setCode(s); }, [key]);
  useEffect(() => { localStorage.setItem(key, code); }, [key, code]);

  async function run(withTests: boolean) {
    setOut(""); setState("loading");
    let buf = "";
    try {
      const py = await getPyodide(!!cp.modules);
      setState("running");
      py.setStdout({ batched: (s: string) => { buf += s + "\n"; setOut(buf); } });
      py.setStderr({ batched: (s: string) => { buf += s + "\n"; setOut(buf); } });
      const ns = py.globals.get("dict")();
      await py.runPythonAsync(code, { globals: ns });
      if (withTests && cp.tests) {
        await py.runPythonAsync(cp.tests, { globals: ns });
        buf += "\n✓ All checks passed.\n"; setOut(buf); setState("pass");
        setNote(await onPass());
      } else setState("idle");
    } catch (e: any) {
      const msg = String(e?.message ?? e);
      const tail = msg.split("\n").filter(Boolean).slice(-6).join("\n");
      buf += "\n" + tail + "\n"; setOut(buf); setState("fail");
    }
  }
  return (
    <div className="px-5 py-4">
      <textarea ref={ta} value={code} onChange={(e) => setCode(e.target.value)} spellCheck={false} aria-label="Python code editor"
        onKeyDown={(e) => {
          if (e.key === "Tab") {
            e.preventDefault();
            const t = e.currentTarget, s = t.selectionStart, en = t.selectionEnd;
            const v = code.slice(0, s) + "    " + code.slice(en); setCode(v);
            requestAnimationFrame(() => { t.selectionStart = t.selectionEnd = s + 4; });
          }
        }}
        className="block min-h-[260px] w-full resize-y rounded border border-charcoal bg-charcoal p-4 font-mono text-[13.5px] leading-relaxed text-[#E6E6E1] outline-none focus:border-cobalt"
        style={{ height: `${Math.min(34, Math.max(12, code.split("\n").length + 2)) * 1.6}rem` }} />
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <button className="btn" onClick={() => run(false)} disabled={state === "loading" || state === "running"}><Play size={14} strokeWidth={1.5} /> Run</button>
        <button className="btn btn-primary" onClick={() => run(true)} disabled={state === "loading" || state === "running"}><CheckSquare size={14} strokeWidth={1.5} /> Run checks</button>
        <button className="btn" onClick={() => { setCode(cp.starter ?? ""); setOut(""); setState("idle"); }}><RotateCcw size={14} strokeWidth={1.5} /> Reset code</button>
        <span className="ml-auto font-mono text-xs text-slate">
          {state === "loading" ? "starting Python (first run takes ~5 s)…" : state === "running" ? "running…" : state === "pass" ? "passed" : state === "fail" ? "not yet" : ""}
        </span>
      </div>
      {out && <pre className={`mt-3 max-h-80 overflow-auto rounded border p-3 font-mono text-[12.5px] leading-relaxed ${state === "fail" ? "border-amber bg-[#FDF3E6]" : state === "pass" ? "border-[#2F7D4F] bg-[#EDF6F0]" : "border-rule bg-stone"}`}>{out}</pre>}
      {note && <p className="mt-2 text-xs text-slate">{note}</p>}
    </div>
  );
}

function Steps({ sectionId, steps, done, onDone }: { sectionId: string; steps: string[]; done: boolean; onDone: () => Promise<string | null> }) {
  const key = `remind-steps-${sectionId}`;
  const [ticks, setTicks] = useState<boolean[]>(steps.map(() => false));
  const [note, setNote] = useState<string | null>(null);
  useEffect(() => { const s = localStorage.getItem(key); if (s) setTicks(JSON.parse(s)); }, [key]);
  const toggle = (i: number) => { const t = ticks.map((v, j) => (j === i ? !v : v)); setTicks(t); localStorage.setItem(key, JSON.stringify(t)); };
  return (
    <div className="px-5 py-4">
      <ol className="grid gap-2">
        {steps.map((s, i) => (
          <li key={i}>
            <button type="button" onClick={() => toggle(i)} className="flex w-full items-start gap-3 rounded px-1 py-1 text-left hover:bg-stone">
              {ticks[i] ? <CheckSquare size={18} strokeWidth={1.5} className="mt-0.5 shrink-0 text-cobalt" /> : <Square size={18} strokeWidth={1.5} className="mt-0.5 shrink-0 text-slate" />}
              <span className="text-[15px]" dangerouslySetInnerHTML={{ __html: s.replace(/`([^`]+)`/g, '<code class="font-mono text-[13px] bg-stone border border-rule px-1 rounded">$1</code>') }} />
            </button>
          </li>
        ))}
      </ol>
      <div className="mt-3 flex items-center gap-3">
        <button className="btn btn-primary" disabled={done || ticks.some((t) => !t)} onClick={async () => setNote(await onDone())}>
          {done ? "Checkpoint completed" : "I’ve done all of these"}
        </button>
        {note && <span className="text-xs text-slate">{note}</span>}
      </div>
    </div>
  );
}
