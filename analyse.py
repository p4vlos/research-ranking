"""
Analyse fetched papers and compute ranking metrics.
"""

import numpy as np
import pandas as pd

from config import RESEARCH_AREAS, WEIGHTS


def compute_area_metrics(area_id: str, papers: list[dict], area_config: dict) -> dict:
    """Compute all metrics for a single research area."""
    if not papers:
        return {
            "area_id": area_id,
            "name": area_config["name"],
            "short": area_config["short"],
            "paper_count": 0,
            "papers_2024": 0,
            "papers_2025": 0,
            "growth_rate": 0.0,
            "total_citations": 0,
            "mean_citations": 0.0,
            "median_citations": 0.0,
            "max_citations": 0,
            "top10_mean": 0.0,
            "top10_papers": [],
        }

    df = pd.DataFrame(papers)
    citations = df["citations"].values

    papers_2024 = len(df[df["year"] == 2024])
    papers_2025 = len(df[df["year"] == 2025])

    # Growth rate: handle division by zero
    if papers_2024 > 0:
        # Annualise 2025 count (we're ~3 months in, so scale up)
        # Actually, OpenAlex indexes with some delay, so 2025 papers
        # are those already indexed. We'll compare raw counts but note
        # that 2025 is partial.
        growth_rate = ((papers_2025 / papers_2024) - 1) * 100
    else:
        growth_rate = 100.0 if papers_2025 > 0 else 0.0

    # Top-10 most cited
    top_indices = np.argsort(citations)[::-1][:10]
    top10_papers = []
    for idx in top_indices:
        row = df.iloc[idx]
        top10_papers.append({
            "title": row["title"],
            "citations": int(row["citations"]),
            "year": int(row["year"]) if pd.notna(row["year"]) else 0,
            "venue": row["venue"],
            "first_author": row["first_author"],
        })

    top10_citations = citations[top_indices]
    top10_mean = float(np.mean(top10_citations)) if len(top10_citations) > 0 else 0.0

    return {
        "area_id": area_id,
        "name": area_config["name"],
        "short": area_config["short"],
        "paper_count": len(papers),
        "papers_2024": papers_2024,
        "papers_2025": papers_2025,
        "growth_rate": round(growth_rate, 1),
        "total_citations": int(np.sum(citations)),
        "mean_citations": round(float(np.mean(citations)), 2),
        "median_citations": round(float(np.median(citations)), 1),
        "max_citations": int(np.max(citations)),
        "top10_mean": round(top10_mean, 1),
        "top10_papers": top10_papers,
    }


def normalise_column(series: pd.Series) -> pd.Series:
    """Min-max normalise a pandas Series to [0, 1]."""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - min_val) / (max_val - min_val)


def compute_composite_score(df: pd.DataFrame) -> pd.Series:
    """
    Compute weighted composite score from normalised metrics.
    Higher = more attractive research area.
    """
    norm_count = normalise_column(df["paper_count"])
    norm_citations = normalise_column(df["mean_citations"])

    # For growth rate, clamp extreme negatives and normalise
    growth_clamped = df["growth_rate"].clip(lower=-50)
    norm_growth = normalise_column(growth_clamped)

    score = (
        WEIGHTS["paper_count"] * norm_count
        + WEIGHTS["mean_citations"] * norm_citations
        + WEIGHTS["growth_rate"] * norm_growth
    )
    return round(score, 3)


def analyse_all(area_papers: dict[str, list[dict]]) -> pd.DataFrame:
    """
    Compute metrics for all areas and return a ranked DataFrame.
    """
    # Build lookup for area configs
    config_map = {a["id"]: a for a in RESEARCH_AREAS}

    metrics_list = []
    top10_data = {}

    for area_id, papers in area_papers.items():
        config = config_map[area_id]
        metrics = compute_area_metrics(area_id, papers, config)
        top10_data[area_id] = metrics.pop("top10_papers")
        metrics_list.append(metrics)

    df = pd.DataFrame(metrics_list)

    # Compute composite score
    df["composite_score"] = compute_composite_score(df)

    # Rank by composite score (1 = best)
    df["rank"] = df["composite_score"].rank(ascending=False, method="min").astype(int)

    # Sort by rank
    df = df.sort_values("rank").reset_index(drop=True)

    return df, top10_data


def print_summary(df: pd.DataFrame, top10_data: dict):
    """Print a readable summary of the ranking."""
    print("\n" + "=" * 80)
    print("RESEARCH AREA RANKING (2024-2025)")
    print("=" * 80)

    display_cols = [
        "rank", "short", "paper_count", "papers_2024", "papers_2025",
        "growth_rate", "mean_citations", "median_citations",
        "max_citations", "top10_mean", "composite_score"
    ]
    print(df[display_cols].to_string(index=False))

    print("\n" + "-" * 80)
    print("TOP-3 MOST CITED PAPERS PER AREA")
    print("-" * 80)

    for _, row in df.iterrows():
        area_id = row["area_id"]
        print(f"\n  [{row['rank']}] {row['name']}")
        papers = top10_data.get(area_id, [])[:3]
        for i, p in enumerate(papers, 1):
            title = (p["title"][:70] + "...") if p["title"] and len(p["title"]) > 70 else p["title"]
            print(f"      {i}. [{p['citations']} cit] {title}")
            print(f"         {p['venue']} ({p['year']})")
