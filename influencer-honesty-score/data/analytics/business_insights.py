"""
analytics/business_insights.py — Business Insights Engine

Translates the raw scoring output into the kind of plain-English,
decision-ready insights a brand / marketing manager actually needs:
who's authentic, who's risky, who's worth a deal, and who to avoid.

All insights are deterministic — derived directly from the existing
fake_score / risk_label / engagement_rate columns produced by
src/scorer.py. No new scoring logic is introduced here.

Run:
    python analytics/business_insights.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from analytics.utils import load_scored_data, REPORTS_DIR, HONESTY_COL, fmt_int


def table(df: pd.DataFrame, cols: list, rename: dict = None) -> str:
    view = df[cols].copy()
    if rename:
        view = view.rename(columns=rename)
    return view.to_markdown(index=False)


def section_top_authentic(df):
    top = df.nsmallest(10, HONESTY_COL).sort_values(HONESTY_COL)
    return [
        "## 1. Top 10 Authentic Influencers",
        "",
        "Lowest Honesty Risk Score — strongest evidence of genuine, organic engagement.",
        "",
        table(top, ["rank", "username", "followers", "engagement_rate", HONESTY_COL, "risk_label"],
              {"rank": "Rank", "username": "Username", "followers": "Followers",
               "engagement_rate": "Engagement %", HONESTY_COL: "Honesty Risk Score", "risk_label": "Risk"}),
        "",
    ]


def section_top_suspicious(df):
    bottom = df.nlargest(10, HONESTY_COL).sort_values(HONESTY_COL, ascending=False)
    return [
        "## 2. Top 10 Suspicious Influencers",
        "",
        "Highest Honesty Risk Score — strongest indicators of bought followers / bot engagement.",
        "",
        table(bottom, ["rank", "username", "followers", "engagement_rate", HONESTY_COL, "risk_label"],
              {"rank": "Rank", "username": "Username", "followers": "Followers",
               "engagement_rate": "Engagement %", HONESTY_COL: "Honesty Risk Score", "risk_label": "Risk"}),
        "",
    ]


def section_brand_deals(df):
    """
    Best for brand deals = reasonable reach (above-median followers) AND
    authentic engagement (below-median Honesty Risk Score). This is a simple,
    transparent two-filter rule — no hidden weighting.
    """
    median_followers = df["followers"].median()
    median_risk = df[HONESTY_COL].median()
    candidates = df[(df["followers"] >= median_followers) & (df[HONESTY_COL] <= median_risk)]
    candidates = candidates.sort_values(HONESTY_COL).head(10)
    return [
        "## 3. Best Influencers for Brand Deals",
        "",
        f"Filter: followers ≥ median ({fmt_int(median_followers)}) AND Honesty Risk Score ≤ median ({median_risk:.1f}).",
        "These accounts combine meaningful reach with authentic engagement — the lowest-risk profile for sponsorship spend.",
        "",
        table(candidates, ["username", "followers", "engagement_rate", HONESTY_COL, "risk_label"],
              {"username": "Username", "followers": "Followers", "engagement_rate": "Engagement %",
               HONESTY_COL: "Honesty Risk Score", "risk_label": "Risk"})
        if len(candidates) else "_No accounts met both criteria in the current dataset._",
        "",
    ]


def section_highest_engagement(df):
    top_eng = df.nlargest(10, "engagement_rate").sort_values("engagement_rate", ascending=False)
    return [
        "## 4. Highest Engagement Accounts",
        "",
        "Raw engagement rate leaders. ⚠️ Cross-check against the Risk column — extremely",
        "high engagement rate is itself one of the Honesty Score's red flags, so a high",
        "rank here does not automatically mean an account is brand-safe.",
        "",
        table(top_eng, ["username", "followers", "engagement_rate", HONESTY_COL, "risk_label"],
              {"username": "Username", "followers": "Followers", "engagement_rate": "Engagement %",
               HONESTY_COL: "Honesty Risk Score", "risk_label": "Risk"}),
        "",
    ]


def section_low_risk(df):
    low = df[df["risk_label"] == "LOW RISK"].sort_values(HONESTY_COL)
    return [
        "## 5. Low Risk Accounts",
        "",
        f"**{len(low)} of {len(df)}** accounts ({len(low) / len(df) * 100:.0f}%) classified LOW RISK.",
        "",
        table(low, ["username", "followers", "engagement_rate", HONESTY_COL],
              {"username": "Username", "followers": "Followers", "engagement_rate": "Engagement %",
               HONESTY_COL: "Honesty Risk Score"})
        if len(low) else "_No accounts currently fall in the LOW RISK band._",
        "",
    ]


def section_high_risk(df):
    high = df[df["risk_label"] == "HIGH RISK"].sort_values(HONESTY_COL, ascending=False)
    return [
        "## 6. High Risk Accounts",
        "",
        f"**{len(high)} of {len(df)}** accounts ({len(high) / len(df) * 100:.0f}%) classified HIGH RISK.",
        "Recommend excluding these from sponsorship shortlists pending manual audience review.",
        "",
        table(high, ["username", "followers", "engagement_rate", HONESTY_COL],
              {"username": "Username", "followers": "Followers", "engagement_rate": "Engagement %",
               HONESTY_COL: "Honesty Risk Score"})
        if len(high) else "_No accounts currently fall in the HIGH RISK band._",
        "",
    ]


def main():
    df = load_scored_data()

    lines = [
        "# Business Insights Report",
        "",
        "_Auto-generated by `analytics/business_insights.py` from",
        "`data/processed/influencers_scored.csv`. Re-run after every new scoring pass",
        "to refresh these insights._",
        "",
        "---",
        "",
    ]

    lines += section_top_authentic(df)
    lines += section_top_suspicious(df)
    lines += section_brand_deals(df)
    lines += section_highest_engagement(df)
    lines += section_low_risk(df)
    lines += section_high_risk(df)

    out_path = os.path.join(REPORTS_DIR, "business_insights.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(str(x) for x in lines))

    print(f"Business insights report saved -> {out_path}")


if __name__ == "__main__":
    main()
