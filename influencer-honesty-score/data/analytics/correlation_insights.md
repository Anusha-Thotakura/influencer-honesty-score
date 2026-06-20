# Correlation Analysis — Key Relationships

Auto-generated from `analytics/correlation_analysis.py`. Pearson correlation
coefficients (r) range from -1 (perfect inverse relationship) to +1 (perfect
direct relationship). `Honesty Risk Score` is the project's core 0-100 metric
where **higher = more suspicious / less authentic**.

## Strongest Relationships

| Metric A | Metric B | Correlation (r) | Interpretation |
|---|---|---|---|
| Avg Likes | Avg Comments | +0.98 | strong positive |
| Followers | Avg Likes | +0.96 | strong positive |
| Engagement Rate | Like-Comment Ratio | -0.92 | strong negative |
| Followers | Avg Comments | +0.92 | strong positive |
| Like-Comment Ratio | Honesty Risk Score | +0.91 | strong positive |
| Avg Comments | Honesty Risk Score | -0.89 | strong negative |

## Full Correlation Matrix

|                    |   Followers |   Following |   Avg Likes |   Avg Comments |   Engagement Rate |   Like-Comment Ratio |   Honesty Risk Score |
|:-------------------|------------:|------------:|------------:|---------------:|------------------:|---------------------:|---------------------:|
| Followers          |        1    |       -0.64 |        0.96 |           0.92 |              0.56 |                -0.53 |                -0.81 |
| Following          |       -0.64 |        1    |       -0.67 |          -0.69 |             -0.78 |                 0.75 |                 0.78 |
| Avg Likes          |        0.96 |       -0.67 |        1    |           0.98 |              0.72 |                -0.68 |                -0.88 |
| Avg Comments       |        0.92 |       -0.69 |        0.98 |           1    |              0.76 |                -0.73 |                -0.89 |
| Engagement Rate    |        0.56 |       -0.78 |        0.72 |           0.76 |              1    |                -0.92 |                -0.84 |
| Like-Comment Ratio |       -0.53 |        0.75 |       -0.68 |          -0.73 |             -0.92 |                 1    |                 0.91 |
| Honesty Risk Score |       -0.81 |        0.78 |       -0.88 |          -0.89 |             -0.84 |                 0.91 |                 1    |

*(See `visualizations/correlation_heatmap.png` for the visual heatmap.)*