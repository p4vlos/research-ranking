# Research Area Ranking Tool

Queries the OpenAlex API for 10 candidate research directions,
retrieves publication counts and citation data (2024–2025),
and produces a data-driven ranking with charts and Excel export.

## Quick Start

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python main.py
```

The tool will:
1. Fetch papers from OpenAlex (~5–20 min depending on result counts)
2. Cache all results to `cache/` (re-runs skip fetching)
3. Compute metrics and rank the 10 areas
4. Generate 5 charts to `output/`
5. Export an Excel spreadsheet to `output/research_area_ranking.xlsx`

## Customisation

### Adjust research areas or keywords
Edit `config.py` → `RESEARCH_AREAS` list. Each area has:
- `id`: unique identifier
- `name`: full display name
- `short`: short label for charts
- `queries`: list of 2–3 keyword search strings

### Adjust ranking weights
Edit `config.py` → `WEIGHTS` dict:
- `paper_count`: weight for publication volume (default 0.33)
- `mean_citations`: weight for citation impact (default 0.33)
- `growth_rate`: weight for year-over-year growth (default 0.34)

### Change year range
Edit `config.py` → `YEARS` list (e.g., `[2023, 2024, 2025]`)

### Re-run without re-fetching
Cached JSON files in `cache/` are reused automatically.
Delete the cache folder to force a fresh fetch.

## Output Files

| File | Description |
|------|-------------|
| `output/research_area_ranking.xlsx` | Full ranking with summary, top-10 papers per area, and all papers |
| `output/01_paper_counts.png` | Stacked bar: 2024 vs 2025 paper counts |
| `output/02_citation_impact.png` | Mean citations per paper by area |
| `output/03_growth_rate.png` | Year-over-year publication growth |
| `output/04_volume_vs_impact.png` | Scatter: volume vs. impact landscape |
| `output/05_composite_ranking.png` | Final composite score ranking |

## Notes

- **OpenAlex is free** — no API key needed. Adding your email in
  `config.py` → `MAILTO` gives you higher rate limits (polite pool).
- **2025 data is partial** — papers indexed so far. Growth rate
  comparisons should account for this.
- **Citation counts favour older papers** — a 2024 paper has had
  more time to accumulate citations than a 2025 paper.
- **Keyword queries are approximate** — you may want to iterate
  on queries after the first run to improve coverage.
