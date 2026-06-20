"""
scorer.py — Influencer Honesty Score Calculator
Computes a Fake Engagement Score (0–100) for each influencer.
Higher score = more suspicious / likely fake engagement.
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv('data/raw/influencers_raw.csv')
print(f"Loaded {len(df)} influencers.\n")


# ─────────────────────────────────────────────
# COMPONENT 1 — Engagement Rate Deviation (30%)
# Real fitness influencers avg 1–3% ER.
# Too high OR too low is suspicious.
# ─────────────────────────────────────────────
INDUSTRY_AVG_ER = 2.0  # 2% is normal for fitness niche

df['engagement_rate'] = (
    (df['avg_likes'] + df['avg_comments']) / df['followers'] * 100
).round(4)

df['er_deviation'] = abs(df['engagement_rate'] - INDUSTRY_AVG_ER)

max_dev = df['er_deviation'].max()
# Normalize: higher deviation = higher suspicion score (0–10)
df['er_score'] = (df['er_deviation'] / max_dev * 10).round(2)


# ─────────────────────────────────────────────
# COMPONENT 2 — Follower-to-Following Ratio (20%)
# Real influencers follow very few, have many followers.
# High following count relative to followers = bought followers.
# ─────────────────────────────────────────────
df['ff_ratio'] = (df['followers'] / (df['following'] + 1)).round(2)

# Low ratio = suspicious. Invert so low ratio → high score.
min_ratio = df['ff_ratio'].min()
max_ratio = df['ff_ratio'].max()
df['ff_score'] = (
    (max_ratio - df['ff_ratio']) / (max_ratio - min_ratio) * 10
).round(2)


# ─────────────────────────────────────────────
# COMPONENT 3 — Like-to-Comment Ratio (25%)
# Bots can like posts automatically but rarely comment.
# Ratio > 200:1 strongly suggests bot activity.
# ─────────────────────────────────────────────
df['lc_ratio'] = (df['avg_likes'] / (df['avg_comments'] + 1)).round(2)

max_lc = df['lc_ratio'].max()
# Higher ratio = more suspicious
df['lc_score'] = (df['lc_ratio'] / max_lc * 10).round(2)


# ─────────────────────────────────────────────
# COMPONENT 4 — HypeAuditor Audience Quality (25%)
# Industry tool score 0–100 (higher = more authentic).
# Invert it: low score = high suspicion.
# ─────────────────────────────────────────────
df['quality_score'] = (
    (100 - df['hypeauditor_score']) / 100 * 10
).round(2)


# ─────────────────────────────────────────────
# FINAL FAKE SCORE (0–100)
# ─────────────────────────────────────────────
df['fake_score'] = (
    0.30 * df['er_score'] +
    0.20 * df['ff_score'] +
    0.25 * df['lc_score'] +
    0.25 * df['quality_score']
) * 10

df['fake_score'] = df['fake_score'].round(1)

# Add risk label
def label(score):
    if score >= 70:
        return 'HIGH RISK'
    elif score >= 40:
        return 'MEDIUM RISK'
    else:
        return 'LOW RISK'

df['risk_label'] = df['fake_score'].apply(label)
df['rank'] = df['fake_score'].rank(ascending=False).astype(int)

df_sorted = df.sort_values('fake_score', ascending=False).reset_index(drop=True)

# ─────────────────────────────────────────────
# SAVE OUTPUT
# ─────────────────────────────────────────────
df_sorted.to_csv('data/processed/influencers_scored.csv', index=False)
print("Scored file saved to data/processed/influencers_scored.csv\n")

# ─────────────────────────────────────────────
# PRINT SUMMARY
# ─────────────────────────────────────────────
print("=" * 55)
print("TOP 10 MOST SUSPICIOUS INFLUENCERS")
print("=" * 55)
print(df_sorted[['rank','username','followers','fake_score','risk_label']].head(10).to_string(index=False))

print("\n" + "=" * 55)
print("TOP 5 MOST AUTHENTIC INFLUENCERS")
print("=" * 55)
print(df_sorted[['rank','username','followers','fake_score','risk_label']].tail(5).to_string(index=False))

print("\n" + "=" * 55)
print("SUMMARY STATS")
print("=" * 55)
print(f"Average Fake Score     : {df['fake_score'].mean():.1f} / 100")
print(f"High Risk accounts     : {(df['risk_label']=='HIGH RISK').sum()}")
print(f"Medium Risk accounts   : {(df['risk_label']=='MEDIUM RISK').sum()}")
print(f"Low Risk accounts      : {(df['risk_label']=='LOW RISK').sum()}")
