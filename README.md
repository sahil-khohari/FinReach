# 🚀 FinReach: Product & Customer Analytics Platform

![FinReach Banner](https://img.shields.io/badge/Product-Analytics-00d2ff?style=for-the-badge&logo=data)
![Stack](https://img.shields.io/badge/Stack-Python%20|%20PostgreSQL%20|%20Tableau-3a7bd5?style=for-the-badge)

Welcome to **FinReach**, a comprehensive product analytics portfolio project focused on digital micro-lending. This repository demonstrates end-to-end data analysis capabilities from synthetic event generation to AI-driven insights and business recommendations.

## 🌟 Live Interactive Demo

Experience the statistical engine and AI recommendation system in real-time:
👉 **[Live Demo: FinReach Analytics](https://finreach-analytics.vercel.app/)**

## 🏗️ Project Architecture

The project is structured into 5 core phases:

### Phase 1: Event Log Generation (`data_generation.py`)
Generates realistic app telemetry for 20,000 users. It simulates a conversion funnel (`signup -> browse -> apply -> funded -> repaid -> repeat_apply`) with statistical probabilities of drop-off at each stage to mimic real-world user behavior.

### Phase 2: SQL Funnel & Cohort Queries (`funnel_cohort.sql`)
Advanced PostgreSQL queries that extract business value:
- **Funnel Conversion:** Uses conditional aggregation (`SUM(CASE WHEN...)`) to track absolute counts and percentage drop-offs across the funnel.
- **Monthly Cohort Retention:** Uses Window Functions and Date math to plot the percentage of users returning for subsequent loans month over month.

### Phase 3: RFM Segmentation & A/B Testing (`rfm_ab_testing.py`)
- **RFM Model:** Scores borrowers on Recency, Frequency, and Monetary value, binning them into 4 actionable segments (Champions, Loyal Customers, At Risk, Lost) using `pandas.qcut`.
- **A/B Testing:** Uses `scipy.stats` to perform a rigorous two-proportion Z-test on funnel variants, determining statistical significance and confidence intervals.

### Phase 4: AI Next-Best-Action Engine (`ai_action_engine.py`)
Integrates the Gemini 1.5 Pro LLM via API to turn raw metrics into structured, actionable business strategies. The engine reads the segmented RFM metrics and generates concrete, micro-lending specific next-best-actions formatted as strict JSON.

### Phase 5: Tableau Dashboard Prep (`tableau_prep.sql`)
Creates robust SQL views ready for BI ingestion:
- Flattens cohort retention data for heatmap visualization.
- Joins borrower demographics with LTV and RFM segments while safely filtering anomalous data points.

## 🚀 Running Locally

```bash
# 1. Clone the repository
git clone https://github.com/sahil-khohari/FinReach.git
cd FinReach

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add API Keys
# Create a .env file and add your GEMINI_API_KEY
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 4. Run any of the phase scripts
python data_generation.py
python rfm_ab_testing.py
```

## 🌐 Deployment (Vercel Serverless)

The API and frontend are hosted using Vercel Serverless functions. 
- **Framework:** FastAPI
- **Config:** `vercel.json` rewrites traffic through `api/index.py` which serves both the frontend HTML and the backend API endpoints.

---
*Developed as a showcase for advanced product analytics, SQL, Python, and AI integration.*
