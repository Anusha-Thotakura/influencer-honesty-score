"""
analytics/visualizations.py — Advanced Data Visualizations

Generates the full chart suite required for the analytics upgrade and saves
every figure as a PNG inside visualizations/. Built with matplotlib +
seaborn so the output is static, portable, and embeddable in the README /
PDF report (the Plotly Dash dashboard generates its own *interactive*
versions of several of these charts separately).

Run:
    python analytics/visualizations.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

from analytics.utils import load_scored_data, VIS_DIR, RISK_COLORS, HONESTY_COL

sns.set_theme(style="whitegrid", font_scale=0.95)
RISK_ORDER = ["LOW RISK", "MEDIUM RISK", "HIGH RISK"]


def _save(fig, name):
    path = os.path.join(VIS_DIR, name)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved -> {path}")


# ── 1. Followers Distribution Histogram ─────────────────────────────────
def followers_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["followers"], bins=10, kde=True, color="#3A7CA5", ax=ax)
    ax.set_title("Followers Distribution")
    ax.set_xlabel("Followers")
    ax.set_ylabel("Number of Influencers")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    _save(fig, "followers_distribution.png")


# ── 2. Engagement Rate Histogram ────────────────────────────────────────
def engagement_rate_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["engagement_rate"], bins=10, kde=True, color="#E76F51", ax=ax)
    ax.set_title("Engagement Rate Distribution")
    ax.set_xlabel("Engagement Rate (%)")
    ax.set_ylabel("Number of Influencers")
    _save(fig, "engagement_rate_distribution.png")


# ── 3. Honesty Score Distribution ───────────────────────────────────────
def honesty_score_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df[HONESTY_COL], bins=10, kde=True, color="#8E44AD", ax=ax)
    ax.set_title("Honesty Risk Score Distribution (0=Authentic, 100=Suspicious)")
    ax.set_xlabel("Honesty Risk Score")
    ax.set_ylabel("Number of Influencers")
    _save(fig, "honesty_score_distribution.png")


# ── 4. Scatter: Followers vs Engagement ─────────────────────────────────
def scatter_followers_engagement(df):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    sns.scatterplot(
        data=df, x="followers", y="engagement_rate",
        hue="risk_label", hue_order=RISK_ORDER, palette=RISK_COLORS,
        s=90, ax=ax, edgecolor="white", linewidth=0.6,
    )
    ax.set_title("Followers vs Engagement Rate")
    ax.set_xlabel("Followers")
    ax.set_ylabel("Engagement Rate (%)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.legend(title="Risk Level", loc="upper right", fontsize=8)
    _save(fig, "scatter_followers_vs_engagement.png")


# ── 5. Scatter: Likes vs Comments ───────────────────────────────────────
def scatter_likes_comments(df):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    sns.scatterplot(
        data=df, x="avg_likes", y="avg_comments",
        hue="risk_label", hue_order=RISK_ORDER, palette=RISK_COLORS,
        s=90, ax=ax, edgecolor="white", linewidth=0.6,
    )
    ax.set_title("Average Likes vs Average Comments")
    ax.set_xlabel("Avg Likes")
    ax.set_ylabel("Avg Comments")
    ax.legend(title="Risk Level", loc="lower right", fontsize=8)
    _save(fig, "scatter_likes_vs_comments.png")


# ── 6. Box Plot: Honesty Score by Risk Label ────────────────────────────
def honesty_score_boxplot(df):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    sns.boxplot(
        data=df, x="risk_label", y=HONESTY_COL, order=RISK_ORDER,
        hue="risk_label", palette=RISK_COLORS, legend=False, ax=ax,
    )
    sns.stripplot(
        data=df, x="risk_label", y=HONESTY_COL, order=RISK_ORDER,
        color="black", alpha=0.5, size=4, ax=ax,
    )
    ax.set_title("Honesty Risk Score Spread by Risk Category")
    ax.set_xlabel("Risk Category")
    ax.set_ylabel("Honesty Risk Score")
    _save(fig, "honesty_score_boxplot.png")


# ── 7. Top 10 Influencers (most authentic = lowest honesty risk score) ─
def top10_chart(df):
    top10 = df.nsmallest(10, HONESTY_COL).sort_values(HONESTY_COL)
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.barh(top10["username"], top10[HONESTY_COL], color="#2E8B57")
    ax.set_title("Top 10 Most Authentic Influencers (Lowest Honesty Risk Score)")
    ax.set_xlabel("Honesty Risk Score")
    ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=8)
    ax.set_xlim(0, max(100, top10[HONESTY_COL].max() * 1.15))
    _save(fig, "top10_most_authentic_influencers.png")


# ── 8. Bottom 10 Influencers (most suspicious = highest honesty risk) ──
def bottom10_chart(df):
    bottom10 = df.nlargest(10, HONESTY_COL).sort_values(HONESTY_COL)
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.barh(bottom10["username"], bottom10[HONESTY_COL], color="#C0392B")
    ax.set_title("Bottom 10 Most Suspicious Influencers (Highest Honesty Risk Score)")
    ax.set_xlabel("Honesty Risk Score")
    ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=8)
    ax.set_xlim(0, 105)
    _save(fig, "bottom10_most_suspicious_influencers.png")


# ── 9. Category Comparison (by follower tier — see analytics/utils.py) ─
def category_comparison_chart(df):
    grouped = (
        df.groupby("follower_tier", observed=True)
        .agg(avg_honesty_risk=(HONESTY_COL, "mean"),
             avg_engagement=("engagement_rate", "mean"),
             count=("username", "count"))
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.barplot(data=grouped, x="follower_tier", y="avg_honesty_risk",
                color="#8E44AD", ax=axes[0])
    axes[0].set_title("Avg Honesty Risk Score by Follower Tier")
    axes[0].set_xlabel("Follower Tier")
    axes[0].set_ylabel("Avg Honesty Risk Score")
    axes[0].tick_params(axis="x", rotation=20)

    sns.barplot(data=grouped, x="follower_tier", y="avg_engagement",
                color="#E76F51", ax=axes[1])
    axes[1].set_title("Avg Engagement Rate by Follower Tier")
    axes[1].set_xlabel("Follower Tier")
    axes[1].set_ylabel("Avg Engagement Rate (%)")
    axes[1].tick_params(axis="x", rotation=20)

    fig.suptitle("Category Comparison — Follower Tiers", fontsize=13)
    _save(fig, "category_comparison_follower_tier.png")


def main():
    df = load_scored_data()
    followers_distribution(df)
    engagement_rate_distribution(df)
    honesty_score_distribution(df)
    scatter_followers_engagement(df)
    scatter_likes_comments(df)
    honesty_score_boxplot(df)
    top10_chart(df)
    bottom10_chart(df)
    category_comparison_chart(df)
    print(f"\nAll visualizations saved in: {VIS_DIR}")


if __name__ == "__main__":
    main()
