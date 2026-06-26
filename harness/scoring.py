from __future__ import annotations

import argparse
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from harness.config import load_competitors, load_source_domains
from harness.parser import (
    domain_share,
    extract_brand_absorption,
    extract_brand_mentions,
    extract_citations,
    gatekeeper_share,
    gatekeeper_summary,
)
from harness.storage import ensure_dir, read_jsonl, write_csv


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return 0.0, 0.0
    phat = successes / total
    denominator = 1 + z * z / total
    center = (phat + z * z / (2 * total)) / denominator
    margin = z * math.sqrt((phat * (1 - phat) + z * z / (4 * total)) / total) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def build_brand_visibility(
    mentions: list[dict[str, Any]],
    absorptions: list[dict[str, Any]],
    citations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    absorptions_by_run_brand = {
        (row["run_id"], row["brand"]): row
        for row in absorptions
    }
    selected_run_brands = {
        (row["run_id"], row["cited_brand"])
        for row in citations
        if row.get("cited_brand")
    }

    rows: list[dict[str, Any]] = []
    for mention in mentions:
        key = (mention["run_id"], mention["brand"])
        absorption = absorptions_by_run_brand.get(key, {})
        rows.append(
            {
                **mention,
                "selected": key in selected_run_brands,
                "absorbed": bool(absorption.get("absorbed", False)),
                "absorption_count": absorption.get("absorption_count", 0),
                "absorption_evidence": absorption.get("absorption_evidence", ""),
                "alias_absorption_count": absorption.get("alias_absorption_count", 0),
                "marker_absorption_count": absorption.get("marker_absorption_count", 0),
            }
        )
    return rows


def score_visibility(
    visibility: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_brand: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_engine_brand: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_group_brand: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_engine_group_brand: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in visibility:
        by_brand[row["brand"]].append(row)
        by_engine_brand[(row["engine"], row["brand"])].append(row)
        by_group_brand[(row["query_group"], row["brand"])].append(row)
        by_engine_group_brand[(row["engine"], row["query_group"], row["brand"])].append(row)

    def summarize(rows: list[dict[str, Any]], extra: dict[str, str]) -> dict[str, Any]:
        total = len(rows)
        included = sum(1 for row in rows if row["mentioned"])
        selected = sum(1 for row in rows if row["selected"])
        absorbed = sum(1 for row in rows if row["absorbed"])
        orders = [int(row["brand_order"]) for row in rows if row.get("brand_order")]
        low, high = wilson_interval(included, total)
        return {
            **extra,
            "runs": total,
            "included_runs": included,
            "inclusion_rate": round(included / total, 4) if total else 0,
            "inclusion_ci_low": round(low, 4),
            "inclusion_ci_high": round(high, 4),
            "selected_runs": selected,
            "selection_rate": round(selected / total, 4) if total else 0,
            "absorbed_runs": absorbed,
            "absorption_rate": round(absorbed / total, 4) if total else 0,
            "avg_brand_order": round(sum(orders) / len(orders), 2) if orders else "",
        }

    brand_scores = [summarize(rows, {"brand": brand}) for brand, rows in sorted(by_brand.items())]
    engine_scores = [
        summarize(rows, {"engine": engine, "brand": brand})
        for (engine, brand), rows in sorted(by_engine_brand.items())
    ]
    group_scores = [
        summarize(rows, {"query_group": query_group, "brand": brand})
        for (query_group, brand), rows in sorted(by_group_brand.items())
    ]
    engine_group_scores = [
        summarize(rows, {"engine": engine, "query_group": query_group, "brand": brand})
        for (engine, query_group, brand), rows in sorted(by_engine_group_brand.items())
    ]
    return brand_scores, engine_scores, group_scores, engine_group_scores


def score_file(input_path: str | Path, output_dir: str | Path) -> None:
    records = read_jsonl(input_path)
    brands = load_competitors()
    source_domains = load_source_domains()
    output = ensure_dir(output_dir)

    mentions: list[dict[str, Any]] = []
    absorptions: list[dict[str, Any]] = []
    citations: list[dict[str, Any]] = []
    for record in records:
        mentions.extend(extract_brand_mentions(record, brands))
        absorptions.extend(
            extract_brand_absorption(record, brands, source_domains["absorption_markers"])
        )
        citations.extend(extract_citations(record, brands, source_domains["gatekeeper_domains"]))

    brand_visibility = build_brand_visibility(mentions, absorptions, citations)
    brand_scores, engine_scores, group_scores, engine_group_scores = score_visibility(brand_visibility)
    source_scores = domain_share(citations)
    gatekeeper_scores = gatekeeper_share(citations)
    gatekeeper_totals = gatekeeper_summary(citations)

    write_csv(
        output / "mentions.csv",
        mentions,
        fieldnames=[
            "run_id",
            "query_id",
            "query_group",
            "vertical",
            "engine",
            "repetition",
            "brand",
            "mentioned",
            "brand_order",
            "mention_count",
        ],
    )
    write_csv(
        output / "brand_absorption.csv",
        absorptions,
        fieldnames=[
            "run_id",
            "query_id",
            "query_group",
            "vertical",
            "engine",
            "repetition",
            "brand",
            "absorbed",
            "absorption_count",
            "absorption_evidence",
            "alias_absorption_count",
            "marker_absorption_count",
        ],
    )
    write_csv(
        output / "brand_visibility.csv",
        brand_visibility,
        fieldnames=[
            "run_id",
            "query_id",
            "query_group",
            "vertical",
            "engine",
            "repetition",
            "brand",
            "mentioned",
            "selected",
            "absorbed",
            "brand_order",
            "mention_count",
            "absorption_count",
            "absorption_evidence",
            "alias_absorption_count",
            "marker_absorption_count",
        ],
    )
    write_csv(
        output / "citations.csv",
        citations,
        fieldnames=[
            "run_id",
            "query_id",
            "query_group",
            "vertical",
            "engine",
            "repetition",
            "url",
            "domain",
            "title",
            "cited_brand",
            "is_gatekeeper",
            "gatekeeper_domain",
            "citation_index",
        ],
    )
    score_fieldnames = [
        "brand",
        "runs",
        "included_runs",
        "inclusion_rate",
        "inclusion_ci_low",
        "inclusion_ci_high",
        "selected_runs",
        "selection_rate",
        "absorbed_runs",
        "absorption_rate",
        "avg_brand_order",
    ]
    write_csv(
        output / "brand_scores.csv",
        brand_scores,
        fieldnames=score_fieldnames,
    )
    write_csv(
        output / "engine_brand_scores.csv",
        engine_scores,
        fieldnames=["engine", *score_fieldnames],
    )
    write_csv(
        output / "group_brand_scores.csv",
        group_scores,
        fieldnames=["query_group", *score_fieldnames],
    )
    write_csv(
        output / "engine_group_brand_scores.csv",
        engine_group_scores,
        fieldnames=["engine", "query_group", *score_fieldnames],
    )
    write_csv(
        output / "source_domain_share.csv",
        source_scores,
        fieldnames=["domain", "citation_count", "share", "is_gatekeeper"],
    )
    write_csv(
        output / "gatekeeper_domain_share.csv",
        gatekeeper_scores,
        fieldnames=[
            "gatekeeper_domain",
            "citation_count",
            "share_of_all_citations",
            "share_of_gatekeeper_citations",
        ],
    )
    write_csv(
        output / "gatekeeper_summary.csv",
        gatekeeper_totals,
        fieldnames=[
            "total_citations",
            "gatekeeper_citations",
            "gatekeeper_citation_share",
        ],
    )
    print(f"Scored {len(records)} runs into {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Score Retell AEO citation runs.")
    parser.add_argument("--input", default="outputs/latest/raw_runs.jsonl")
    parser.add_argument("--output", default="outputs/latest")
    args = parser.parse_args()
    score_file(args.input, args.output)


if __name__ == "__main__":
    main()
