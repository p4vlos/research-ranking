"""
Fetch papers from OpenAlex API with caching and pagination.
"""

import json
import os
import time
from pathlib import Path

import requests
from tqdm import tqdm

from config import MAILTO, YEARS, WORK_TYPES, MAX_PAGES_PER_QUERY, RESEARCH_AREAS

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

BASE_URL = "https://api.openalex.org/works"


def build_filter_string():
    """Build the OpenAlex filter for year range and work types."""
    year_min, year_max = min(YEARS), max(YEARS)
    types_str = "|".join(WORK_TYPES)
    return f"publication_year:{year_min}-{year_max},type:{types_str}"


def fetch_query(query: str, area_id: str, query_idx: int) -> list[dict]:
    """
    Fetch all papers matching a keyword query from OpenAlex.
    Uses cursor-based pagination to get all results.
    Caches results to disk.
    """
    cache_file = CACHE_DIR / f"{area_id}_q{query_idx}.json"

    if cache_file.exists():
        with open(cache_file) as f:
            cached = json.load(f)
        print(f"  [cache] Loaded {len(cached)} papers for '{query}'")
        return cached

    all_works = []
    cursor = "*"
    page = 0
    filter_str = build_filter_string()

    while cursor and page < MAX_PAGES_PER_QUERY:
        params = {
            "search": query,
            "filter": filter_str,
            "sort": "cited_by_count:desc",
            "per_page": 200,
            "cursor": cursor,
            "mailto": MAILTO,
            "select": (
                "id,title,publication_year,publication_date,"
                "cited_by_count,type,doi,"
                "primary_location,authorships"
            ),
        }

        try:
            resp = requests.get(BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"  [error] API request failed: {e}")
            break

        results = data.get("results", [])
        if not results:
            break

        # Extract relevant fields
        for work in results:
            paper = {
                "openalex_id": work.get("id", ""),
                "title": work.get("title", ""),
                "year": work.get("publication_year"),
                "date": work.get("publication_date", ""),
                "citations": work.get("cited_by_count", 0),
                "type": work.get("type", ""),
                "doi": work.get("doi", ""),
                "venue": "",
                "first_author": "",
            }
            # Extract venue
            loc = work.get("primary_location") or {}
            source = loc.get("source") or {}
            paper["venue"] = source.get("display_name", "")

            # Extract first author
            authorships = work.get("authorships", [])
            if authorships:
                author_info = authorships[0].get("author", {})
                paper["first_author"] = author_info.get("display_name", "")

            all_works.append(paper)

        # Get next cursor
        meta = data.get("meta", {})
        cursor = meta.get("next_cursor")
        page += 1

        # Polite rate limiting
        time.sleep(0.15)

    # Cache results
    with open(cache_file, "w") as f:
        json.dump(all_works, f)

    print(f"  [fetch] Got {len(all_works)} papers for '{query}'")
    return all_works


def fetch_all_areas() -> dict[str, list[dict]]:
    """
    Fetch papers for all research areas.
    Returns dict: area_id -> list of deduplicated papers.
    """
    area_papers = {}

    for area in tqdm(RESEARCH_AREAS, desc="Fetching areas"):
        area_id = area["id"]
        area_name = area["name"]
        print(f"\n{'='*60}")
        print(f"Fetching: {area_name}")
        print(f"{'='*60}")

        all_papers = []
        seen_ids = set()

        for idx, query in enumerate(area["queries"]):
            papers = fetch_query(query, area_id, idx)
            for p in papers:
                pid = p["openalex_id"]
                if pid not in seen_ids:
                    seen_ids.add(pid)
                    all_papers.append(p)

        print(f"  => {len(all_papers)} unique papers after dedup")
        area_papers[area_id] = all_papers

    return area_papers


if __name__ == "__main__":
    results = fetch_all_areas()
    for area_id, papers in results.items():
        print(f"{area_id}: {len(papers)} papers")
