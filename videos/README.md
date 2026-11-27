# Re-Mind animations (Manim)

Nine short animations, one or two per week, in the website's palette and type.

| Scene | File on the site | Section |
|---|---|---|
| `W0Python` | `w0_python` | Week 0 · Python I |
| `W0Averages` | `w0_averages` | Week 0 · Maths I |
| `W1Request` | `w1_request` | Week 1 · APIs |
| `W2Agent` | `w2_agent` | Week 2 · Agents |
| `W3Bandit` | `w3_bandit` | Week 3 · Bandits |
| `W3QLearning` | `w3_qlearning` | Week 3 · Q-learning |
| `W4Forgetting` | `w4_forgetting` | Week 4 · Forgetting |
| `W4Scheduler` | `w4_scheduler` | Week 4 · Training |
| `W5System` | `w5_system` | Week 5 · Architecture |

## Render
```bash
pip install manim           # needs LaTeX + dvisvgm, and the fonts Inter, JetBrains Mono, Newsreader
manim -qh w3.py W3Bandit    # 1080p30, ~20 s per scene
```
Every `self.say(text, ...)` line is both the on-screen pacing and a subtitle cue: rendering writes
`captions/<Scene>.vtt`. **These captions are also the narration script**: to add a voiceover, record
each cue in its time window (the cue timings are in the .vtt), or re-time by editing `min_rate` in `style.py`.

## Export to the site
Re-encode to H.264 and copy with the caption file:
```bash
ffmpeg -i media/videos/w3/1080p30/W3Bandit.mp4 -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p -movflags +faststart -an ../site/public/videos/w3_bandit.mp4
cp captions/W3Bandit.vtt ../site/public/videos/w3_bandit.vtt
```
