import fs from "node:fs";
import path from "node:path";
import { Markdown } from "@/components/Markdown";
import { SubmitForm } from "@/components/SubmitForm";

export const metadata = { title: "Mid-term" };

export default function Page() {
  const md = fs.readFileSync(path.join(process.cwd(), "content", "assessments", "MIDTERM.md"), "utf8").replace(/^# .+\n/, "");
  const title = fs.readFileSync(path.join(process.cwd(), "content", "assessments", "MIDTERM.md"), "utf8").match(/^# (.+)$/m)?.[1] ?? "Mid-term";
  return (
    <div className="mx-auto grid max-w-[1200px] gap-12 px-6 pt-10 lg:grid-cols-[1fr_340px]">
      <article className="min-w-0">
        <p className="eyebrow">Assessment · Mid-term</p>
        <h1 className="mt-2 font-serif text-4xl font-semibold tracking-tight">{title.replace(/^Mid-term — /, "")}</h1>
        <div className="mt-8"><Markdown>{md}</Markdown></div>
      </article>
      <aside><div className="sticky top-32"><SubmitForm kind="midterm" /></div></aside>
    </div>
  );
}
