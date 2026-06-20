# STEP-BY-STEP EXECUTION GUIDE
## Influencer Honesty Score Project

---

## PHASE 1 — Setup Your Computer (Day 1, ~2 hours)

### Step 1 — Install Python
1. Open your browser. Go to: https://python.org/downloads
2. Click the big yellow "Download Python 3.x.x" button
3. Run the installer
4. IMPORTANT: Check the box that says "Add Python to PATH" before clicking Install
5. Click Install Now. Wait for it to finish.
6. Open Command Prompt (Windows: press Win+R → type cmd → press Enter)
7. Type: python --version
8. You should see: Python 3.x.x
   If you see an error, restart your computer and try again.

### Step 2 — Install VS Code
1. Go to: https://code.visualstudio.com
2. Click Download for Windows (or Mac)
3. Run the installer. Click Next → Next → Install
4. Open VS Code after installation

### Step 3 — Install Python extension in VS Code
1. In VS Code, press Ctrl+Shift+X
2. In the search bar type: Python
3. Click the first result (by Microsoft) → Click Install

### Step 4 — Create your project folder
1. Open Command Prompt
2. Type these commands one by one, pressing Enter after each:
   cd Desktop
   mkdir influencer-honesty-score
   cd influencer-honesty-score

### Step 5 — Set up virtual environment
Type these one by one:
   python -m venv venv
   venv\Scripts\activate

You will see (venv) appear at the start of the line. This means it worked.

### Step 6 — Create folder structure
Type each line and press Enter:
   mkdir data
   mkdir data\raw
   mkdir data\processed
   mkdir src
   mkdir dashboard
   mkdir report
   mkdir notebooks

### Step 7 — Install all required libraries
Type this one command and wait 3–5 minutes:
   pip install pandas numpy plotly dash requests openpyxl jupyter

When it finishes, type: pip list
You should see pandas, plotly, dash, etc. in the list.

### Step 8 — Open project in VS Code
Type: code .
VS Code will open with your project folder.

---

## PHASE 2 — Collect Data (Days 2–6)

### Step 1 — Open Google Sheets
Go to sheets.google.com → Click "Blank" to create a new sheet

### Step 2 — Set up your columns
In Row 1, type these headers (one per cell, A to J):
   username | platform | followers | following | total_posts
   avg_likes | avg_comments | avg_views | verified | hypeauditor_score

### Step 3 — Find influencers
1. Open Instagram on your phone or browser
2. Search: #fitnessindia
3. Click on posts → visit the profile
4. You need 75–100 profiles. Do 15–20 per day for 4–5 days.

### Step 4 — What to record per profile
For EACH influencer, open their profile and write down:
- username: their @ handle (without the @)
- platform: Instagram
- followers: the number shown (e.g. 450K = 450000)
- following: shown right next to followers
- total_posts: shown on their profile grid
- avg_likes: open their last 10 posts, note the like count, add them up and divide by 10
- avg_comments: same as above but for comment count
- avg_views: for Reels, note view count. Average of last 10 Reels.
- verified: yes if they have a blue tick, no if they don't
- hypeauditor_score: go to hypeauditor.com, paste their username, note the score shown (free)

### Step 5 — Save as CSV
1. In Google Sheets: File → Download → Comma Separated Values (.csv)
2. Save the file as: influencers_raw.csv
3. Move it into your project folder: influencer-honesty-score/data/raw/

---

## PHASE 3 — Run the Fake Score (Day 7)

### Step 1 — Copy scorer.py to your project
The file is already provided in the src/ folder.

### Step 2 — Open Command Prompt in your project folder
1. Open Command Prompt
2. Type: cd Desktop\influencer-honesty-score
3. Activate venv: venv\Scripts\activate

### Step 3 — Run the scorer
Type: python src/scorer.py

You will see a table printed showing the most suspicious influencers.
The scored file is saved in data/processed/influencers_scored.csv

---

## PHASE 4 — Run the Dashboard (Day 8)

### Step 1 — Open Command Prompt in your project folder
cd Desktop\influencer-honesty-score
venv\Scripts\activate

### Step 2 — Start the dashboard
python dashboard/app.py

### Step 3 — Open your browser
Go to: http://127.0.0.1:8050
You will see your live dashboard with charts and a ranking table.

### Step 4 — Take screenshots
Press Windows + Shift + S to take screenshots of:
- The bar chart (top suspicious influencers)
- The scatter plot
- The full ranking table
Save these screenshots. You will need them for your README and LinkedIn post.

---

## PHASE 5 — Write Insight Report (Day 9)

### Step 1 — Open Google Docs or Canva
Canva: go to canva.com → search "report template" → pick a clean one

### Step 2 — Write these 7 sections

SECTION 1 — TITLE
Influencer Honesty Score: Fitness Niche Analysis (India)
Your Name | Date

SECTION 2 — SUMMARY (3 lines)
"Analyzed [X] fitness influencers on Instagram. Built a custom Fake Engagement Score
using 4 metrics. Found that [X]% of accounts show signs of fake engagement."

SECTION 3 — METHODOLOGY
List your 4 formula components and weights. One sentence each.

SECTION 4 — TOP 5 SUSPICIOUS ACCOUNTS
Make a small table: Username | Followers | Fake Score | Risk Level

SECTION 5 — TOP 5 AUTHENTIC ACCOUNTS
Same table format.

SECTION 6 — KEY FINDINGS (3 bullet points)
Example: "Micro-influencers (10k–50k) had the highest average fake score at X/100"

SECTION 7 — BRAND RECOMMENDATION (2–3 lines)
"Brands should evaluate engagement rate AND like-comment ratio before partnerships.
Accounts with ER > 5% should be cross-checked with audience quality tools."

### Step 3 — Export as PDF
File → Download → PDF → Save as influencer_honesty_report.pdf
Move it to your report/ folder.

---

## PHASE 6 — Upload to GitHub (Day 10)

### Step 1 — Create GitHub account
Go to github.com → Sign Up (use your real name in username like anu-sharma)

### Step 2 — Create a new repository
1. Click the + icon (top right) → New repository
2. Repository name: influencer-honesty-score
3. Description: Fake engagement detection model for fitness influencers
4. Set to: Public
5. Do NOT check "Add a README file"
6. Click Create repository

### Step 3 — Connect your local project to GitHub
In Command Prompt (inside your project folder, venv activated):
   git init
   git add .
   git commit -m "Initial commit - Influencer Honesty Score project"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/influencer-honesty-score.git
   git push -u origin main

Replace YOUR_USERNAME with your actual GitHub username.

### Step 4 — Verify on GitHub
Go to github.com/YOUR_USERNAME/influencer-honesty-score
You should see all your files there.

### Step 5 — Add README on GitHub
Click "Add a README" on your repo page → paste the contents of your README.md → Commit changes

---

## PHASE 7 — Post on LinkedIn (Day 11)

### Best time to post: Tuesday or Wednesday, 10–11am IST

### Copy and customize this post:

---
I analyzed [X] fitness influencers and built a Fake Engagement Score from scratch using Python.

Here's what I found:

→ [X] out of [X] accounts show HIGH RISK fake engagement
→ Micro-influencers (10k–50k) had the most suspicious scores
→ Verified accounts with 500k+ followers showed the most authentic engagement

Built using:
• Python (Pandas, NumPy)
• Plotly Dash interactive dashboard
• Custom 4-component scoring formula

Full project + dataset on GitHub: [paste your GitHub link]

Happy to connect with anyone in data analytics, marketing tech, or recruitment!

#DataAnalytics #Python #InfluencerMarketing #DataScience #OpenToWork #FresherJobs
---

### Screenshot to attach: your dashboard screenshot (the bar chart works best)

---

## YOU'RE DONE. 🎉

Files in your project:
✅ data/raw/influencers_raw.csv        — your collected data
✅ data/processed/influencers_scored.csv — scored and ranked
✅ src/scorer.py                        — your scoring engine
✅ src/youtube_collector.py             — YouTube API collector
✅ dashboard/app.py                     — interactive dashboard
✅ report/influencer_honesty_report.pdf — 1-page insight report
✅ README.md                            — GitHub documentation
✅ requirements.txt                     — library list
✅ .gitignore                           — GitHub cleanup
