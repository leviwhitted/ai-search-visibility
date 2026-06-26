from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = PROJECT_ROOT / file_path
    with file_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {file_path}")
    return data


def load_queries(path: str | Path = "queries.yaml") -> tuple[list[dict[str, Any]], dict[str, str]]:
    data = load_yaml(path)
    queries = data.get("queries", [])
    if not isinstance(queries, list) or not queries:
        raise ValueError("queries.yaml must contain a non-empty queries list")
    geo = data.get("geo", {}) or {}
    return queries, geo


def load_competitors(path: str | Path = "competitors.yaml") -> list[dict[str, Any]]:
    data = load_yaml(path)
    brands: list[dict[str, Any]] = []
    primary = data.get("primary_brand")
    if not isinstance(primary, dict):
        raise ValueError("competitors.yaml must contain primary_brand")
    primary["is_primary"] = True
    brands.append(primary)
    for competitor in data.get("competitors", []):
        competitor["is_primary"] = False
        brands.append(competitor)
    return brands


def load_source_domains(path: str | Path = "source_domains.yaml") -> dict[str, Any]:
    data = load_yaml(path)
    gatekeeper_domains = data.get("gatekeeper_domains", []) or []
    absorption_markers = data.get("absorption_markers", []) or []
    if not isinstance(gatekeeper_domains, list):
        raise ValueError("source_domains.yaml gatekeeper_domains must be a list")
    if not isinstance(absorption_markers, list):
        raise ValueError("source_domains.yaml absorption_markers must be a list")
    return {
        "gatekeeper_domains": [str(domain).lower().removeprefix("www.") for domain in gatekeeper_domains],
        "absorption_markers": [str(marker) for marker in absorption_markers],
    }
