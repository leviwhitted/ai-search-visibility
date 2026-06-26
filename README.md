# Retell AI SEO Mini-Pilot

Lean v1 scaffold for a 5-business-day AEO and competitive-visibility mini-pilot.

The package is intentionally small: plain Python, YAML config, JSONL/CSV output, optional Postgres schema, and static charts. Live API calls are stubbed until keys are added.

## What Runs Offline

The sample mode runs end-to-end without live keys:

```powershell
cd C:\Repos\gig-work-operating-system\retell-pilot
python -m harness.run --mode sample --repetitions 3 --output outputs\sample_run
python -m harness.scoring --input outputs\sample_run\raw_runs.jsonl --output outputs\sample_run
python -m harness.charts --scores outputs\sample_run\brand_scores.csv --citations outputs\sample_run\citations.csv --output outputs\sample_run\charts
```

Expected outputs:

- `raw_runs.jsonl`
- `runs_index.csv`
- `mentions.csv`
- `brand_absorption.csv`
- `brand_visibility.csv`
- `citations.csv`
- `brand_scores.csv`
- `engine_brand_scores.csv`
- `group_brand_scores.csv`
- `engine_group_brand_scores.csv`
- `source_domain_share.csv`
- `gatekeeper_domain_share.csv`
- `gatekeeper_summary.csv`
- `charts/inclusion_by_brand.svg` offline fallback, or `.png` when `matplotlib` is installed
- `charts/top_citation_domains.svg` offline fallback, or `.png` when `matplotlib` is installed

## Requirements

Minimum:

- Python 3.11+
- PyYAML

Optional for polished PNG charts:

- matplotlib

Install locally if needed:

```powershell
python -m pip install -r requirements.txt
```

## Live API Status

The engine adapters are deliberate stubs:

- `harness/adapters/openai_adapter.py`
- `harness/adapters/perplexity_adapter.py`
- `harness/adapters/gemini_adapter.py`

Each adapter has TODO markers for the real API call. Until implemented, `--mode live-stub` writes a structured placeholder and `--mode sample` uses synthetic responses from `sample_data/sample_responses.jsonl`.

Required keys/accounts for live work:

- `OPENAI_API_KEY`
- `PERPLEXITY_API_KEY`
- `GEMINI_API_KEY`
- DataForSEO credentials for rank/SERP and sampled AI-surface visibility

## Config Files

- `queries.yaml`: buyer-query taxonomy.
- `competitors.yaml`: Retell plus competitor aliases/domains.
- `source_domains.yaml`: gatekeeper citation domains plus Retell absorption markers.
- `db/schema.sql`: optional Postgres schema.

## Notes

The measurement is directional. Store raw outputs and report repeated-run counts because AI-answer surfaces vary by engine, model, timing, location, and prompt wording.
