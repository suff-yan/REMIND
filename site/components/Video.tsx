"use client";
import { useRef } from "react";
import { useSession } from "./Session";

export function Video({ sectionId, src, title, hasFile }: { sectionId: string; src: string; title: string; hasFile: boolean }) {
  const { save, progress } = useSession();
  const sent = useRef(false);
  const watched = progress[sectionId]?.video_watched;
  if (!hasFile)
    return (
      <figure className="panel my-8 flex aspect-video items-center justify-center text-sm text-slate">
        Animation “{title}” is being rendered and will appear here.
      </figure>
    );
  return (
    <figure className="my-8">
      <video className="w-full rounded-md border border-rule bg-charcoal" controls preload="metadata" playsInline
        onTimeUpdate={(e) => {
          const v = e.currentTarget;
          if (!sent.current && v.duration && v.currentTime / v.duration > 0.8) { sent.current = true; save(sectionId, { video_watched: true }); }
        }}>
        <source src={`/videos/${src}.mp4`} type="video/mp4" />
        <track kind="subtitles" src={`/videos/${src}.vtt`} srcLang="en" label="English" default />
      </video>
      <figcaption className="mt-2 flex justify-between text-xs text-slate">
        <span>Animation · {title}</span>
        <span className="font-mono">{watched ? "watched" : "counts as watched at 80%"}</span>
      </figcaption>
    </figure>
  );
}
