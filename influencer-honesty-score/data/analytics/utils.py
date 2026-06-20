"""
analytics/utils.py — Shared helpers for the analytics layer.

Every analytics script (correlation_analysis, visualizations, business_insights,
data_quality, executive_report) imports from here so that column names, folder
paths and derived fields stay consistent across the whole project.

This file does NOT touch src/scorer.py or the Fake Score formula — it only
reads the already-scored CSV and adds a couple of presentation-only helper
columns (follower tier, honesty label) used purely for grouping in charts
and reports.
"""

import os
import pandas as pd

# ─────────────────────────────────────────────
# PATHS (relative to project root — run scripts from project root)
# ─────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORED_CSV = os.path.join(PROJECT_ROOT, "data", "processed", "influencers_scored.csv")
RAW_CSV = os.path.join(PROJECT_ROOT, "data", "raw", "influencers_raw.csv")

VIS_DIR = os.path.join(PROJECT_ROOT, "visualizations")
ANALYTICS_DIR = os.path.join(PROJECT_ROOT, "analytics")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

for _d in (VIS_DIR, REPORTS_DIR):
    os.makedirs(_d, exist_ok=True)

# ─────────────────────────────────────────────
# COLUMN MAP
# The scorer.py output already contains everything we need.
# "fake_score" = the project's core Honesty Score (0-100, HIGHER = more
# suspicious / less honest). We surface it everywhere as "Honesty Risk Score"
# so a non-technical reader (e.g. a brand manager) understands direction
# without having to know the internal column name.
# ─────────────────────────────────────────────
HONESTY_COL = "fake_score"
HONESTY_LABEL = "Honesty Risk Score"

CORRELATION_METRICS = {
    "followers": "Followers",
    "following": "Following",
    "avg_likes": "Avg Likes",
    "avg_comments": "Avg Comments",
    "engagement_rate": "Engagement Rate",
    "lc_ratio": "Like-Comment Ratio",
    HONESTY_COL: HONESTY_LABEL,
}

RISK_COLORS = {
    "HIGH RISK": "#E24B4A",
    "MEDIUM RISK": "#EF9F27",
    "LOW RISK": "#639922",
}


def load_scored_data():
    """Load the scored dataset and attach presentation-only helper columns."""
    df = pd.read_csv(SCORED_CSV)

    # Follower tier — used for "category comparison" charts since the current
    # dataset only contains a single niche (fitness) and a single platform
    # (Instagram). Follower tier gives a meaningful, analytically useful
    # grouping dimension without inventing data that doesn't exist.
    bins = [-1, 50_000, 200_000, 1_000_000, float("inf")]
    tier_labels = ["Nano (<50K)", "Micro (50K-200K)", "Macro (200K-1M)", "Mega (1M+)"]
    df["follower_tier"] = pd.cut(df["followers"], bins=bins, labels=tier_labels)

    return df


def fmt_int(n):
    return f"{int(n):,}"
