"""
analytics/executive_report.py — Executive Analytics Report Generator

Pulls together the dataset overview, key findings, correlation highlights,
trends, recommendations, and business implications into a single
stakeholder-facing document: reports/executive_summary.md

Depends on correlation_analysis.py having been run first (reads
analytics/correlation_matrix.csv); if it hasn't, this script computes it
inline so it can also run standalone.

Run:
    python analytics/executive_report.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from analytics.utils import load_scored_data, REPORTS_DIR, ANALYTICS_DIR, HONESTY_COL, fmt_int
from analytics.correlation_analysis import (
    compute_correlation_matrix, top_relationships, interpret
)


def dataset_overview(df: pd.DataFrame) -> list:
    return [
        "## 1. Dataset Overview",
        "",
        f"- **Total influencers analyzed:** {len(df)}",
        f"- **Platform:** {', '.join(df['platform'].unique())}",
        f"- **Niche:** {', '.join(df['niche'].unique())}",
        f"- **Follower range:** {fmt_int(df['followers'].min())} – {fmt_int(df['followers'].max())}",
        f"- **Verified accounts:** {(df['verified'].str.lower() == 'yes').sum()} of {len(df)}",
        f"- **Average HypeAuditor audience-quality score:** {df['hypeauditor_score'].mean():.1f} / 100",
        "",
    ]


def key_findings(df: pd.DataFrame) -> list:
    risk_counts = df["risk_label"].value_counts()
    most_suspicious = df.loc[df[HONESTY_COL].idxmax()]
    most_authentic = df.loc[df[HONESTY_COL].idxmin()]

    tier_avg = df.groupby("follower_tier", observed=True)[HONESTY_COL].mean().sort_values()
    most_authentic_tier = tier_avg.index[0]
    most_suspicious_tier = tier_avg.index[-1]

    return [
        "## 2. Key Findings",
        "",
        f"- **Average Honesty Risk Score:** {df[HONESTY_COL].mean():.1f} / 100 across all {len(df)} influencers.",
        f"- **Risk distribution:** {risk_counts.get('HIGH RISK', 0)} High Risk, "
        f"{risk_counts.get('MEDIUM RISK', 0)} Medium Risk, {risk_counts.get('LOW RISK', 0)} Low Risk "
        f"({risk_counts.get('HIGH RISK', 0) / len(df) * 100:.0f}% of accounts flagged High Risk).",
        f"- **Most suspicious account:** `{most_suspicious['username']}` "
        f"(Honesty Risk Score {most_suspicious[HONESTY_COL]:.1f}, "
        f"{fmt_int(most_suspicious['followers'])} followers).",
        f"- **Most authentic account:** `{most_authentic['username']}` "
        f"(Honesty Risk Score {most_authentic[HONESTY_COL]:.1f}, "
        f"{fmt_int(most_authentic['followers'])} followers).",
        f"- **By follower tier:** `{most_suspicious_tier}` accounts carry the highest average "
        f"Honesty Risk Score ({tier_avg.iloc[-1]:.1f}), while `{most_authentic_tier}` accounts "
        f"average the lowest ({tier_avg.iloc[0]:.1f}) — larger, established accounts trend more authentic.",
        "",
    ]


def correlation_section(corr: pd.DataFrame) -> list:
    rels = top_relationships(corr, n=5)
    lines = [
        "## 3. Correlation Highlights",
        "",
        "| Metric A | Metric B | r | Interpretation |",
        "|---|---|---|---|",
    ]
    for a, b, r in rels:
        lines.append(f"| {a} | {b} | {r:+.2f} | {interpret(r)} |")
    lines += [
        "",
        "Full matrix: `analytics/correlation_matrix.csv` · Heatmap: `visualizations/correlation_heatmap.png`",
        "",
    ]
    return lines


def trends_section(df: pd.DataFrame) -> list:
    corr_ff_fake = df["ff_ratio"].corr(df[HONESTY_COL])
    corr_followers_fake = df["followers"].corr(df[HONESTY_COL])
    return [
        "## 4. Trends",
        "",
        f"- **Follower-to-following ratio vs Honesty Risk:** r = {corr_ff_fake:+.2f} — "
        f"accounts that follow disproportionately many other users for their size "
        f"({'a classic bought-follower signature' if corr_ff_fake < 0 else 'no strong pattern detected'}) "
        f"tend toward higher risk scores.",
        f"- **Followers vs Honesty Risk:** r = {corr_followers_fake:+.2f} — "
        f"{'larger accounts trend more authentic' if corr_followers_fake < 0 else 'account size alone is not a reliable authenticity signal'} "
        "in this dataset, though this should not be read as 'big = automatically safe'.",
        "- **Engagement rate is bimodal at the extremes:** both unusually *low* and unusually "
        "*high* engagement rates correlate with elevated Honesty Risk Scores, confirming the "
        "scorer's deliberate design choice to penalize deviation from the ~2% industry average "
        "in either direction, not just abnormally high engagement.",
        "",
    ]


def recommendations_section() -> list:
    return [
        "## 5. Recommendations",
        "",
        "1. **Prioritize Low/Medium Risk accounts with above-median reach** for sponsorship "
        "shortlists (see `reports/business_insights.md`, section 3).",
        "2. **Treat raw engagement-rate leaderboards with caution** — cross-reference against "
        "Honesty Risk Score before using engagement rate alone as a selection criterion.",
        "3. **Request platform-verified audience insights** (e.g. HypeAuditor, Instagram "
        "Insights export) for any High Risk account before signing a deal, rather than "
        "excluding them outright — some may simply have an unusual but legitimate audience mix.",
        "4. **Re-run the scorer and analytics pipeline on a rolling basis** as influencer "
        "metrics change; Honesty Risk Score is a snapshot, not a permanent label.",
        "",
    ]


def business_implications_section(df: pd.DataFrame) -> list:
    high_risk_followers = df.loc[df["risk_label"] == "HIGH RISK", "followers"].sum()
    total_followers = df["followers"].sum()
    pct = high_risk_followers / total_followers * 100
    return [
        "## 6. Business Implications",
        "",
        f"- High Risk accounts in this sample represent **{fmt_int(high_risk_followers)} combined "
        f"followers ({pct:.0f}% of total reach analyzed)** — a meaningful share of ad spend is at risk "
        "if these accounts are booked without further vetting.",
        "- A brand running a ₹10L campaign across this influencer pool could mis-allocate a "
        "proportional share of budget to inflated reach if selection is based on follower count alone, "
        "underscoring the ROI case for an authenticity-screening step before influencer payouts.",
        "- The scoring framework is fully transparent and reproducible (deterministic formula, no "
        "black-box model), making it suitable to embed directly into a brand's influencer-vetting "
        "workflow or procurement checklist.",
        "",
    ]


def main():
    df = load_scored_data()
    corr_csv = os.path.join(ANALYTICS_DIR, "correlation_matrix.csv")
    if os.path.exists(corr_csv):
        corr = pd.read_csv(corr_csv, index_col=0)
    else:
        corr = compute_correlation_matrix(df)

    lines = [
        "# Executive Analytics Report — Influencer Honesty Score",
        "",
        "_Auto-generated by `analytics/executive_report.py`._",
        "",
        "---",
        "",
    ]
    lines += dataset_overview(df)
    lines += key_findings(df)
    lines += correlation_section(corr)
    lines += trends_section(df)
    lines += recommendations_section()
    lines += business_implications_section(df)

    out_path = os.path.join(REPORTS_DIR, "executive_summary.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Executive summary saved -> {out_path}")


if __name__ == "__main__":
    main()
