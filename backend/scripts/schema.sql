-- ============================================
-- DHARMA APP — SUPABASE SCHEMA
-- Run this entire file in the Supabase SQL Editor
-- ============================================

-- Enable pgvector extension
create extension if not exists vector;

-- ============================================
-- USERS TABLE
-- ============================================
create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text unique not null,
  password_hash text not null,
  is_verified boolean default false,
  verification_token text,
  reset_token text,
  created_at timestamptz default now()
);

-- ============================================
-- SUTTAS TABLE (vector store)
-- ============================================
create table if not exists suttas (
  id uuid primary key default gen_random_uuid(),
  reference text unique not null,
  title text not null,
  collection text not null,
  content text not null,
  embedding vector(384),  -- 384 dimensions for all-MiniLM-L6-v2
  created_at timestamptz default now()
);

-- Index for fast vector similarity search
create index if not exists suttas_embedding_idx
  on suttas
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 10);

-- ============================================
-- QUESTIONS TABLE (conversation history)
-- ============================================
create table if not exists questions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references users(id) on delete cascade not null,
  question text not null,
  answer text not null,
  sources jsonb default '[]',
  created_at timestamptz default now()
);

-- Index for fast user history lookup
create index if not exists questions_user_id_idx on questions(user_id);
create index if not exists questions_created_at_idx on questions(created_at desc);

-- ============================================
-- ROW LEVEL SECURITY
-- Users can only see their own questions
-- ============================================
alter table questions enable row level security;

create policy "Users can read own questions"
  on questions for select
  using (user_id = auth.uid());

create policy "Users can insert own questions"
  on questions for insert
  with check (user_id = auth.uid());

create policy "Users can delete own questions"
  on questions for delete
  using (user_id = auth.uid());

-- Suttas are public (anyone can read)
alter table suttas enable row level security;

create policy "Suttas are publicly readable"
  on suttas for select
  using (true);

-- Users table — only service role can write, users can read own row
alter table users enable row level security;

create policy "Users can read own profile"
  on users for select
  using (true);

-- ============================================
-- MATCH SUTTAS FUNCTION
-- Called by the RAG pipeline to find relevant suttas
-- ============================================
create or replace function match_suttas(
  query_embedding vector(384),
  match_threshold float default 0.3,
  match_count int default 5
)
returns table (
  id uuid,
  reference text,
  title text,
  collection text,
  content text,
  similarity float
)
language sql stable
as $$
  select
    suttas.id,
    suttas.reference,
    suttas.title,
    suttas.collection,
    suttas.content,
    1 - (suttas.embedding <=> query_embedding) as similarity
  from suttas
  where 1 - (suttas.embedding <=> query_embedding) > match_threshold
  order by suttas.embedding <=> query_embedding
  limit match_count;
$$;