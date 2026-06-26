# Retell AI SEO Mini-Pilot Build Plan

## Pilot Cadence

### Day 1 - Setup, Taxonomy, Baseline Inputs

- Confirm API/accounts checklist.
- Freeze buyer-query taxonomy and competitor set.
- Pull Retell public sitemap and main content inventory.
- Create DataForSEO keyword/SERP task list for priority queries.
- Run offline harness on sample data to confirm output shape.

### Day 2 - Citation Runs

- Run OpenAI web search, Perplexity Sonar, and Gemini grounding samples.
- Execute 3-5 repetitions per prompt per engine.
- Use low temperature where supported.
- Store raw JSON responses and run metadata.
- Spot-check citation URLs and brand extraction.

### Day 3 - SERP and Competitive Baseline

- Pull DataForSEO rank/SERP data for priority buyer terms.
- Capture sampled SERP/AI-surface observations where available and label them non-official.
- Build competitor intersection table: which domains/pages appear for the same queries.
- Inventory Retell public pages against buyer-query groups.

### Day 4 - Scoring and Gaps

- Score inclusion rate, brand order/rank, source-domain share, and confidence bands.
- Compare Retell visibility against competitors by engine and query group.
- Identify source/page types repeatedly cited for competitors but missing for Retell.
- Draft prioritized action shortlist.

### Day 5 - Delivery Package

- Finalize baseline report.
- Add competitive-gap memo and raw appendix.
- Generate 1-2 static charts.
- Write 2-3 week follow-on implementation plan.
- Package assumptions, limitations, and recommended validation checks.

## Buyer-Query Taxonomy

The v1 prompt set is intentionally buyer-intent oriented. Exact prompts live in `queries.yaml`; that file is canonical and currently contains a ~50-prompt panel (48 prompts) across head terms, comparisons, verticals, alternatives, BOFU brand checks, SMB receptionist demand, and additional vertical probes.

### Category Head Terms

1. What is the best voice AI platform for customer support teams?
2. Best AI phone agent platform for businesses.
3. Top conversational voice AI platforms for call centers.
4. Best AI voice agent API for developers.
5. Best AI receptionist software for inbound calls.
6. Best outbound AI calling platform for sales teams.
7. Voice AI platform with low latency and natural conversations.

### Comparison and VS Terms

1. Retell AI vs Vapi for voice agents.
2. Retell AI vs Synthflow for AI phone calls.
3. Retell AI vs Bland AI for outbound calling.
4. Vapi vs Bland AI vs Retell AI.
5. Synthflow alternatives for voice AI agents.
6. Bland AI alternatives for enterprise voice AI.
7. Best Retell AI alternatives.
8. Cognigy vs Retell AI for contact centers.

### Healthcare Queries

1. Best voice AI platform for healthcare appointment scheduling.
2. HIPAA-ready AI phone agent for clinics.
3. AI voice agents for patient intake calls.

### Financial Services Queries

1. Best AI phone agent for financial services customer support.
2. Voice AI platform for banking call centers.
3. AI voice agent for loan servicing calls.

### Insurance Queries

1. Best AI voice agent for insurance claims intake.
2. AI phone automation for insurance agencies.
3. Voice AI platform for insurance customer support.

### Debt Collection Queries

1. AI voice agent for debt collection calls.
2. Best automated phone system for collections teams.
3. Compliant voice AI for payment reminder calls.

### Home Services Queries

1. Best AI receptionist for home services companies.
2. AI phone answering for HVAC businesses.
3. Voice AI for plumbing service appointment booking.

### Additional Configured Groups

The expanded panel also includes:

- `alternatives_battlefield`: competitor-vs-competitor and Retell-alternative prompts where listicles and peripheral vendors often shape the answer.
- `bofu_brand`: pricing, compliance, reliability, and current-year brand-intent prompts.
- `smb_receptionist`: small-business, dental, and medical-office receptionist demand.
- `additional_verticals`: real estate, hospitality, and ecommerce probes.

## Competitor Set

Primary brand:

- Retell AI

Competitors:

- Vapi
- Synthflow
- Bland AI
- Cognigy
- Air AI
- Goodcall
- PolyAI

PolyAI is included as the seventh competitor because it appears in enterprise conversational AI and call-center buying contexts, which helps separate startup/developer comparisons from enterprise contact-center comparisons.

## Citation-Run Methodology

Engines:

- OpenAI web search through the Responses API.
- Perplexity Sonar.
- Gemini API with Google Search grounding.

Run controls:

- 3-5 repetitions per prompt per engine.
- Temperature 0 or lowest supported value.
- Fixed geography: United States, with California/Redwood City noted where supported.
- Fixed collection window: complete all runs within the same business day when possible.
- Fresh session per prompt run.
- Store raw answer text, citations, engine/model, timestamp, query ID, query group, repetition, geo, temperature, and adapter metadata.

Pitfalls and labels:

- AI answers are non-deterministic.
- API output may differ from consumer UI.
- Citation URLs can be incomplete or hallucinated.
- Geo and personalization can affect results.
- Google AI Overview data is sampled/non-official unless Google publishes an official API later.

## Scoring

Core metrics:

- Inclusion rate: share of runs where a brand is mentioned.
- Selection rate: share of runs where a brand-owned domain is cited.
- Absorption rate: share of runs where the brand's aliases or Retell-specific framing/data appear in the answer text. Retell marker checks come from `source_domains.yaml` (`680ms`, `99.2%`, `turn-taking`, `production-grade`, `SOC 2 Type II`).
- Brand-order/rank: first mention order among tracked brands.
- Source-domain share: share of cited domains associated with a brand or recurring source.
- Gatekeeper citation share: share of citations from third-party gatekeeper domains in `source_domains.yaml` (for example Tested.media, Pickaxe, Vellum, AgentZap, G2, Capterra, Reddit).
- Competitor co-mention rate: how often Retell appears with each competitor.
- Prompt-group splits: report inclusion, selection, absorption, and brand order by query group and engine.
- Confidence bands: Wilson-style or simple repeated-run intervals over inclusion counts.

Report with counts:

- Prefer "Retell appeared in 7 of 15 runs" over false-precision percentages alone.
- Show prompt group and engine splits.
- Keep low sample sizes visible.

Selection versus absorption is a required distinction. A cited Retell URL proves source selection; Retell latency/reliability framing in the answer text proves absorption. Selection without absorption should be treated as weaker influence.

## Data Sources

DataForSEO:

- Rank and SERP snapshots for priority buyer terms.
- Keyword data where available.
- Competitor intersections and recurring SERP domains.
- Sampled SERP/AI-surface visibility where supported, labeled non-official for AI Overview-style features.

Without GSC access:

- Public crawl from Retell sitemap and discoverable pages.
- Indexed-page sample using public search operators where appropriate.
- DataForSEO ranked keyword and SERP coverage.
- Competitor page intersections for the same buyer terms.
- Public backlink/mention estimates only if available and clearly labeled.
- AI-answer sampled citation runs as directional visibility evidence.

## Deliverable Formats

- `baseline_report.md`: concise narrative with method, findings, caveats, and top gaps.
- `competitive_gap.csv`: brand/query/engine visibility matrix.
- `action_shortlist.md`: 10 prioritized moves with evidence and validation signals.
- `raw_runs.jsonl`: unedited run log.
- `mentions.csv`: extracted brand mentions by run.
- `brand_absorption.csv`: answer-text absorption markers and evidence by run/brand.
- `brand_visibility.csv`: joined mention, cited-domain selection, and absorption rows by run/brand.
- `citations.csv`: extracted citation URLs and domains by run.
- `gatekeeper_domain_share.csv` and `gatekeeper_summary.csv`: citation battlefield outputs.
- `group_brand_scores.csv` and `engine_group_brand_scores.csv`: per-group score splits.
- Static charts:
  - Inclusion rate by brand and engine.
  - Citation/source-domain share for top domains.

Action-shortlist recommendations must map back to the evidence-ranked levers in `SPEC.md`: earned media / third-party authoritative coverage, G2/Capterra review presence, answer-first structure, authoritative quotes/original statistics, entity/Knowledge Graph clarity, and gatekeeper/listicle ecosystem coverage. Do not present schema markup or `llms.txt` as primary recommendations; treat them as hygiene or inert unless future evidence changes.

## API Keys and Accounts Checklist

TODO for Levi:

- OpenAI API key with web search access.
- Perplexity API key with Sonar access.
- Gemini API key with Google Search grounding access.
- DataForSEO account and API credentials.
- Optional: Retell-approved GSC/GA4/CMS access for Phase 2 only.
- Optional: Screaming Frog license or equivalent crawler if public crawl needs more depth.
