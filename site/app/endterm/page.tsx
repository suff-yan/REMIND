import fs from "node:fs";
import path from "node:path";
import { Markdown } from "@/components/Markdown";
import { SubmitForm } from "@/components/SubmitForm";

export const metadata = { title: "End-term" };

export default function Page() {
  const md = fs.readFileSync(path.join(process.cwd(), "content", "assessments", "ENDTERM.md"), "utf8").replace(/^# .+\n/, "");
  const title = fs.readFileSync(path.join(process.cwd(), "content", "assessments", "ENDTERM.md"), "utf8").match(/^# (.+)$/m)?.[1] ?? "End-term";
  return (
    <div className="mx-auto grid max-w-[1200px] gap-12 px-6 pt-10 lg:grid-cols-[1fr_340px]">
      <article className="min-w-0">
        <p className="eyebrow">Assessment · End-term</p>
        <h1 className="mt-2 font-serif text-4xl font-semibold tracking-tight">{title.replace(/^End-term — /, "")}</h1>
        <div className="mt-8"><Markdown>{md}</Markdown></div>
      </article>
      <aside><div className="sticky top-32"><SubmitForm kind="endterm" /></div></aside>
    </div>
  );
}
