"""
Research Area Ranking Tool
==========================
Queries OpenAlex for 10 candidate research directions,
computes publication volume, citation impact, and growth metrics,
and produces a data-driven ranking.

Usage:
    python main.py
"""

import sys
import time

from fetch_openalex import fetch_all_areas
from analyse import analyse_all, print_summary
from visualise import generate_all_charts
from export import export_to_excel


def main():
    print("=" * 60)
    print("RESEARCH AREA RANKING TOOL")
    print("Data source: OpenAlex (2024–2025)")
    print("Paper types: journal articles + conference proceedings")
    print("=" * 60)

    # Phase 1: Fetch data
    start = time.time()
    print("\n[Phase 1] Fetching papers from OpenAlex...")
    area_papers = fetch_all_areas()
    fetch_time = time.time() - start
    print(f"\nFetch complete in {fetch_time:.1f}s")

    total_papers = sum(len(p) for p in area_papers.values())
    print(f"Total unique papers across all areas: {total_papers}")

    # Phase 2: Analyse
    print("\n[Phase 2] Computing metrics and ranking...")
    df, top10_data = analyse_all(area_papers)
    print_summary(df, top10_data)

    # Phase 3: Visualise
    print("\n[Phase 3] Generating charts...")
    generate_all_charts(df)

    # Phase 4: Export
    print("\n[Phase 4] Exporting to Excel...")
    filepath = export_to_excel(df, top10_data, area_papers)

    print("\n" + "=" * 60)
    print("DONE!")
    print(f"Results saved to: output/")
    print(f"  - research_area_ranking.xlsx")
    print(f"  - 01_paper_counts.png")
    print(f"  - 02_citation_impact.png")
    print(f"  - 03_growth_rate.png")
    print(f"  - 04_volume_vs_impact.png")
    print(f"  - 05_composite_ranking.png")
    print("=" * 60)


if __name__ == "__main__":
    main()
