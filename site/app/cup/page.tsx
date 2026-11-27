import { CupBoard } from "./CupBoard";
export const metadata = { title: "Re-Mind Cup" };
export default function Page() {
  return (
    <div className="mx-auto max-w-[1000px] px-6 pt-10">
      <p className="eyebrow">End-term · Part C</p>
      <h1 className="mt-2 font-serif text-4xl font-semibold tracking-tight">The Re-Mind Cup</h1>
      <div className="prose mt-6">
        <p>Train the best review scheduler you can, export it, and upload it here. Every night at 02:07 IST, all entries are scored on <strong>3,000 simulated students the public code has never seen</strong>.</p>
        <p className="font-mono">score = average recall (%) − reviews per concept</p>
        <p>For reference, on the public seed: Leitner boxes ≈ 84, the course RL agent ≈ 85, reviewing every day ≈ 40. Both reward hacks from Week 4 score badly by design. Check locally with <code>python cup/evaluate.py my_entry.json</code>.</p>
        <p>Entry file: <code>{`{"q": [[6 numbers] × 18]}`}</code> (a Q-table) or <code>{`{"policy": [18 actions 0–5]}`}</code>. State index = streak × 3 + last grade.</p>
      </div>
      <CupBoard />
    </div>
  );
}
