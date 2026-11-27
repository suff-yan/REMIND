import fs from "node:fs";
import path from "node:path";
import { Markdown } from "@/components/Markdown";
export const metadata = { title: "Resources" };
export default function Page() {
  const md = fs.readFileSync(path.join(process.cwd(), "content", "resources.md"), "utf8");
  return (
    <div className="mx-auto max-w-[820px] px-6 pt-10">
      <p className="eyebrow">Reference</p>
      <h1 className="mt-2 font-serif text-4xl font-semibold tracking-tight">Resources, glossary and setup help</h1>
      <div className="mt-8"><Markdown>{md}</Markdown></div>
    </div>
  );
}
