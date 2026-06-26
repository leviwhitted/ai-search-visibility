# MarketBrew Oracle — State Audit, Gap Analysis & Path to Demo

**Prepared:** 2026-06-26
**For:** Retell AI "SEO Strategist / Growth SEO Lead" portfolio centerpiece
**North Star:** An agent that ingests MarketBrew knowledge plus client data and outputs cited SEO recommendations.
**Verdict:** ~60% of the way to a demo-able functional Oracle. The hard, risky parts are already built and working. The missing pieces are well-scoped and mostly Codex-delegable (~4–5 focused build-days).

---

## 1. Executive Summary

There are **three** relevant assets, not one, and they fit together better than the project history suggests:

1. **The Knowledge layer** (`C:\Repos\marketbrew`) — a locked, client-grade 130-page reference manual plus a structured, audited 233-atom knowledge base, all distilled from public MarketBrew YouTube/PDF sources. **Complete.**
2. **The Oracle agent prototype** (`C:\Repos\clixsy-oracle-agent`) — half-built. The **grounded cited-Q&A engine is real and working** against Claude Sonnet 4.6 with hard citation integrity. The **recommendation engine is a schema scaffold only** (deterministic template, no LLM reasoning, no client-data intake).
3. **The Retell AEO/GEO measurement harness** (`C:\Repos\gig-work-operating-system\retell-pilot`) — the freshest work. It is *not* the Oracle by design, but it produces exactly the **client-signal evidence** an Oracle would consume. It is the natural source of "client data" for the demo.

The single biggest finding: **the expensive, de-risking work is done.** A clean domain corpus, a working grounded-LLM loop that refuses to hallucinate citations, and a full validated contract suite already exist. What remains is to clone the proven Q&A pattern into a *recommendation* generator, feed it mock client signals, and wrap a thin demo surface around it.

---

## 2. Inventory — What Exists and Where

### 2.A Knowledge layer — `C:\Repos\marketbrew` — COMPLETE

| Asset | State | Detail |
|---|---|---|
| **Reference Manual V1** | LOCKED (2026-04-07) | Build 37 evergreen core (115pp PDF, 62 sections) + Build 38 bounded-current companion (15pp). Two-layer architecture. DOCX + styled PDF produced. Built from public MarketBrew sources. Client-deliverable IP. |
| **Knowledge atom DB** | Frozen v1.0 (2026-02-28) | 233 audited atoms in a structured schema. Tiers: 24 gold / 68 silver / 141 bronze. Types: 150 definition / 36 rule / 26 framework / 21 procedure. Source: Google Sheet `MB_Knowledge_DB`. Has provenance, QA gates, decisions log, source registry. |
| **Tooling** | Stable | Batch staging/upsert scripts, PDF export pipeline (pandoc + XeLaTeX), release parity checks. |

The atom schema is rich: `atom_id, type, title, aka, clean_extract, practical_meaning, difficulty, workflow_stage, role_relevance, tags, inputs, outputs, dependencies, status, confidence, canonical, tier, last_reviewed_date, sources_json, needed_inputs, notes`. Every atom carries `sources_json` provenance — this is what makes citation auditable.

### 2.B Oracle agent prototype — `C:\Repos\clixsy-oracle-agent` — HALF BUILT

Its own README calls it "sparse and scaffold-like." **That is stale.** The repo contains real, tested modules and a working LLM grounding pipeline.

**The Q&A half — REAL and WORKING:**
- `data/kb_snapshot/` — the 233 atoms vendored as a local CSV + manifest + provenance, so runtime is deterministic and reads from a frozen snapshot, not the live sheet (audit anchor commit `c8ba85b`).
- `implementation/kb/snapshot_loader.py` — typed loader for the full atom schema.
- `implementation/qa/qa_engine.py` — the centerpiece. `answer_question()`:
  - loads atoms → builds a grounding system prompt containing the **full atom corpus**, prompt-cached with a 1h TTL,
  - calls **Claude Sonnet 4.6** with structured JSON output + adaptive thinking,
  - validates output against the `qa_answer` JSON schema,
  - **enforces citation integrity** — any cited `atom_id` not present in the KB invalidates the entire answer,
  - forces the model to declare `unknowns` rather than answer outside the KB, with coarse confidence tied to atom tier (gold > silver > bronze).
- `_live_qa_smoke.py` — a real smoke test confirming live Sonnet calls and prompt-cache engagement (cache write on call 1, cache read on call 2).

This is a genuine **"MarketBrew expert that answers with atom-cited evidence and refuses to hallucinate."** It is the hard part, and it works.

**The recommendation half — SCAFFOLD ONLY:**
- `contracts/` — a full, validated JSON-schema suite with examples and a worked end-to-end scenario (`001_recommendation_generation_flow`): `evidence_bundle`, `recommendation`, `recommendation_draft`, `recommendation_generation_request/response`, `evaluation_record`, `outcome_record`, `qa_answer`.
- `implementation/generation/draft_generator.py` — **assembles a recommendation draft from hardcoded template strings** to prove the data-flow shape. There is **no LLM reasoning**, no client-data ingestion, and evidence bundles must be hand-fed.
- `validator/` — 26 passing tests over the contract/flow boundaries.
- Runtime, transport, persistence, auth, deployment are **intentionally unresolved** (documented as deferred).

### 2.C Retell AEO/GEO harness — `C:\Repos\gig-work-operating-system\retell-pilot` — the client-signal instrument

The freshest work (2026-06-26) and the source of shared vocabulary (`SPEC.md`, `BUILD_PLAN.md`). It is deliberately **not** an Oracle (SPEC explicitly excludes a persistent agent and recommendation engine from v1). It measures AI-answer visibility:
- `harness/` — adapters for OpenAI / Perplexity / Gemini, plus `parser`, `scoring`, `storage`, `charts`, `run`.
- `db/schema.sql` — Postgres schema for runs/mentions/citations.
- `sample_data/` + `outputs/sample_run/` — a real offline run with brand-visibility, absorption, gatekeeper, and citation CSVs plus two SVG charts.
- Scoring vocabulary worth reusing: **inclusion / selection / absorption / gatekeeper share** — a more sophisticated evidence model than the Oracle scaffold currently expects.

**Why it matters here:** its outputs *are* the "client data" the Oracle needs. The seam is: `retell-pilot evidence → evidence_bundle → Oracle recommendation engine → cited recommendation`.

---

## 3. Maturity Assessment — Distance to the North Star

North Star = *ingest MarketBrew knowledge + client data → output cited SEO recommendations.*

| Capability | Status | Notes |
|---|---|---|
| MarketBrew knowledge ingestion | ✅ Done | 233 atoms, vendored snapshot, typed loader. |
| Cited Q&A over knowledge | ✅ Done | Working LLM loop, citation integrity, gap-declaration. |
| Evidence / recommendation / citation schemas | ✅ Done | Rich, validated contract suite + worked scenario. |
| Retrieval layer | ✅ N/A at this scale | 233 atoms fit in a cached prompt; full-context stuffing works, **no RAG/embeddings needed for the demo.** |
| **Client-data ingestion** | ❌ Missing | No client-signal schema wired in; evidence bundles are hand-fed. |
| **Recommendation generation (LLM over KB + client signals)** | ❌ Not built | Deterministic placeholder only — the core missing piece. |
| **Demo surface** | ❌ Missing | Only pytest + a throwaway smoke script. No CLI/UI a reviewer can run. |

**Net: ~60% complete.** The de-risking is done (clean corpus, working grounded loop, citation enforcement, schemas). The remaining 40% is additive and well-scoped, not exploratory.

---

## 4. The Gap — Precisely the Seam Between the Two Working Halves

```
  [retell-pilot]              [NEW: client shim]        [clixsy-oracle-agent]
  AEO/GEO evidence  ──────►   evidence_bundle    ──────►  Recommendation engine ──────►  cited recommendation
  (brand visibility,         (existing contract)         (TODAY: template only;          (cites BOTH the client
   citations, gaps)                                       NEEDS: LLM grounded             signal that triggered it
                                                          in KB atoms + signals)          AND the MB atom that
                                                                                          justifies it)
                                            [MB atom corpus] ──┘
```

Two concrete gaps:
1. **Nothing feeds the recommendation engine real client signals.** Need a small client-signal loader that maps SEO data (crawl / GSC-style / AEO-visibility) into the existing `evidence_bundle` contract.
2. **The recommendation engine doesn't reason.** It must become an LLM step — the proven `qa_engine` pattern, but the system prompt now contains *both* the KB atoms *and* the client's evidence bundle, and each output recommendation must cite the client signal that triggered it **and** the MarketBrew atom(s) that justify it.

---

## 5. Shortest Path to a Demo-able Functional Oracle

**Recommended approach:** clone the proven `qa_engine` grounded-LLM pattern into a recommendation generator, feed it **fabricated mock client data** (yes — recommended; see §5.1), reuse the existing contracts and KB loader, and wrap a thin CLI demo. No new infrastructure, no RAG, no dashboard.

### 5.1 Should we fabricate mock client data? — Yes.

The North Star demo needs a client to point at, and there is **no permissible real client** (no Clixsy data; Retell hasn't granted GSC/GA4). Fabricate a clearly-labeled synthetic client. Two good options:
- **Borrow the retell-pilot output shape** — its `outputs/sample_run/*.csv` already encode realistic brand-visibility/citation/gap signals. A synthetic "client" derived from that shape is both realistic *and* on-narrative for the Retell role.
- Or a small hand-authored SEO signal pack (a crawl-style page inventory + a few ranking/visibility gaps) for a fictional SaaS.

Label everything `SYNTHETIC / DEMO DATA` in-file and in the README. This is standard for a portfolio piece and removes any client-data risk.

### 5.2 Build steps & effort

| # | Step | Effort | Owner |
|---|---|---|---|
| 1 | **Mock client dataset** — fabricate a labeled synthetic SEO signal pack (borrow retell-pilot output shape). | ~0.5 day | Codex |
| 2 | **Client-signal loader + evidence_bundle builder** — parse mock signals into the existing `evidence_bundle` contract. | ~0.5–1 day | Codex |
| 3 | **Recommendation engine (the real one)** — clone `qa_engine`'s grounded pattern: system prompt = KB atoms + client evidence bundle; output = N recommendations, each citing the triggering client signal AND the justifying MB atom(s); structured JSON; reject uncited claims; reuse schema validation + citation integrity. **The centerpiece.** | ~1.5–2 days | Claude designs prompt/contract; Codex implements |
| 4 | **Thin demo surface** — a CLI (`oracle ask "…"` and `oracle recommend --client mock`) that prints a cited Q&A answer and a cited recommendation shortlist; optional one-page static HTML report reusing retell-pilot's chart style. | ~1 day | Codex + Claude polish |
| 5 | **Portfolio hygiene** — fork/rename to `marketbrew-oracle`, strip Clixsy branding + internal infra docs, write a clean README (architecture diagram + sample transcript), flip public. | ~0.5 day | Claude |

**Total: ~4–5 focused build-days**, the bulk Codex-delegable. Claude owns the recommendation prompt/contract design (the one genuinely judgment-heavy task) and the demo/README polish.

---

## 6. Portfolio / Public-Repo Readiness

**The story is strong and directly on-target for the Retell GEO/AEO role:**
> "I built a domain-grounded SEO recommendation engine: a curated 233-atom knowledge base distilled from public MarketBrew material, plus an LLM agent that answers questions and generates recommendations with hard citation integrity — it literally cannot cite knowledge that doesn't exist, and it declares gaps instead of hallucinating. Client signals come in as evidence bundles; every recommendation traces back to both the client signal that triggered it and the methodology atom that justifies it."

**Blockers to a public GitHub link (all mechanical, none architectural):**
1. **Repo is named `clixsy-oracle-agent` and Clixsy (a client) branding runs throughout** — including contract examples. Must rebrand to `marketbrew-oracle` and scrub Clixsy references before going public. *(A separate session is assessing the public-link question; this is the key input for it.)*
2. **Repo is currently PRIVATE** (correct for now). Flip public only after the rebrand.
3. **No runnable demo or README story yet** — a reviewer cloning it today sees pytest + scaffolding, not a working Oracle. Steps 4–5 above are what make it linkable.
4. **`ai_context/` and `ChatGPT_Internal_Sources/` contain internal infra notes** (OpenBrain/Supabase architecture, remote-access standards) — exclude from the public version.
5. **The reference manual is paid client-deliverable IP.** Showcase a sample/excerpt and the *method*, not the full 130-page manual, in anything public.

**Good news on security:** no secrets are committed — the Anthropic key is read from the environment (`anthropic.Anthropic()`), not hardcoded. The only "secret" grep hit is a doc *about* secret handling.

---

## 7. Recommendation to Levi

This is a **genuinely strong portfolio centerpiece that is closer to done than it looks**, and the work remaining is the kind that demos extremely well for an AI-native SEO role. The recommended next move is to build out steps 1–5 (§5.2) as a bounded ~4–5 day push, Codex-delegable under Claude's design lead.

**Per the engagement constraints, this session is stopping at the audit. To proceed to build, I need sub-orchestrator authority to dispatch the build work to Codex.**
