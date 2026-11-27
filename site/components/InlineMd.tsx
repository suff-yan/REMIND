"use client";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

/** One line of markdown with inline maths and `code`, rendered without a wrapping <p>. */
export function InlineMd({ children }: { children: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}
      components={{
        p: ({ children }) => <>{children}</>,
        code: ({ children }) => <code className="rounded border border-rule bg-stone px-1 font-mono text-[0.86em]">{children}</code>,
      }}>
      {children}
    </ReactMarkdown>
  );
}
