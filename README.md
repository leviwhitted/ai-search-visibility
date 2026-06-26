# AI Search Visibility

A Python measurement harness for auditing brand visibility in AI answer engines.

The tool measures where a brand (and its competitors) get cited when buyers ask ChatGPT, Perplexity, or Gemini questions in a given category. It tracks citation share, brand mention rates, answer absorption (does the brand's own framing appear in the AI's answer, not just a link?), and which third-party gatekeeper domains are shaping what the AI says. Config-driven via YAML — swap the query set and competitor list to measure any category.

---

## What it measures

AI answer engines (ChatGPT, Perplexity, Gemini) increasingly answer buyer-intent queries without a buyer visiting a company's website. This pilot measures that surface:

- **Citation inclusion rate** — how often Retell appears vs. Vapi, Bland AI, Synthflow, Cognigy, and PolyAI across 50 buyer-intent queries
- **Brand absorption** — whether Retell's own benchmark data appears in answers, not just its URL
- **Gatekeeper domain share** — which third-party sources (G2, Reddit, Tested.media, Pickaxe, etc.) shape category answers
- **Segment gaps** — where Retell leads (reliability/technical framing) vs. where competitors hold ground (SMB, broad commercial head terms)

---

## Run it now (no API keys needed)

```bash
git clone https://github.com/leviwhitted/ai-search-visibility.git
cd ai-search-visibility
pip install -r requirements.txt

# Full offline run using synthetic sample data
python -m harness.run --mode sample --repetitions 3 --output outputs/sample_run
python -m harness.scoring --input outputs/sample_run/raw_runs.jsonl --output outputs/sample_run
python -m harness.charts --scores outputs/sample_run/brand_scores.csv --citations outputs/sample_run/citations.csv --output outputs/sample_run/charts
```

Sample mode runs end-to-end with synthetic responses — no API keys, no spend. All output files are produced.

---

## Output files

```
outputs/sample_run/
├── raw_runs.jsonl               # One record per engine x query x run
├── runs_index.csv               # Run metadata index
├── mentions.csv                 # Brand mentions extracted from each answer
├── brand_absorption.csv         # Benchmark string detection in answer text
├── citations.csv                # Cited URLs per answer
├── brand_scores.csv             # Aggregate brand inclusion and absorption scores
├── engine_brand_scores.csv      # Scores broken out by engine
├── gatekeeper_summary.csv       # Third-party domain citation share
└── charts/
    ├── inclusion_by_brand.svg
    └── top_citation_domains.svg
```

---

## Live mode (with API keys)

Engine adapters are stubs ready for real keys:

```
harness/adapters/
├── openai_adapter.py       -> needs OPENAI_API_KEY
├── perplexity_adapter.py   -> needs PERPLEXITY_API_KEY
└── gemini_adapter.py       -> needs GEMINI_API_KEY
```

Add keys to `.env`, then run with `--mode live-stub`. Each adapter follows the same interface — swap or extend without touching the scoring or storage layers.

---

## Query taxonomy

50 buyer-intent queries across 8 groups in `queries.yaml`:

| Group | Example |
|-------|---------|
| Category head terms | "Best voice AI platform for customer support teams" |
| Comparison vs. terms | "Retell AI vs Vapi for voice agents" |
| Alternatives battlefield | "Best Vapi alternative for voice agents" |
| Healthcare | "HIPAA-ready AI phone agent for clinics" |
| Financial services | "Voice AI platform for banking call centers" |
| SMB / receptionist | "Best AI answering service for small business" |
| BoFu brand | "Retell AI pricing and cost per minute" |
| Additional verticals | Real estate, hospitality, e-commerce |

GEO research sets a 50-query minimum for a directional read. Each query runs 3-5 times per engine to account for AI-answer variance.

---

## Config files

- `queries.yaml` — full query taxonomy with group and vertical labels
- `competitors.yaml` — Retell plus 6 competitors, domain aliases, and brand variants
- `source_domains.yaml` — gatekeeper citation domains + Retell absorption markers (benchmark strings to detect in answer text)
- `db/schema.sql` — optional Postgres schema for persistent run storage

---

## Measurement principles

The harness controls for AI-answer variance by:

- Running each query multiple times (configurable `--repetitions`)
- Storing raw responses alongside extracted signals
- Distinguishing citation selection (URL cited) from absorption (brand framing appears in answer text)
- Fixing geography and language per `queries.yaml` geo block
- Labeling all output as directional/sampled, not canonical rankings

---

## Project structure

```
ai-search-visibility/
├── harness/
│   ├── run.py              Entry point -- fetch and store raw runs
│   ├── scoring.py          Brand mention extraction and scoring
│   ├── charts.py           SVG/PNG chart generation
│   ├── storage.py          JSONL/CSV persistence (+ optional Postgres)
│   └── adapters/           Engine adapters (OpenAI, Perplexity, Gemini)
├── sample_data/
│   └── sample_responses.jsonl   Synthetic responses for offline demo
├── example_report/         Sample report output (charts + analysis memos)
├── queries.yaml            50 buyer-intent queries across 8 groups
├── competitors.yaml        Retell + 6 competitor definitions
├── source_domains.yaml     Gatekeeper domain registry + absorption markers
├── db/schema.sql           Postgres schema (optional)
├── SPEC.md                 Full measurement methodology and design rationale
└── BUILD_PLAN.md           5-day implementation roadmap
```

---

## Requirements

- Python 3.11+
- PyYAML (required)
- matplotlib (optional, for PNG charts instead of SVG fallback)

```bash
pip install -r requirements.txt
```

---

## License

MIT
