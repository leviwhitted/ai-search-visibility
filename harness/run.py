from __future__ import annotations

import argparse
import hashlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from harness.adapters import GeminiGroundingAdapter, OpenAIWebSearchAdapter, PerplexitySonarAdapter
from harness.adapters.base import PromptRun, SampleResponseStore
from harness.config import PROJECT_ROOT, load_queries
from harness.storage import ensure_dir, write_csv, write_jsonl


ADAPTERS = {
    "openai_web_search": OpenAIWebSearchAdapter,
    "perplexity_sonar": PerplexitySonarAdapter,
    "gemini_grounding": GeminiGroundingAdapter,
}


def build_run_id(engine: str, query_id: str, repetition: int, captured_at: str) -> str:
    raw = f"{engine}:{query_id}:{repetition}:{captured_at}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:16]


def build_record(raw: dict[str, Any], prompt_run: PromptRun, captured_at: str) -> dict[str, Any]:
    record = dict(raw)
    record.update(
        {
            "run_id": build_run_id(record["engine"], prompt_run.query["id"], prompt_run.repetition, captured_at),
            "query_id": prompt_run.query["id"],
            "query_group": prompt_run.query["group"],
            "query_text": prompt_run.query["text"],
            "vertical": prompt_run.query.get("vertical", ""),
            "repetition": prompt_run.repetition,
            "captured_at": captured_at,
            "mode": prompt_run.mode,
            "country": prompt_run.geo.get("country", ""),
            "region": prompt_run.geo.get("region", ""),
            "city": prompt_run.geo.get("city", ""),
            "language": prompt_run.geo.get("language", ""),
            "temperature": 0,
        }
    )
    return record


def run_harness(args: argparse.Namespace) -> list[dict[str, Any]]:
    queries, geo = load_queries(args.queries)
    sample_store = None
    if args.mode == "sample":
        sample_store = SampleResponseStore(PROJECT_ROOT / "sample_data" / "sample_responses.jsonl")

    adapter_names = args.engines or list(ADAPTERS.keys())
    adapters = [ADAPTERS[name](sample_store=sample_store) for name in adapter_names]

    records: list[dict[str, Any]] = []
    for query in queries:
        for adapter in adapters:
            for repetition in range(1, args.repetitions + 1):
                captured_at = datetime.now(UTC).isoformat()
                prompt_run = PromptRun(query=query, geo=geo, repetition=repetition, mode=args.mode)
                raw = adapter.run(prompt_run)
                records.append(build_record(raw, prompt_run, captured_at))
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Retell AEO citation harness.")
    parser.add_argument("--mode", choices=["sample", "live-stub"], default="sample")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--queries", default="queries.yaml")
    parser.add_argument("--output", default="outputs/latest")
    parser.add_argument(
        "--engines",
        nargs="*",
        choices=sorted(ADAPTERS.keys()),
        help="Optional subset of engines.",
    )
    args = parser.parse_args()

    output_dir = ensure_dir(Path(args.output))
    records = run_harness(args)
    write_jsonl(output_dir / "raw_runs.jsonl", records)
    write_csv(
        output_dir / "runs_index.csv",
        records,
        fieldnames=[
            "run_id",
            "query_id",
            "query_group",
            "vertical",
            "engine",
            "model",
            "repetition",
            "captured_at",
            "mode",
            "country",
            "region",
            "city",
            "language",
            "temperature",
        ],
    )
    print(f"Wrote {len(records)} raw runs to {output_dir}")


if __name__ == "__main__":
    main()
