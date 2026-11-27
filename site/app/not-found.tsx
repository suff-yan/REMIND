import Link from "next/link";
export default function NotFound() {
  return <div className="mx-auto max-w-[760px] px-6 pt-16"><h1 className="font-serif text-3xl font-semibold">Page not found</h1><p className="mt-3 text-slate">Back to the <Link href="/">syllabus</Link>.</p></div>;
}
