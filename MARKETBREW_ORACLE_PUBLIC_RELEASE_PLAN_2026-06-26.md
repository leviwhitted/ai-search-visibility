# MarketBrew Oracle — Public-Repo Release Plan (Rebrand & Scrub)

**Prepared:** 2026-06-26
**Goal:** Make the Oracle linkable as a public GitHub portfolio repo for the Retell role, with zero client (Clixsy) exposure and no internal infra leakage.
**Sequencing:** Execute this **after** the `feat/oracle-recommendation-engine` Codex build lands and is reviewed, so the new (clean-named) recommendation/CLI modules are included. This is a plan, not yet an action.

---

## 1. Strategy — fresh public repo, not an in-place flip

**Recommended: create a NEW public repo `marketbrew-oracle` and copy a curated, scrubbed subset into it with fresh history.** Do **not** simply rename `clixsy-oracle-agent` and flip it public.

Why:
- **Git history is a liability.** Every historical commit in `clixsy-oracle-agent` carries the Clixsy name and internal working notes. Flipping the repo public exposes all of it; `git filter-repo` to scrub history is error-prone and still leaves the old name in the URL/forks. A fresh repo with a clean initial commit is safer and cleaner.
- **Curation control.** A fresh repo lets us include exactly the public surface and nothing else.
- The existing `clixsy-oracle-agent` stays private as the working repo.

---

## 2. Scope of the scrub (current state)

- **67** occurrences of "clixsy" across **23 JSON, 10 MD, 8 PY** files.
- **14** of those are schema `$id` URLs pointing at `github.com/leviwhitted/clixsy-oracle-agent/...` — must repoint to the new repo URL.
- Hardcoded default ids to change, e.g. `project_id="clixsy-oracle-smoke"` → `marketbrew-oracle-demo`.
- New modules from the Codex build (recommend/, client_signals/, cli, mock data) are spec'd to be clean already (synthetic, no Clixsy), so they need only the schema-URL repoint, not name scrubbing.

---

## 3. INCLUDE in the public repo (the runnable Oracle)

- `implementation/` — kb loader, contracts boundary, qa engine, **recommend engine (new)**, **client_signals (new)**, generation/records/fixtures, **cli (new)**.
- `contracts/` — all schemas + specs + examples (with `$id` URLs repointed).
- `data/kb_snapshot/` — the atom snapshot + manifest + provenance **(see §6 IP decision)**.
- `data/mock_clients/acme_voice_ai/` — synthetic demo data (clearly labeled).
- `validator/` — the test suite.
- `requirements.txt`, `.gitignore`, a fresh `README.md`, `LICENSE`.
- `outputs/` — optionally a sample demo run + the static HTML report as a showcase artifact.

## 4. EXCLUDE from the public repo (internal-only)

- `ai_context/` — internal orientation/working-state notes.
- `ChatGPT_Internal_Sources/` — internal infra decisions (OpenBrain/Supabase architecture, remote-access standards, secret-handling SOP). **Must not be public.**
- `browser_context/` — internal browser-model handoff packs.
- `research/janus/` — the build brief + peer-model dispatch notes.
- `delegated.md`, `_live_qa_smoke.py` (throwaway), and any `STATUS`/phase-status working docs.

---

## 5. Scrub & rebrand checklist (mechanical, automatable)

1. Copy the INCLUDE set into a fresh `C:\Repos\marketbrew-oracle\` working tree.
2. Global replace `clixsy-oracle-agent` → `marketbrew-oracle` and `clixsy` → `marketbrew` across `*.py *.md *.json` (then eyeball each — some "clixsy" strings are in example payloads/project_ids).
3. Repoint all schema `$id` URLs to `github.com/leviwhitted/marketbrew-oracle/...`.
4. Update default ids/strings (`project_id` demo defaults, smoke labels).
5. Rewrite `README.md` (see §7) and add a `LICENSE` (see §8).
6. Re-run the full validator suite in the new tree — must stay green after the rename.
7. `git init` fresh, single clean initial commit, create the **private** GitHub repo first, push, verify, then flip to public only after the secret scan (§9).

---

## 6. The one real decision for Levi — publishing the 233-atom KB

The atom snapshot (`data/kb_snapshot/*.csv`) is **distilled from public MarketBrew YouTube/PDF sources**, so there is no third-party rights issue. But the curation itself (233 audited, tiered, schema-structured atoms) is arguably the most valuable artifact you produced — and a public repo needs *some* KB to be runnable.

Three options:
- **(a) Ship all 233 atoms.** Maximum "wow," fully runnable, shows the depth of the corpus. Cost: gives away the full curated KB.
- **(b) Ship a representative public sample (~30–50 atoms across all tiers/types) + keep the full 233 private.** Repo still runs and demos convincingly; full corpus stays proprietary. **Recommended default.**
- **(c) Ship zero atoms; provide a tiny synthetic toy KB for the public demo.** Safest IP-wise, least impressive.

**Recommendation: (b).** It keeps the demo genuine and runnable while protecting the full corpus as your IP. Needs your call.

> Note: the 130-page reference manual is paid client-deliverable IP and lives in `C:\Repos\marketbrew`, not in this repo. It stays out of the public release entirely; reference it as "method" in the README, do not ship it.

---

## 7. README story (portfolio-grade)

Lead with the on-target narrative (matches the Retell GEO/AEO role):
- One-paragraph hook: a domain-grounded SEO recommendation engine with **hard citation integrity** — it cannot cite knowledge that doesn't exist and declares gaps instead of hallucinating.
- **Architecture diagram:** MarketBrew atom corpus + client evidence bundle → grounded LLM → cited recommendation (cites both the client signal and the methodology atom). (Mermaid is fine; renders on GitHub.)
- **Quickstart:** clone → `.venv` → install → set `ANTHROPIC_API_KEY` → `oracle ask` / `oracle recommend --client acme_voice_ai`.
- **Sample transcript:** a real captured Q&A answer + a recommendation shortlist with visible atom + finding citations.
- A short "how it works / citation-integrity" section and a "synthetic demo data" disclaimer.

## 8. LICENSE

- Code: MIT (portfolio-friendly, permissive).
- If shipping any atom data, add a short data-use note clarifying the atoms are a curated derivative of public MarketBrew material for demonstration.

## 9. Pre-publish secret scan (gate)

Before flipping public: scan the new tree for keys/PII/client names (`gitleaks` or a targeted grep for `sk-`, `ANTHROPIC_API_KEY`, "clixsy", real client names). Confirm `ChatGPT_Internal_Sources/` and `ai_context/` are absent. Only then flip the repo to public. (Current working repo already keeps the key in env, no committed secrets.)

---

## 10. Effort

~0.5–1 day, mostly mechanical and automatable, once the Codex build has landed and been reviewed. The only blocking input is the §6 KB-publication decision.
