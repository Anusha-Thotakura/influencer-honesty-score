# Data Quality Report

**Dataset:** `data/raw/influencers_raw.csv`  
**Rows:** 20  **Columns:** 11  
**Scored output validated:** `data/processed/influencers_scored.csv` (20 rows)

---

## 1. Missing Values

No missing values found in any column. ✅

## 2. Duplicate Rows

- Fully duplicate rows: **0**
- Duplicate `username` entries: **0**

## 3. Outliers (IQR Method, 1.5×IQR bounds)

| column            |   lower_bound |      upper_bound |   outlier_count | outlier_usernames   |
|:------------------|--------------:|-----------------:|----------------:|:--------------------|
| followers         |    -545625    |      1.13938e+06 |               1 | shraddha_fit        |
| following         |      -8017.5  |  14210.5         |               0 | -                   |
| total_posts       |       -726.25 |   1943.75        |               1 | yogalife_arjun      |
| avg_likes         |     -19543.8  |  33646.2         |               0 | -                   |
| avg_comments      |       -905    |   1523           |               0 | -                   |
| avg_views         |    -270312    | 480188           |               0 | -                   |
| hypeauditor_score |        -48.5  |    151.5         |               0 | -                   |

*Note: outliers here are statistically unusual values, not necessarily errors —
in this dataset, several outliers are exactly the accounts the Honesty Score is
designed to flag (e.g. unusually high follower counts relative to engagement).*

## 4. Invalid / Implausible Entries

No invalid or implausible entries detected. ✅

## 5. Dataset Health Score

### **99.3 / 100 — Excellent**

Composite score combining missing-value rate, duplicate-row rate, outlier
density, and invalid-entry checks. 100 = perfectly clean dataset.

| Check | Weight (max penalty) |
|---|---|
| Missing values | -30 |
| Duplicate rows | -20 |
| Duplicate usernames | -10 |
| Outlier density | -15 |
| Invalid entries | -25 |