# Re-Mind course website

Next.js 16 · Tailwind 4 · Supabase · self-hosted Pyodide. Content lives in `content/` (one Markdown file per section:
prose below, quiz / checkpoint / links in the front matter), so mentors can edit without touching code.

## Run locally (no setup needed)
```bash
npm install
npm run dev            # http://localhost:3000, data goes to .data/dev-db.json
python3 scripts/check-content.py   # validates every quiz and checkpoint against mentor_solutions/
```
Mentor dashboard locally: `/mentor`, passcode `mentor` (dev only).

## Deploy on Vercel
1. Vercel → Add New → Project → import `suff-yan/REMIND`. **Root Directory: `site`.**
2. Environment variables (Settings → Environment Variables), then Deploy:

| Name | Value |
|---|---|
| `SUPABASE_URL` | `https://jbnhduvvqjndedwhjwtr.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase → Project Settings → API keys → secret / service_role |
| `SESSION_SECRET` | output of `openssl rand -hex 32` |
| `MENTOR_PASSCODE` | a long passphrase shared with mentors |
| `ALLOWLIST_ENABLED` | `false` now; `true` after uploading the selected roll numbers on `/mentor` |
| `SMTP_HOST` / `SMTP_PORT` | `smtp.gmail.com` / `465` |
| `SMTP_USER` / `SMTP_PASS` | `sufiyanstudies@gmail.com` / its 16-character app password |
| `MAIL_FROM` | `Re-Mind WiDS <sufiyanstudies@gmail.com>` |
| `MAIL_REPLY_TO` | `24b0935@iitb.ac.in` |

Without the Supabase variables the site still renders, but profiles cannot be saved on Vercel.

## Database
`supabase/schema.sql` — already applied to the project. Re-running it is safe.

## Editing content
- New section: add `content/w<N>/<order>-<slug>.md`. Front matter: `title`, `minutes`, optional `video`
  (file name in `public/videos/` without extension), `checkpoint`, `quiz`, `resources`.
- Browser checkpoints: put a reference solution in `../mentor_solutions/checkpoints/<week>-<slug>.py` and run
  `python3 scripts/check-content.py`; it must report the starter failing and the solution passing.
- Quiz option order is shuffled per question on the page, so write the correct answer anywhere.
