-- Re-Mind WiDS 6.0 — run once in Supabase → SQL Editor → New query → Run.
-- All access goes through the website's server with the service-role key.
-- Row Level Security is ON with no policies, so the public anon key can read/write nothing.

create table if not exists students (
  roll            text primary key check (roll ~ '^[0-9]{2}[A-Z][0-9]{4}$'),
  name            text not null,
  pin_hash        text not null,
  failed_attempts int  not null default 0,
  locked_until    timestamptz,
  created_at      timestamptz not null default now(),
  last_active     timestamptz
);

create table if not exists progress (
  roll           text not null references students(roll) on delete cascade,
  section_id     text not null,
  video_watched  boolean not null default false,
  quiz_score     int,
  quiz_passed    boolean not null default false,
  code_completed boolean not null default false,
  completed      boolean not null default false,
  updated_at     timestamptz not null default now(),
  primary key (roll, section_id)
);

create table if not exists submissions (
  roll         text not null references students(roll) on delete cascade,
  kind         text not null check (kind in ('midterm', 'endterm')),
  repo_url     text not null,
  video_url    text,
  report_url   text,
  submitted_at timestamptz not null default now(),
  primary key (roll, kind)
);

create table if not exists cup_entries (
  roll         text primary key references students(roll) on delete cascade,
  entry        jsonb not null,
  uploaded_at  timestamptz not null default now(),
  score        double precision,
  retention    double precision,
  reviews      double precision,
  exam_pass    double precision,
  error        text,
  evaluated_at timestamptz
);

create table if not exists allowlist (
  roll text primary key,
  name text
);

create table if not exists pin_resets (
  roll       text primary key references students(roll) on delete cascade,
  code_hash  text not null,
  expires_at timestamptz not null
);

alter table students    enable row level security;
alter table progress    enable row level security;
alter table submissions enable row level security;
alter table cup_entries enable row level security;
alter table allowlist   enable row level security;
alter table pin_resets  enable row level security;

create index if not exists progress_roll_idx on progress(roll);
