#!/usr/bin/env bash
# One-step launcher for the Influencer Honesty Score dashboard.
# Usage: ./run.sh
set -e
cd "$(dirname "$0")"
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "Starting dashboard..."
echo "Open http://127.0.0.1:8050 in your browser once it says 'Dash is running'."
python dashboard/app.py
