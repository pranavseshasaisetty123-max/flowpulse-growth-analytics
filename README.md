## FlowPulse Growth Analytics

**Goal:** End-to-end Growth Analytics project for a B2C SaaS application (`FlowPulse`), covering data modeling, large-scale synthetic data generation, SQL analytics, Python-based EDA, and a CEO-ready decision dashboard.

This project simulates the work of a first data analyst at a fast-growing startup, focused on translating data into **business decisions**, not just charts.

---

### 1. Business Context

- **Product:** FlowPulse — a workflow & habit-tracking app for knowledge workers and freelancers.
- **Business Model:** Freemium with paid tiers:
  - `Basic` – $9/month  
  - `Pro` – $19/month  
  - `Team` – $49/month
- **Primary Objective:** Drive sustainable revenue growth while improving retention and marketing efficiency.

**Key Business Questions**

- Are we growing efficiently? (MRR, MoM growth)
- Which customer segments and acquisition channels generate the highest LTV?
- Where are we losing revenue? (churn, failed payments, revenue leakage)
- How concentrated is revenue across customers?

---

### 2. Key KPIs Tracked

- **Monthly Recurring Revenue (MRR)**
- **Month-over-Month Revenue Growth**
- **Customer Lifetime Value (LTV)**
- **Customer Acquisition Cost (CAC)**
- **Churn Rate & Retention Cohorts**
- **LTV / CAC Ratio**
- **Revenue Concentration (Pareto 80/20)**
- **Revenue Leakage** (failed / refunded payments)

---

### 3. Project Structure

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

---

### 4. Setup

```bash
cd flowpulse-growth-analytics

# (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

---

### 5. Data Generation

```bash
python scripts/generate_synthetic_data.py
```

This script generates realistic SaaS-style datasets with churn, growth patterns, and marketing attribution.

Generated files in `data/raw/`:

- `customers.csv`
- `subscriptions.csv`
- `payments.csv`
- `marketing_channels.csv`
- `user_events.csv`

---

### 6. Analysis Overview

**SQL Analysis (`/sql`)** – each script answers a specific business question:

- `ddl_create_tables.sql` – schema & table definitions.
- `analytics_monthly_revenue.sql` – MRR trends & growth.
- `analytics_ltv.sql` – LTV by customer, plan, and segment.
- `analytics_churn_cohorts.sql` – retention & churn cohorts.
- `analytics_cac_by_channel.sql` – marketing efficiency.
- `analytics_pareto_customers.sql` – revenue concentration (top 20%).
- `analytics_revenue_leakage.sql` – failed payments & revenue leakage.

**Python EDA (`/notebooks`)**

- `01_data_generation.ipynb` – data sanity checks.
- `02_eda_growth_metrics.ipynb` – growth, churn, and revenue trends.
- `03_feature_deep_dive_retention.ipynb` – engagement vs churn.

---

### 7. Dashboard (CEO-Level)

**Specification:** `dashboard/powerbi_spec.md`

Designed for **executive decision-making**, not just reporting.

- **KPIs Included**
  - MRR & growth %
  - Active customers
  - Churn rate
  - LTV, CAC, and LTV/CAC ratio
- **Views**
  - Overview
  - Acquisition
  - Revenue
  - Retention
  - Customer Segments
- **Filters**
  - Date
  - Country
  - Segment
  - Device
  - Subscription plan

---

### 8. Sample Key Insights

> Insights are derived from the synthetic dataset and designed to mirror realistic SaaS behavior.

- ~20% of customers contribute over 60% of total revenue, indicating strong revenue concentration.
- Churn is highest within the first 2–3 months after conversion from free to paid plans.
- Paid acquisition channels show higher CAC with lower retention compared to organic and referral channels.
- Revenue leakage is primarily driven by failed renewals and delayed payment retries.

---

### 9. Business Recommendations

- Introduce **annual and discounted long-term plans** to reduce early-stage churn.
- Reallocate marketing spend from **high-CAC paid channels** toward referral and organic growth.
- Implement **automated renewal reminders and smart retry logic** to reduce payment failures.
- Design **onboarding nudges and engagement campaigns** to improve early product adoption and retention.

---

### 10. Notes

- The dataset is synthetic, but modeled to reflect realistic SaaS growth, churn, and marketing dynamics.
- The project emphasizes **business impact, metric selection, and decision-making**, not just visualizations.
- **Target audience:** Startup CEOs, founders, investors, and hiring managers.

