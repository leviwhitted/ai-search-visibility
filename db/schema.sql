create table if not exists citation_runs (
  run_id text primary key,
  query_id text not null,
  query_group text not null,
  query_text text not null,
  engine text not null,
  model text,
  repetition integer not null,
  country text,
  region text,
  city text,
  language text,
  temperature numeric,
  captured_at timestamptz not null,
  mode text not null,
  raw_response jsonb not null
);

create table if not exists brand_mentions (
  run_id text not null references citation_runs(run_id),
  query_id text not null,
  query_group text not null,
  engine text not null,
  repetition integer not null,
  brand text not null,
  mentioned boolean not null,
  brand_order integer,
  mention_count integer not null default 0,
  primary key (run_id, brand)
);

create table if not exists citations (
  run_id text not null references citation_runs(run_id),
  query_id text not null,
  query_group text not null,
  engine text not null,
  repetition integer not null,
  url text not null,
  domain text not null,
  title text,
  cited_brand text,
  is_gatekeeper boolean not null default false,
  gatekeeper_domain text,
  citation_index integer not null,
  primary key (run_id, citation_index)
);

create table if not exists brand_absorptions (
  run_id text not null references citation_runs(run_id),
  query_id text not null,
  query_group text not null,
  engine text not null,
  repetition integer not null,
  brand text not null,
  absorbed boolean not null,
  absorption_count integer not null default 0,
  absorption_evidence text,
  alias_absorption_count integer not null default 0,
  marker_absorption_count integer not null default 0,
  primary key (run_id, brand)
);

create index if not exists idx_citation_runs_query_engine
  on citation_runs(query_id, engine);

create index if not exists idx_brand_mentions_brand
  on brand_mentions(brand, engine, mentioned);

create index if not exists idx_citations_domain
  on citations(domain);

create index if not exists idx_citations_gatekeeper
  on citations(gatekeeper_domain)
  where is_gatekeeper;

create index if not exists idx_brand_absorptions_brand
  on brand_absorptions(brand, engine, absorbed);
