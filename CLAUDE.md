# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research area ranking tool that queries the OpenAlex API to evaluate and rank 10 candidate research directions in wearable health technology and machine learning. It scores areas by publication volume, citation impact, and year-over-year growth, then produces charts and an Excel report.

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

Runtime is 5–20 minutes due to API pagination. No API key is needed (OpenAlex is free). The `MAILTO` in `config.py` enables higher rate limits via OpenAlex's polite pool.

There are no tests, linting, or build commands.

## Architecture

Four-phase pipeline orchestrated by `main.py`:

1. **Fetch** (`fetch_openalex.py`) — Queries OpenAlex API with cursor-based pagination for each research area. Caches raw JSON responses in `cache/`. Deduplicates papers by OpenAlex ID.
2. **Analyse** (`analyse.py`) — Computes per-area metrics (paper counts, citation stats, growth rate) and a composite score via min-max normalized weighted average.
3. **Visualise** (`visualise.py`) — Generates 5 PNG charts (bar, scatter, ranking) to `output/`.
4. **Export** (`export.py`) — Creates a multi-sheet Excel workbook (`output/research_area_ranking.xlsx`) with formatted headers, medal-colored top-3 rows, and auto-width columns.

`config.py` is the central configuration hub: research area definitions (id, label, OpenAlex query), year range, work types, composite score weights, and pagination limits.

## Key Data Flow

`fetch_all_areas()` returns `dict[area_id → list[paper_dict]]` → `analyse_all()` produces `(DataFrame, top10_data)` → both consumed by `generate_all_charts(df)` and `export_to_excel(df, top10_data, area_papers)`.

## Customisation

- **Research areas**: Edit the `RESEARCH_AREAS` list in `config.py` (each entry has `id`, `label`, `queries` with OpenAlex filter syntax).
- **Ranking weights**: Adjust `WEIGHTS` dict in `config.py` (keys: `paper_count`, `mean_citations`, `growth_rate`; should sum to ~1.0).
- **Year range**: Change `YEARS` list in `config.py`.
- **Fetch depth**: `MAX_PAGES_PER_QUERY` controls pagination (each page = 200 results).
