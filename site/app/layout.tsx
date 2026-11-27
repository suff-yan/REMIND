import type { Metadata } from "next";
import Link from "next/link";
import "@fontsource-variable/newsreader";
import "@fontsource-variable/inter";
import "@fontsource-variable/jetbrains-mono";
import "./globals.css";
import { SessionProvider } from "@/components/Session";
import { AuthBar } from "@/components/AuthBar";
import { allSectionIds } from "@/lib/content";

export const metadata: Metadata = {
  title: { default: "Re-Mind · WiDS 6.0", template: "%s · Re-Mind" },
  description: "An agentic AI tutor that learns when you'll forget. A six-week Winter in Data Science project by the Analytics Club, IIT Bombay.",
};

const nav = [["/", "Syllabus"], ["/midterm", "Mid-term"], ["/endterm", "End-term"], ["/cup", "Cup"], ["/resources", "Resources"]];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <SessionProvider>
          <header className="sticky top-0 z-20 border-b border-rule bg-paper/95 backdrop-blur-[2px]">
            <div className="mx-auto flex h-14 max-w-[1200px] items-center gap-8 px-6">
              <Link href="/" className="flex items-baseline gap-2 text-ink no-underline">
                <span className="font-serif text-xl font-semibold tracking-tight">Re-Mind</span>
                <span className="font-mono text-[11px] text-slate">WiDS 6.0</span>
              </Link>
              <nav className="flex gap-5 text-sm">
                {nav.map(([href, label]) => <Link key={href} href={href} className="text-slate no-underline hover:text-ink">{label}</Link>)}
              </nav>
            </div>
          </header>
          <AuthBar totalSections={allSectionIds().length} />
          <main>{children}</main>
          <footer className="mt-24 border-t border-rule">
            <div className="mx-auto flex max-w-[1200px] flex-wrap gap-x-8 gap-y-1 px-6 py-6 text-xs text-slate">
              <span>Analytics Club, IIT Bombay · Winter in Data Science 6.0</span>
              <span>Mentors: Muhammed Sufiyan · Anshuman Gupta</span>
              <a href="https://github.com/suff-yan/REMIND">Course repository</a>
              <Link href="/mentor" className="ml-auto text-slate">Mentors</Link>
            </div>
          </footer>
        </SessionProvider>
      </body>
    </html>
  );
}
