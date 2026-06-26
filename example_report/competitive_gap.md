ILLUSTRATIVE EXAMPLE — generated from synthetic sample data, NOT real Retell measurement.

# Competitive Gap Memo

This memo lists only gaps supported by the sample-run CSVs. In the sample, Retell does **not** trail any competitor on inclusion rate, selection rate, or absorption rate at the aggregate brand level. Retell is 432/432 on all three.

The competitive gaps below are therefore brand-order gaps: cases where Retell is included, selected, and absorbed, but another brand appears earlier on average within the same query group and engine.

| Engine | Query Group | Runs | Retell Inclusion / Selection / Absorption | Retell Avg. Brand Order | Competitor Ahead | Competitor Avg. Brand Order | Competitor Inclusion / Selection / Absorption |
|---|---|---:|---:|---:|---|---:|---:|
| `gemini_grounding` | `debt_collection` | 9 | 100.00% / 100.00% / 100.00% | 2.00 | Bland AI | 1.00 | 100.00% / 100.00% / 100.00% |
| `openai_web_search` | `debt_collection` | 9 | 100.00% / 100.00% / 100.00% | 2.00 | Bland AI | 1.00 | 100.00% / 100.00% / 100.00% |
| `gemini_grounding` | `financial_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | Cognigy | 1.00 | 100.00% / 100.00% / 100.00% |
| `gemini_grounding` | `financial_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | PolyAI | 2.00 | 100.00% / 100.00% / 100.00% |
| `openai_web_search` | `financial_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | Cognigy | 1.00 | 100.00% / 100.00% / 100.00% |
| `openai_web_search` | `financial_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | PolyAI | 2.00 | 100.00% / 100.00% / 100.00% |
| `perplexity_sonar` | `financial_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | Cognigy | 1.00 | 100.00% / 100.00% / 100.00% |
| `perplexity_sonar` | `financial_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | PolyAI | 2.00 | 100.00% / 100.00% / 100.00% |
| `gemini_grounding` | `home_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | Goodcall | 1.00 | 100.00% / 100.00% / 100.00% |
| `gemini_grounding` | `home_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | Synthflow | 2.00 | 100.00% / 100.00% / 100.00% |
| `openai_web_search` | `home_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | Goodcall | 1.00 | 100.00% / 100.00% / 100.00% |
| `openai_web_search` | `home_services` | 9 | 100.00% / 100.00% / 100.00% | 3.00 | Synthflow | 2.00 | 100.00% / 100.00% / 100.00% |
| `perplexity_sonar` | `home_services` | 9 | 100.00% / 100.00% / 100.00% | 2.00 | Goodcall | 1.00 | 100.00% / 100.00% / 100.00% |
| `perplexity_sonar` | `category_head_terms` | 21 | 100.00% / 100.00% / 100.00% | 2.00 | Vapi | 1.00 | 100.00% / 100.00% / 100.00% |

## Interpretation

Retell's sample visibility is strong; the gap is not absence. The recurring weak spots are the financial-services, home-services, debt-collection, and Perplexity category-head contexts where the answer still includes Retell but leads with a competitor.

That distinction matters for action planning. The right response is not generic "get indexed" work. The more relevant plays are vertical authority, answer-first pages for contested query groups, and third-party source wins that can change the first-mentioned brand in answers where Retell is already present.
