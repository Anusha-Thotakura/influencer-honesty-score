"""
analytics/run_analytics.py — Master Analytics Pipeline

Runs the full analytics layer in the correct order with a single command.
Assumes src/scorer.py has already been run (data/processed/influencers_scored.csv
must exist) — this pipeline only ANALYZES the scored output, it does not
recompute the Fake/Honesty Score itself.

Run from the project root:
    python src/scorer.py            # (if not already run)
    python analytics/run_analytics.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics.utils import SCORED_CSV
from analytics import data_quality, correlation_analysis, visualizations, business_insights, executive_report


def main():
    if not os.path.exists(SCORED_CSV):
        print(f"ERROR: {SCORED_CSV} not found. Run `python src/scorer.py` first.")
        sys.exit(1)

    print("=" * 60)
    print("STEP 1/5 — Data Quality Report")
    print("=" * 60)
    data_quality.main()

    print("\n" + "=" * 60)
    print("STEP 2/5 — Correlation Analysis")
    print("=" * 60)
    correlation_analysis.main()

    print("\n" + "=" * 60)
    print("STEP 3/5 — Advanced Visualizations")
    print("=" * 60)
    visualizations.main()

    print("\n" + "=" * 60)
    print("STEP 4/5 — Business Insights Engine")
    print("=" * 60)
    business_insights.main()

    print("\n" + "=" * 60)
    print("STEP 5/5 — Executive Analytics Report")
    print("=" * 60)
    executive_report.main()

    print("\n" + "=" * 60)
    print("ANALYTICS PIPELINE COMPLETE")
    print("=" * 60)
    print("  visualizations/   -> all chart PNGs")
    print("  analytics/        -> correlation_matrix.csv, correlation_insights.md")
    print("  reports/          -> data_quality_report.md, business_insights.md, executive_summary.md")
    print("\nNext: launch the dashboard ->  python dashboard/app.py")


if __name__ == "__main__":
    main()
