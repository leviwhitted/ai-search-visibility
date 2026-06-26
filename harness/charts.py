from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from harness.storage import ensure_dir


def read_csv(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def try_matplotlib_chart(scores: list[dict[str, Any]], citations: list[dict[str, Any]], output: Path) -> bool:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    top_scores = sorted(scores, key=lambda row: float(row["inclusion_rate"]), reverse=True)
    brands = [row["brand"] for row in top_scores]
    rates = [float(row["inclusion_rate"]) for row in top_scores]

    plt.figure(figsize=(9, 5))
    plt.barh(brands, rates, color="#2f6f73")
    plt.xlabel("Inclusion rate")
    plt.title("Brand inclusion rate across sampled AI-answer runs")
    plt.xlim(0, 1)
    plt.tight_layout()
    plt.savefig(output / "inclusion_by_brand.png", dpi=160)
    plt.close()

    top_domains = citations[:10]
    domains = [row["domain"] for row in top_domains]
    counts = [int(row["citation_count"]) for row in top_domains]

    plt.figure(figsize=(9, 5))
    plt.barh(domains, counts, color="#7d5a3c")
    plt.xlabel("Citation count")
    plt.title("Top cited domains")
    plt.tight_layout()
    plt.savefig(output / "top_citation_domains.png", dpi=160)
    plt.close()
    return True


def svg_bar_chart(path: Path, title: str, labels: list[str], values: list[float], x_label: str) -> None:
    width = 920
    row_height = 34
    margin_left = 230
    margin_top = 56
    chart_width = 620
    height = margin_top + row_height * len(labels) + 48
    max_value = max(values) if values else 1
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="24" y="32" font-family="Arial" font-size="20" font-weight="700" fill="#1f2933">{title}</text>',
    ]
    for index, (label, value) in enumerate(zip(labels, values)):
        y = margin_top + index * row_height
        bar_width = int((value / max_value) * chart_width) if max_value else 0
        lines.append(f'<text x="24" y="{y + 20}" font-family="Arial" font-size="13" fill="#25313b">{label}</text>')
        lines.append(f'<rect x="{margin_left}" y="{y + 5}" width="{bar_width}" height="20" rx="2" fill="#2f6f73"/>')
        display = f"{value:.2f}" if value <= 1 else f"{int(value)}"
        lines.append(
            f'<text x="{margin_left + bar_width + 8}" y="{y + 20}" font-family="Arial" font-size="12" fill="#25313b">{display}</text>'
        )
    lines.append(f'<text x="{margin_left}" y="{height - 14}" font-family="Arial" font-size="12" fill="#56616b">{x_label}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def fallback_svg_charts(scores: list[dict[str, Any]], citations: list[dict[str, Any]], output: Path) -> None:
    top_scores = sorted(scores, key=lambda row: float(row["inclusion_rate"]), reverse=True)
    svg_bar_chart(
        output / "inclusion_by_brand.svg",
        "Brand inclusion rate across sampled AI-answer runs",
        [row["brand"] for row in top_scores],
        [float(row["inclusion_rate"]) for row in top_scores],
        "Inclusion rate",
    )
    top_domains = citations[:10]
    svg_bar_chart(
        output / "top_citation_domains.svg",
        "Top cited domains",
        [row["domain"] for row in top_domains],
        [float(row["citation_count"]) for row in top_domains],
        "Citation count",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate static Retell pilot charts.")
    parser.add_argument("--scores", default="outputs/latest/brand_scores.csv")
    parser.add_argument("--citations", default="outputs/latest/source_domain_share.csv")
    parser.add_argument("--output", default="outputs/latest/charts")
    args = parser.parse_args()

    output = ensure_dir(args.output)
    scores = read_csv(args.scores)
    citations = read_csv(args.citations)
    if try_matplotlib_chart(scores, citations, output):
        print(f"Wrote matplotlib PNG charts to {output}")
    else:
        fallback_svg_charts(scores, citations, output)
        print(f"matplotlib not installed; wrote SVG fallback charts to {output}")


if __name__ == "__main__":
    main()
