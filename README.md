## FlowPulse Growth Analytics

**Goal:** End-to-end Growth Analytics project for a B2C SaaS app (`FlowPulse`) covering data model, synthetic dataset, SQL analytics, Python EDA, and a CEO-ready dashboard.

### 1. Business context

- **Product:** FlowPulse – workflow & habit-tracking app for knowledge workers and freelancers.
- **Model:** Freemium with paid tiers (`Basic` $9/mo, `Pro` $19/mo, `Team` $49/mo).
- **Key questions:**
  - Are we growing efficiently (MRR, MoM growth)?
  - Which channels and segments drive the best LTV?
  - Where are we leaking revenue or losing users (churn, failed payments)?

### 2. Project structure

```text
flowpulse-growth-analytics/
├─ data/
│  ├─ raw/
│  │  ├─ customers.csv
│  │  ├─ subscriptions.csv
│  │  ├─ payments.csv
│  │  ├─ marketing_channels.csv
│  │  ├─ user_events.csv
│  └─ processed/
├─ sql/
│  ├─ ddl_create_tables.sql
│  ├─ analytics_monthly_revenue.sql
│  ├─ analytics_ltv.sql
│  ├─ analytics_churn_cohorts.sql
│  ├─ analytics_cac_by_channel.sql
│  ├─ analytics_pareto_customers.sql
│  ├─ analytics_revenue_leakage.sql
├─ notebooks/
│  ├─ 01_data_generation.ipynb
│  ├─ 02_eda_growth_metrics.ipynb
│  └─ 03_feature_deep_dive_retention.ipynb
├─ dashboard/
│  ├─ powerbi_spec.md
│  ├─ mockup_screenshots/
├─ scripts/
│  └─ generate_synthetic_data.py
├─ requirements.txt
├─ .gitignore
└─ README.md
```

### 3. Setup

```bash
cd flowpulse-growth-analytics

# (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

### 4. Generate synthetic data

```bash
python scripts/generate_synthetic_data.py
```

This creates CSV files in `data/raw/`:

- `customers.csv`
- `subscriptions.csv`
- `payments.csv`
- `marketing_channels.csv`
- `user_events.csv`

### 5. Analysis

- **SQL (`/sql`)**
  - `ddl_create_tables.sql` – schema definitions.
  - `analytics_monthly_revenue.sql` – MRR & growth.
  - `analytics_ltv.sql` – LTV by customer and segment.
  - `analytics_churn_cohorts.sql` – retention cohorts.
  - `analytics_cac_by_channel.sql` – CAC by marketing channel.
  - `analytics_pareto_customers.sql` – top 20% customers by revenue.
  - `analytics_revenue_leakage.sql` – failed/refunded payments and churn.

- **Notebooks (`/notebooks`)**
  - `01_data_generation.ipynb` – sanity checks on synthetic data.
  - `02_eda_growth_metrics.ipynb` – core growth & retention analysis.
  - `03_feature_deep_dive_retention.ipynb` – engagement vs churn.

### 6. Dashboard

- Specification in `dashboard/powerbi_spec.md`.
- Includes:
  - KPIs: MRR, MRR growth %, active customers, churn, LTV, CAC, LTV/CAC.
  - Pages: Overview, Acquisition, Revenue, Retention, Segments.
  - Filters: date, country, segment, device, plan.

### 7. Notes

- Dataset is synthetic but modeled to mimic real-world B2C SaaS growth, churn, and marketing performance.
- Designed for a startup CEO / investor audience: focus on business impact, not just visuals.

