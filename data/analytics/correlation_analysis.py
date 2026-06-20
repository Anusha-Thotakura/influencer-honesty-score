"""
analytics/correlation_analysis.py — Correlation Analysis Module

Computes a Pearson correlation matrix across the core engagement / honesty
metrics, saves it as a CSV (analytics/correlation_matrix.csv), renders a
heatmap (visualizations/correlation_heatmap.png), and writes a short
plain-English summary of the strongest relationships
(analytics/correlation_insights.md) that the other scripts (business
insights + executive report) reuse.

Run:
    python analytics/correlation_analysis.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from analytics.utils import (
    load_scored_data, CORRELATION_METRICS, VIS_DIR, ANALYTICS_DIR, HONESTY_COL
)

sns.set_theme(style="white", font_scale=0.9)


def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(CORRELATION_METRICS.keys())
    corr = df[cols].corr(method="pearson").round(3)
    corr = corr.rename(index=CORRELATION_METRICS, columns=CORRELATION_METRICS)
    return corr


def plot_heatmap(corr: pd.DataFrame, out_path: str):
    plt.figure(figsize=(9, 7))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        vmin=-1, vmax=1,
        center=0,
        square=True,
        linewidths=0.6,
        cbar_kws={"label": "Pearson Correlation Coefficient"},
    )
    plt.title("Correlation Heatmap — Influencer Engagement & Honesty Metrics", fontsize=13, pad=14)
    plt.xticks(rotation=40, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def top_relationships(corr: pd.DataFrame, n=5):
    """Return the n strongest (non self) correlation pairs, sorted by |r|."""
    pairs = []
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            r = corr.iloc[i, j]
            pairs.append((cols[i], cols[j], r))
    pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    return pairs[:n]


def interpret(r: float) -> str:
    a = abs(r)
    direction = "positive" if r > 0 else "negative"
    if a >= 0.7:
        strength = "strong"
    elif a >= 0.4:
        strength = "moderate"
    elif a >= 0.2:
        strength = "weak"
    else:
        strength = "negligible"
    return f"{strength} {direction}"


def write_insights_md(corr: pd.DataFrame, out_path: str):
    rels = top_relationships(corr, n=6)
    lines = [
        "# Correlation Analysis — Key Relationships",
        "",
        "Auto-generated from `analytics/correlation_analysis.py`. Pearson correlation",
        "coefficients (r) range from -1 (perfect inverse relationship) to +1 (perfect",
        "direct relationship). `Honesty Risk Score` is the project's core 0-100 metric",
        "where **higher = more suspicious / less authentic**.",
        "",
        "## Strongest Relationships",
        "",
        "| Metric A | Metric B | Correlation (r) | Interpretation |",
        "|---|---|---|---|",
    ]
    for a, b, r in rels:
        lines.append(f"| {a} | {b} | {r:+.2f} | {interpret(r)} |")

    lines += [
        "",
        "## Full Correlation Matrix",
        "",
        corr.round(2).to_markdown(),
        "",
        "*(See `visualizations/correlation_heatmap.png` for the visual heatmap.)*",
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    df = load_scored_data()
    corr = compute_correlation_matrix(df)

    matrix_csv = os.path.join(ANALYTICS_DIR, "correlation_matrix.csv")
    corr.to_csv(matrix_csv)
    print(f"Correlation matrix saved -> {matrix_csv}")

    heatmap_png = os.path.join(VIS_DIR, "correlation_heatmap.png")
    plot_heatmap(corr, heatmap_png)
    print(f"Correlation heatmap saved -> {heatmap_png}")

    insights_md = os.path.join(ANALYTICS_DIR, "correlation_insights.md")
    write_insights_md(corr, insights_md)
    print(f"Correlation insights saved -> {insights_md}")

    print("\nTop relationships:")
    for a, b, r in top_relationships(corr, n=6):
        print(f"  {a:<20} <-> {b:<20}  r = {r:+.2f}  ({interpret(r)})")

    return corr


if __name__ == "__main__":
    main()
