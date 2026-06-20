# 🔍 Influencer Honesty Score

> Detecting fake engagement across fitness influencers on Instagram/YouTube using a custom-built scoring model.

---

## 🧠 What This Project Does

Brands waste billions on influencers with fake followers and bot-driven engagement.  
This project builds a **Fake Engagement Score (0–100)** for 100 fitness influencers using 4 measurable signals — and ranks them from most suspicious to most authentic.

**Higher score = more likely to have fake engagement.**

---

## 📊 Key Findings

- **9 out of 20** analyzed accounts showed HIGH RISK fake engagement patterns
- **Average Fake Score: 63.7 / 100** across fitness influencers
- Micro-influencers (10k–50k followers) had the **highest fake scores** on average
- Mega influencers (500k+) scored significantly lower — consistent, organic growth

---

## 🧪 My Fake Score Formula

```
Fake_Score = (0.30 × Engagement Rate Deviation)
           + (0.20 × Follower-Following Ratio)
           + (0.25 × Like-to-Comment Ratio)
           + (0.25 × Audience Quality Score)
```

| Component | Weight | What it detects |
|---|---|---|
| Engagement Rate Deviation | 30% | ER too high or too low vs industry avg (2%) |
| Follower-Following Ratio | 20% | Bought followers = high following, low ratio |
| Like-to-Comment Ratio | 25% | Bots like but don't comment — ratio > 200:1 = suspicious |
| Audience Quality | 25% | HypeAuditor's audience authenticity score (inverted) |

---

## 🛠️ Tech Stack

- **Python** — Pandas, NumPy
- **Plotly Dash** — Interactive dashboard
- **YouTube Data API v3** — Data collection
- **HypeAuditor** — Audience quality scores

---

## 🗂️ Project Structure

```
influencer-honesty-score/
├── data/
│   ├── raw/                  # Original collected data
│   └── processed/            # Scored and ranked output
├── src/
│   ├── scorer.py             # Fake Score calculation engine
│   └── youtube_collector.py  # YouTube API data collector
├── dashboard/
│   └── app.py                # Plotly Dash interactive dashboard
├── report/
│   └── influencer_honesty_report.pdf
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/influencer-honesty-score.git
cd influencer-honesty-score

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the scorer
python src/scorer.py

# 5. Launch the dashboard
python dashboard/app.py
# Open http://127.0.0.1:8050
```

---

## 📁 Dataset

20-sample dataset included in `data/raw/influencers_raw.csv`.  
Full 100-influencer dataset available on request.

---

## 👩‍💻 About

Built by **Anu** | Final Year B.Tech CSE | Malla Reddy University, Hyderabad  
Open to Data Analyst / Full Stack Developer roles — [LinkedIn](#)
