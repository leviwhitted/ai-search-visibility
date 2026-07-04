ILLUSTRATIVE EXAMPLE — generated from synthetic sample data, NOT real Retell measurement.

# Retell AI-Search Visibility Baseline

This is a polished example of the Retell AI-Search Visibility Baseline deliverable format. It uses only the existing pilot sample-run outputs in `retell-pilot/outputs/sample_run/`. No live APIs, Google surfaces, GSC, GA4, or Retell-private data were used.

## Method Summary

The sample run measures 48 buyer-intent prompts across 3 engines (`openai_web_search`, `perplexity_sonar`, and `gemini_grounding`) with 3 repetitions per prompt. That produces 432 measured runs per tracked brand.

The report separates three visibility signals:

- **Inclusion rate:** whether the brand appeared in the AI answer.
- **Selection rate:** whether a brand-owned/source domain was cited.
- **Absorption rate:** whether brand aliases or Retell-specific framing markers appeared in the answer text.

The sample also tracks average brand order, source-domain citation share, and gatekeeper-domain citation share. Brand order is interpreted only within this sampled panel.

## Executive Readout

In this synthetic sample, Retell is not invisible. Retell appears in every measured run and is selected and absorbed in every measured run:

| Brand | Included Runs | Inclusion Rate | Selected Runs | Selection Rate | Absorbed Runs | Absorption Rate |
|---|---:|---:|---:|---:|---:|---:|
| Retell AI | 432/432 | 100.00% | 432/432 | 100.00% | 432/432 | 100.00% |
| Synthflow | 351/432 | 81.25% | 129/432 | 29.86% | 351/432 | 81.25% |
| Bland AI | 270/432 | 62.50% | 69/432 | 15.97% | 270/432 | 62.50% |
| Vapi | 243/432 | 56.25% | 243/432 | 56.25% | 243/432 | 56.25% |
| Cognigy | 243/432 | 56.25% | 129/432 | 29.86% | 243/432 | 56.25% |
| PolyAI | 204/432 | 47.22% | 120/432 | 27.78% | 204/432 | 47.22% |
| Goodcall | 96/432 | 22.22% | 87/432 | 20.14% | 96/432 | 22.22% |
| Air AI | 87/432 | 20.14% | 87/432 | 20.14% | 87/432 | 20.14% |

The resulting brand-order view is more useful than a binary inclusion read. Across included runs, Retell's average brand order is 1.36. Vapi is the closest competitor at 1.84, followed by Bland AI at 2.98, Goodcall at 3.31, Synthflow at 3.50, Cognigy at 3.74, Air AI at 3.97, and PolyAI at 4.24.

## Engine-Level Pattern

Retell is included, selected, and absorbed in 144/144 runs for each measured engine.

| Engine | Retell Inclusion | Retell Selection | Retell Absorption | Strongest Competitor Inclusion |
|---|---:|---:|---:|---|
| `openai_web_search` | 144/144, 100.00% | 144/144, 100.00% | 144/144, 100.00% | Synthflow, 126/144, 87.50% |
| `perplexity_sonar` | 144/144, 100.00% | 144/144, 100.00% | 144/144, 100.00% | Synthflow, 126/144, 87.50% |
| `gemini_grounding` | 144/144, 100.00% | 144/144, 100.00% | 144/144, 100.00% | Synthflow, 99/144, 68.75% |

This sample therefore does not support a claim that Retell has a broad inclusion deficit. The credible interpretation is narrower: Retell has strong baseline presence, but selected verticals and source ecosystems show contested ordering.

## Query-Group Competitive Comparison

Retell leads inclusion in every query group in the sample, but competitors are ordered ahead of Retell in several vertical groups.

| Query Group | Retell Inclusion | Retell Selection | Retell Absorption | Retell Avg. Brand Order | Competitor Pattern |
|---|---:|---:|---:|---:|---|
| `category_head_terms` | 63/63, 100.00% | 63/63, 100.00% | 63/63, 100.00% | 1.33 | Vapi also reaches 63/63 and averages 1.67. |
| `comparison_vs_terms` | 72/72, 100.00% | 72/72, 100.00% | 72/72, 100.00% | 1.00 | Retell is first on average. |
| `healthcare` | 27/27, 100.00% | 27/27, 100.00% | 27/27, 100.00% | 1.00 | Cognigy and PolyAI are included in 27/27. |
| `financial_services` | 27/27, 100.00% | 27/27, 100.00% | 27/27, 100.00% | 3.00 | Cognigy averages 1.00 and PolyAI averages 2.00. |
| `insurance` | 27/27, 100.00% | 27/27, 100.00% | 27/27, 100.00% | 1.00 | Synthflow and Goodcall are also included in 27/27. |
| `debt_collection` | 27/27, 100.00% | 27/27, 100.00% | 27/27, 100.00% | 1.67 | Bland AI averages 1.33. |
| `home_services` | 27/27, 100.00% | 27/27, 100.00% | 27/27, 100.00% | 2.67 | Goodcall averages 1.00 and Synthflow averages 2.33. |
| `alternatives_battlefield` | 63/63, 100.00% | 63/63, 100.00% | 63/63, 100.00% | 1.11 | Synthflow appears in 56/63. |
| `bofu_brand` | 36/36, 100.00% | 36/36, 100.00% | 36/36, 100.00% | 1.11 | Synthflow appears in 32/36. |
| `smb_receptionist` | 36/36, 100.00% | 36/36, 100.00% | 36/36, 100.00% | 1.11 | Synthflow appears in 32/36; Vapi is selected in 24/36. |
| `additional_verticals` | 27/27, 100.00% | 27/27, 100.00% | 27/27, 100.00% | 1.11 | Synthflow appears in 24/27. |

## Gatekeeper and Source Share

The sample includes 1,335 total citations. Retell-owned citations account for 432 citations when combining `retellai.com` and `docs.retellai.com`, or 32.36% of all citations.

| Source Domain | Citation Count | Share of All Citations | Gatekeeper Flag |
|---|---:|---:|---|
| `retellai.com` | 348 | 26.07% | No |
| `vapi.ai` | 201 | 15.06% | No |
| `cognigy.com` | 129 | 9.66% | No |
| `synthflow.ai` | 129 | 9.66% | Yes |
| `poly.ai` | 120 | 8.99% | No |
| `air.ai` | 87 | 6.52% | No |
| `goodcall.com` | 87 | 6.52% | Yes |
| `docs.retellai.com` | 84 | 6.29% | No |
| `bland.ai` | 69 | 5.17% | Yes |
| `docs.vapi.ai` | 42 | 3.15% | No |
| `tested.media` | 39 | 2.92% | Yes |

Gatekeeper citations total 324/1,335, or 24.27% of all citations.

| Gatekeeper Domain | Citation Count | Share of All Citations | Share of Gatekeeper Citations |
|---|---:|---:|---:|
| `synthflow.ai` | 129 | 9.66% | 39.81% |
| `goodcall.com` | 87 | 6.52% | 26.85% |
| `bland.ai` | 69 | 5.17% | 21.30% |
| `tested.media` | 39 | 2.92% | 12.04% |

The source-share readout supports two conclusions in this sample: Retell's owned pages are heavily selected, and a measurable share of the category narrative still routes through gatekeeper or competitor-adjacent sources.

## Top Visibility Gaps

1. **Financial services brand order:** Retell is included and selected in 27/27 financial-services runs, but averages position 3.00 behind Cognigy at 1.00 and PolyAI at 2.00.
2. **Home services brand order:** Retell is included and selected in 27/27 home-services runs, but averages position 2.67 behind Goodcall at 1.00 and Synthflow at 2.33.
3. **Debt collection brand order:** Retell is included and selected in 27/27 debt-collection runs, but Bland AI averages position 1.33 versus Retell at 1.67.
4. **Perplexity category head terms:** Retell remains included, selected, and absorbed in 21/21 Perplexity category-head runs, but Vapi averages position 1.00 while Retell averages 2.00.
5. **Gatekeeper ecosystem:** Gatekeeper citations account for 324/1,335 citations, or 24.27%. Tested.media is the only non-vendor gatekeeper surfaced in the top-domain sample at 39 citations, or 2.92% of all citations.

## Static Visuals

- [Brand visibility rates](charts/brand_visibility_rates.svg)
- [Citation source-domain share](charts/source_domain_share.svg)

## Note: synthetic scores vs. live signal

The 100% Retell scores above come from the synthetic sample panel and exist only to demonstrate the report format. A separate set of live, single-run spot checks on logged-in consumer engines surfaced a different and more actionable pattern: for several vertical, receptionist, and comparison framings, Retell was not cited at all, and vertical-specialist competitors appeared in its place. That divergence is exactly why the real deliverable runs repeated samples per query across engines rather than trusting any single answer. Treat the live spot check as directional and the synthetic scores as format-only.

## Limitations

This is an illustrative example generated from synthetic sample data, not a real Retell measurement. The sample run is designed to prove the report shape and scoring workflow.

The measurements are directional. AI answers can vary by run, model version, geography, personalization, source availability, and API versus consumer UI behavior. The sample does not include official Google AI Overview data, because no official Google AI Overview API is assumed. It also does not include Retell GSC, GA4, CMS, CRM, or private analytics data.

Because Retell scores 100.00% inclusion, selection, and absorption in this sample, this report does not claim Retell has a broad AI-search visibility deficit. The defensible gaps are brand-order and source-influence gaps within specific query groups and engines.
