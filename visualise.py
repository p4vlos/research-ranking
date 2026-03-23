"""
Generate charts for research area comparison.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Style
sns.set_theme(style="whitegrid", font_scale=1.1)
PALETTE = sns.color_palette("viridis", 10)


def chart_paper_counts(df: pd.DataFrame):
    """Stacked bar chart: 2024 vs 2025 paper counts per area."""
    fig, ax = plt.subplots(figsize=(14, 7))

    sorted_df = df.sort_values("paper_count", ascending=True)
    y_pos = range(len(sorted_df))

    bars_2024 = ax.barh(
        y_pos, sorted_df["papers_2024"], color="#2196F3",
        label="2024", edgecolor="white", linewidth=0.5
    )
    bars_2025 = ax.barh(
        y_pos, sorted_df["papers_2025"], left=sorted_df["papers_2024"],
        color="#FF9800", label="2025 (partial year)",
        edgecolor="white", linewidth=0.5
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_df["short"])
    ax.set_xlabel("Number of Peer-Reviewed Papers")
    ax.set_title("Publication Volume by Research Area (2024–2025)", fontweight="bold", pad=15)
    ax.legend(loc="lower right")

    # Add total count labels
    for i, (_, row) in enumerate(sorted_df.iterrows()):
        total = row["paper_count"]
        ax.text(total + max(df["paper_count"]) * 0.01, i, str(total),
                va="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    path = OUTPUT_DIR / "01_paper_counts.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def chart_citation_impact(df: pd.DataFrame):
    """Horizontal bar chart: mean citations per paper."""
    fig, ax = plt.subplots(figsize=(14, 7))

    sorted_df = df.sort_values("mean_citations", ascending=True)
    y_pos = range(len(sorted_df))

    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(sorted_df)))
    bars = ax.barh(y_pos, sorted_df["mean_citations"], color=colors,
                   edgecolor="white", linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_df["short"])
    ax.set_xlabel("Mean Citations per Paper")
    ax.set_title("Citation Impact by Research Area (2024–2025)", fontweight="bold", pad=15)

    for i, (_, row) in enumerate(sorted_df.iterrows()):
        val = row["mean_citations"]
        ax.text(val + max(df["mean_citations"]) * 0.02, i,
                f"{val:.1f}", va="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    path = OUTPUT_DIR / "02_citation_impact.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def chart_growth_rate(df: pd.DataFrame):
    """Bar chart: year-over-year growth rate."""
    fig, ax = plt.subplots(figsize=(14, 7))

    sorted_df = df.sort_values("growth_rate", ascending=True)
    y_pos = range(len(sorted_df))

    colors = ["#E53935" if v < 0 else "#43A047" for v in sorted_df["growth_rate"]]
    bars = ax.barh(y_pos, sorted_df["growth_rate"], color=colors,
                   edgecolor="white", linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_df["short"])
    ax.set_xlabel("Growth Rate (%): 2024 → 2025")
    ax.set_title("Publication Growth Rate by Research Area", fontweight="bold", pad=15)
    ax.axvline(x=0, color="black", linewidth=0.8, linestyle="-")

    for i, (_, row) in enumerate(sorted_df.iterrows()):
        val = row["growth_rate"]
        offset = max(abs(df["growth_rate"].max()), abs(df["growth_rate"].min())) * 0.02
        x_pos = val + offset if val >= 0 else val - offset
        ha = "left" if val >= 0 else "right"
        ax.text(x_pos, i, f"{val:+.1f}%", va="center", ha=ha,
                fontsize=9, fontweight="bold")

    plt.tight_layout()
    path = OUTPUT_DIR / "03_growth_rate.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def chart_scatter_volume_vs_impact(df: pd.DataFrame):
    """Scatter: paper count (x) vs mean citations (y), sized by growth."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Size by growth rate (clamped and shifted to positive)
    growth_shifted = df["growth_rate"].clip(lower=-50) + 60
    sizes = growth_shifted * 3

    scatter = ax.scatter(
        df["paper_count"], df["mean_citations"],
        s=sizes, c=df["composite_score"],
        cmap="RdYlGn", edgecolors="black", linewidth=0.8,
        alpha=0.85, zorder=5
    )

    # Labels
    for _, row in df.iterrows():
        ax.annotate(
            row["short"],
            (row["paper_count"], row["mean_citations"]),
            xytext=(8, 8), textcoords="offset points",
            fontsize=9, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor="gray", alpha=0.8)
        )

    ax.set_xlabel("Total Paper Count (2024–2025)")
    ax.set_ylabel("Mean Citations per Paper")
    ax.set_title(
        "Research Area Landscape: Volume vs. Impact\n"
        "(bubble size = growth rate, colour = composite score)",
        fontweight="bold", pad=15
    )

    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("Composite Score")

    plt.tight_layout()
    path = OUTPUT_DIR / "04_volume_vs_impact.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def chart_composite_ranking(df: pd.DataFrame):
    """Final composite score ranking with breakdown."""
    fig, ax = plt.subplots(figsize=(14, 7))

    sorted_df = df.sort_values("composite_score", ascending=True)
    y_pos = range(len(sorted_df))

    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(sorted_df)))
    bars = ax.barh(y_pos, sorted_df["composite_score"], color=colors,
                   edgecolor="white", linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"#{r} {s}" for r, s in
                        zip(sorted_df["rank"], sorted_df["short"])])
    ax.set_xlabel("Composite Score (0–1)")
    ax.set_title(
        "Overall Research Area Ranking\n"
        "(balanced: 33% volume + 33% citations + 34% growth)",
        fontweight="bold", pad=15
    )

    for i, (_, row) in enumerate(sorted_df.iterrows()):
        ax.text(row["composite_score"] + 0.01, i,
                f"{row['composite_score']:.3f}",
                va="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    path = OUTPUT_DIR / "05_composite_ranking.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def generate_all_charts(df: pd.DataFrame):
    """Generate all charts."""
    print("\nGenerating charts...")
    chart_paper_counts(df)
    chart_citation_impact(df)
    chart_growth_rate(df)
    chart_scatter_volume_vs_impact(df)
    chart_composite_ranking(df)
    print("All charts generated.")
