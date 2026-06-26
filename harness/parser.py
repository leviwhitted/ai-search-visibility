from __future__ import annotations

import re
from collections import Counter
from typing import Any
from urllib.parse import urlparse


def normalize_domain(url: str) -> str:
    url = (url or "").strip()
    parsed = urlparse(url if "://" in url else f"https://{url}")
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def domain_matches(domain: str, known_domain: str) -> bool:
    return domain == known_domain or domain.endswith("." + known_domain)


def find_text_markers(text: str, markers: list[str]) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for marker in markers:
        marker_text = str(marker)
        if not marker_text:
            continue
        pattern = re.compile(rf"(?<![a-z0-9]){re.escape(marker_text.lower())}(?![a-z0-9])")
        if pattern.search(lowered):
            found.append(marker_text)
    return found


def extract_brand_mentions(record: dict[str, Any], brands: list[dict[str, Any]]) -> list[dict[str, Any]]:
    text = record.get("answer_text", "") or ""
    lowered = text.lower()
    first_positions: list[tuple[int, str]] = []
    mention_counts: dict[str, int] = {}

    for brand in brands:
        name = brand["name"]
        aliases = brand.get("aliases", [name])
        positions: list[int] = []
        count = 0
        for alias in aliases:
            pattern = re.compile(rf"(?<![a-z0-9]){re.escape(alias.lower())}(?![a-z0-9])")
            matches = list(pattern.finditer(lowered))
            count += len(matches)
            positions.extend(match.start() for match in matches)
        mention_counts[name] = count
        if positions:
            first_positions.append((min(positions), name))

    ordered = {name: index + 1 for index, (_, name) in enumerate(sorted(first_positions))}
    rows: list[dict[str, Any]] = []
    for brand in brands:
        name = brand["name"]
        rows.append(
            {
                "run_id": record["run_id"],
                "query_id": record["query_id"],
                "query_group": record["query_group"],
                "vertical": record.get("vertical", ""),
                "engine": record["engine"],
                "repetition": record["repetition"],
                "brand": name,
                "mentioned": mention_counts[name] > 0,
                "brand_order": ordered.get(name),
                "mention_count": mention_counts[name],
            }
        )
    return rows


def extract_brand_absorption(
    record: dict[str, Any],
    brands: list[dict[str, Any]],
    absorption_markers: list[str] | None = None,
) -> list[dict[str, Any]]:
    text = record.get("answer_text", "") or ""
    rows: list[dict[str, Any]] = []
    absorption_markers = absorption_markers or []

    for brand in brands:
        name = brand["name"]
        alias_hits = find_text_markers(text, brand.get("aliases", [name]))
        marker_hits = find_text_markers(text, absorption_markers) if brand.get("is_primary") else []
        evidence = sorted(set(alias_hits + marker_hits), key=str.lower)
        rows.append(
            {
                "run_id": record["run_id"],
                "query_id": record["query_id"],
                "query_group": record["query_group"],
                "vertical": record.get("vertical", ""),
                "engine": record["engine"],
                "repetition": record["repetition"],
                "brand": name,
                "absorbed": bool(evidence),
                "absorption_count": len(evidence),
                "absorption_evidence": " | ".join(evidence),
                "alias_absorption_count": len(alias_hits),
                "marker_absorption_count": len(marker_hits),
            }
        )
    return rows


def extract_citations(
    record: dict[str, Any],
    brands: list[dict[str, Any]],
    gatekeeper_domains: list[str] | None = None,
) -> list[dict[str, Any]]:
    domain_to_brand = {}
    for brand in brands:
        for domain in brand.get("domains", []):
            domain_to_brand[domain.lower().removeprefix("www.")] = brand["name"]
    gatekeepers = [domain.lower().removeprefix("www.") for domain in (gatekeeper_domains or [])]

    rows: list[dict[str, Any]] = []
    for index, citation in enumerate(record.get("citations", []), start=1):
        url = citation.get("url", "")
        domain = normalize_domain(url)
        cited_brand = None
        for known_domain, brand_name in domain_to_brand.items():
            if domain_matches(domain, known_domain):
                cited_brand = brand_name
                break
        matched_gatekeeper = ""
        for gatekeeper_domain in gatekeepers:
            if domain_matches(domain, gatekeeper_domain):
                matched_gatekeeper = gatekeeper_domain
                break
        rows.append(
            {
                "run_id": record["run_id"],
                "query_id": record["query_id"],
                "query_group": record["query_group"],
                "vertical": record.get("vertical", ""),
                "engine": record["engine"],
                "repetition": record["repetition"],
                "url": url,
                "domain": domain,
                "title": citation.get("title", ""),
                "cited_brand": cited_brand or "",
                "is_gatekeeper": bool(matched_gatekeeper),
                "gatekeeper_domain": matched_gatekeeper,
                "citation_index": index,
            }
        )
    return rows


def domain_share(citations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(row["domain"] for row in citations if row.get("domain"))
    total = sum(counts.values()) or 1
    gatekeeper_domains = {
        row["domain"]: row.get("is_gatekeeper", False)
        for row in citations
        if row.get("domain")
    }
    return [
        {
            "domain": domain,
            "citation_count": count,
            "share": count / total,
            "is_gatekeeper": gatekeeper_domains.get(domain, False),
        }
        for domain, count in counts.most_common()
    ]


def gatekeeper_share(citations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total_citations = len(citations) or 1
    gatekeeper_rows = [row for row in citations if row.get("is_gatekeeper")]
    gatekeeper_total = len(gatekeeper_rows) or 1
    counts = Counter(row["gatekeeper_domain"] for row in gatekeeper_rows if row.get("gatekeeper_domain"))
    return [
        {
            "gatekeeper_domain": domain,
            "citation_count": count,
            "share_of_all_citations": count / total_citations,
            "share_of_gatekeeper_citations": count / gatekeeper_total,
        }
        for domain, count in counts.most_common()
    ]


def gatekeeper_summary(citations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total = len(citations)
    gatekeeper_count = sum(1 for row in citations if row.get("is_gatekeeper"))
    return [
        {
            "total_citations": total,
            "gatekeeper_citations": gatekeeper_count,
            "gatekeeper_citation_share": gatekeeper_count / total if total else 0,
        }
    ]
