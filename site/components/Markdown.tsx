import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";

const slug = (s: string) => s.toLowerCase().replace(/[^\w]+/g, "-").replace(/(^-|-$)/g, "");
const text = (c: React.ReactNode): string => Array.isArray(c) ? c.map(text).join("") : typeof c === "string" ? c : "";

export function Markdown({ children }: { children: string }) {
  return (
    <div className="prose">
      <ReactMarkdown remarkPlugins={[remarkGfm, remarkMath]} rehypePlugins={[rehypeKatex, [rehypeHighlight, { detect: false }]]}
        components={{
          h2: ({ children }) => <h2 id={slug(text(children))}>{children}</h2>,
          a: ({ href, children }) => <a href={href} {...(href?.startsWith("http") ? { target: "_blank", rel: "noreferrer" } : {})}>{children}</a>,
        }}>
        {children}
      </ReactMarkdown>
    </div>
  );
}
export const headings = (md: string) =>
  [...md.matchAll(/^## (.+)$/gm)].map((m) => ({ title: m[1].replace(/[`*_]/g, ""), id: slug(m[1].replace(/[`*_]/g, "")) }));
