# Retell AI SEO Mini-Pilot Spec

## Positioning

This is a lean 5-business-day AEO and competitive-visibility mini-pilot for Retell AI. The operator-proof frame is simple: produce a Retell-specific instrument that shows where Retell appears, where competitors appear, which sources are shaping AI/search answers, and which actions Retell can ship first.

This is not branded as an Oracle product in v1. The working artifact is an AEO visibility baseline plus competitive gap report. It should be useful even if Retell never grants GSC, GA4, or CMS access.

Strategic framing (important): research shows Retell already holds a real GEO advantage on the technical/reliability narrative. Its benchmark data (680ms latency, 99.2% tool-calling accuracy) gets cited, and its own retell-vs-X comparison content is ingested by AI engines. The pilot must NOT claim Retell is invisible in AI search. The credible thesis is: Retell wins the reliability framing but cedes ground on (a) broad commercial head terms, (b) SMB-adjacent and receptionist demand, and (c) the third-party gatekeeper ecosystem, and none of it is measured systematically. The pilot's job is to quantify citation share, locate the contested segments, and recommend how to extend the existing moat, not to overclaim a deficit.

## V1 Scope

V1 uses plain Python plus Postgres or CSV. It does not include pgvector, RAG, embeddings, n8n, a dashboard app, or automated content generation.

Included:

- Buyer-query taxonomy with ~50 Retell-relevant prompts (GEO research sets a 50-prompt floor for a directional read; see `queries.yaml`).
- Competitor set of 5-7 voice AI and conversational AI vendors.
- Reproducible citation-run harness for OpenAI web search, Perplexity Sonar, and Gemini grounding.
- Repeated prompt runs, raw response storage, extracted brand mentions, extracted citations, and basic scoring.
- External-market baseline without GSC: public crawl/sitemap inventory, indexed-page sample, DataForSEO rank/SERP data, competitor intersections, and sampled AI-search visibility.
- Compact report package: baseline memo, competitive gap matrix, prioritized action shortlist, raw appendix, and 1-2 static charts.

Excluded from v1:

- No official Google AI Overviews API claims.
- No Retell private analytics dependency.
- No dashboard app.
- No persistent agent or recommendation engine.
- No shared client corpus.
- No client-specific MarketBrew or Clixsy data.
- No embeddings or vector database.

## Measurement Principles

The AI-answer measurement is directional and sampled. It is not a canonical ranking source.

Controls:

- Run each prompt 3-5 times per engine.
- Use low temperature where supported.
- Fix geography and language where APIs support it.
- Run within a fixed collection window.
- Use fresh sessions and no conversation history.
- Store raw responses, citations, extracted brands, source URLs, model/engine, timestamp, location, and run metadata.
- Measure both citation selection and citation absorption: track not only whether a brand's URL is cited, but whether the brand's own framing/data appears in the answer text (Retell's `680ms` / `99.2%` benchmarks; see `source_domains.yaml` absorption_markers). Selection without absorption overstates influence (Zhang et al. 2026).
- Flag third-party gatekeeper domains (see `source_domains.yaml`): when answers cite Tested.media, Pickaxe, Vellum, AgentZap, Zeeg, G2, Reddit, etc., record it so the report shows which sources shape the category narrative.

Google AI Overview visibility is handled through DataForSEO or sampled SERP capture where available and labeled as sampled/non-official. The report must not imply Google provides an official AI Overview API for this purpose.

## Deliverables

1. Baseline report
   - Retell inclusion rate across prompt groups and engines.
   - Competitor inclusion rate and brand-order comparison.
   - Citation/source domains shaping answers.
   - SERP visibility snapshot for priority buyer terms.
   - Data limitations clearly labeled.

2. Competitive-gap memo
   - Prompt groups where Retell is absent or lower ordered than key competitors.
   - Competitor pages/sources repeatedly cited.
   - Content, comparison, and authority gaps.

3. Prioritized action shortlist
   - 10 recommendations max.
   - Each recommendation includes query group, evidence, mechanism, effort, expected visibility signal, and 2-week validation check.

4. Evidence appendix
   - Raw prompt list.
   - Raw sampled responses.
   - Extracted mentions and citations.
   - Scoring table.

5. Static visuals
   - Brand inclusion rate by competitor and engine.
   - Source-domain share or prompt-group gap heatmap.

## Success Criteria

The pilot succeeds if it produces a defensible artifact Retell can evaluate quickly:

- At least 45 buyer-intent prompts are run across 3 engines with 3+ repetitions each (the ~50-prompt panel is the target floor).
- Raw responses and scoring outputs are reproducible from config files.
- Retell, Vapi, Synthflow, Bland AI, Cognigy, Air AI, Goodcall, and one additional competitor are measured consistently.
- The report identifies at least 5 specific Retell visibility gaps and at least 5 source/page opportunities.
- Every recommendation is tied to observed evidence, not generic SEO advice.
- Limitations are stated plainly, especially AI-answer sampling variance and non-official Google AI Overview measurement.

The pilot does not need to prove traffic lift inside five business days. It needs to prove that Levi can build and operate an AI-native search visibility instrument with practical recommendations.

## Data Governance

Retell data, MarketBrew material, and any future client corpora stay isolated. Public MarketBrew YouTube/PDF material can be referenced as public proof of methodology, but no Clixsy data is used in this pilot.

V1 outputs should be shareable with Retell as a standalone public-data diagnostic unless Retell later provides private access.

## Evidence Base and Recommendation Levers

Recommendations in the action shortlist must map to evidence-backed levers, not generic SEO. Per the archived GEO/AEO research (`research/raw_perplexity_2026-06-26/aeo-geo-citation-report.md`) and competitive analysis (`research/raw_gemini_2026-06-26/advanced_ai_voice_agent_seo_analysis.txt`), the highest-leverage levers for a SaaS like Retell, in order:

1. Earned media / third-party authoritative coverage (outperforms owned content ~325% for AI citation).
2. Review-site presence (G2/Capterra is a near-binary citation gate for SaaS; ~100%/99% of cited SaaS tools had them).
3. Answer-first content structure (front-loaded, self-contained answers).
4. Authoritative quotes plus original statistics (+41% / +33% visibility).
5. Entity clarity / Knowledge Graph presence (brand-mention correlation 0.66 vs 0.22 for backlinks).
6. Winning the gatekeeper/listicle ecosystem (Tested.media, Pickaxe, Vellum, AgentZap) via digital PR and analyst relations.

Explicitly NOT primary levers: schema markup (no independent citation lift in a 1,885-page RCT; hygiene only) and llms.txt (inert). Retell already runs strong owned comparison content, so the differentiated value is measurement/instrumentation plus extending into under-owned segments and the gatekeeper sources.

## Phase 2 - Full Oracle Roadmap

Phase 2 is future scope only. It should be discussed after Retell has seen the v1 artifact and, ideally, provided GSC/GA4/CMS access.

Layer 1: Signal ingestion

- Retell GSC and GA4 exports.
- Technical crawl and sitemap inventory.
- DataForSEO rank/SERP and competitor intersections.
- AI-answer citation tracking over time.
- Content inventory and page-level metadata.

Layer 2: Knowledge corpus

- Public SEO best-practice corpus.
- Public AEO/GEO corpus.
- Public MarketBrew methodology atoms where rights are clear.
- Structured citations and provenance.
- Optional pgvector only after corpus usefulness is proven.

Layer 3: Reasoning engine

- Evidence-bundle recommendations.
- Each recommendation cites the Retell signal that triggered it and the public best-practice basis.
- Scoring by impact, effort, confidence, and validation signal.
- Modes for audit, strategy, content planning, and monitoring.

Layer 4: Surfacing and action

- Dashboard or reporting surface only if Retell wants ongoing operations.
- Recommendation queue.
- Monitoring views for rank, citation share, and content actions.
- Optional programmatic page/content workflow.

Phase 2 can become a reusable growth-intelligence engine, but client-specific data and corpora must remain separate.
