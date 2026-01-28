## FlowPulse Growth & Retention Dashboard (Power BI Spec)

### 1. Audience and purpose

- **Audience:** CEO, Head of Growth, Product, and investors.
- **Purpose:** Track revenue growth, acquisition efficiency, retention, and segment performance in one place.

### 2. Data sources

- `customers`
- `subscriptions`
- `payments`
- `marketing_channels`
- `user_events`

Loaded from the CSVs in `data/raw/` or from your warehouse tables based on `sql/ddl_create_tables.sql`.

### 3. Pages / tabs

1. **Overview**
2. **Acquisition & CAC**
3. **Revenue & Monetization**
4. **Retention & Engagement**
5. **Customer Segments**

---

### 4. Overview page

**Top KPIs (card visuals):**
- MRR (current month, USD)
- MRR MoM growth %
- Active customers (last 30 days)
- Net customer churn rate (last 30 days / last month)
- Average LTV per paying customer
- Blended CAC
- LTV/CAC ratio

**Charts:**
- **Line chart:** `MRR over time`
  - Axis: Month
  - Values: Sum of `amount_usd` (successful payments)
  - Filters: payment_status = success
- **Line chart:** `Active customers over time`
  - Axis: Month
  - Values: Count of distinct `customer_id` with at least one `user_event` in that month.
- **Clustered column + line:** `Net customer adds`
  - Columns: New customers per month.
  - Line: Churned customers per month.

**Business narrative:**
- Helps CEO answer: *“Are we growing fast enough, and is that growth healthy?”*

---

### 5. Acquisition & CAC page

**KPIs:**
- New customers (selected period)
- Blended CAC (selected period)
- LTV/CAC ratio (overall and by channel)

**Charts:**
- **Stacked column chart:** `New customers by channel`
  - Axis: Month
  - Legend: `channel_name`
  - Values: Count of distinct `customer_id`.
- **Bar chart:** `CAC by channel`
  - Axis: `channel_name`
  - Values: Average `cac_usd` from `marketing_channels` or calculated CAC.
- **Scatter plot:** `LTV vs CAC by channel`
  - X: CAC (per channel)
  - Y: Average LTV (per channel)
  - Size: Number of customers
  - Color: Channel name

**Filters:**
- Date range
- Country
- Segment

**Business narrative:**
- Highlights which channels should get more/less budget based on LTV/CAC and payback period.

---

### 6. Revenue & Monetization page

**KPIs:**
- Gross revenue (selected period)
- Revenue leakage % (failed + refunded / gross)
- ARPU (average revenue per user)

**Charts:**
- **Area chart:** `Revenue vs Revenue leakage`
  - Axis: Month
  - Values:
    - Successful revenue
    - Failed + refunded amounts
- **Funnel:** `Free → Trial → Paid → Retained`
  - Stages:
    - Total signups
    - Started trial (non-free subscriptions + trial_start_date)
    - Paying customers
    - Retained at 3 months / 6 months
- **Table:** `Top 20% customers`
  - Columns: customer_id, LTV, segment, country, plan.

**Business narrative:**
- Helps quantify how strong the monetization engine is and where money is being left on the table.

---

### 7. Retention & Engagement page

**KPIs:**
- 3-month customer retention %
- 6-month customer retention %
- DAU/WAU/MAU ratios

**Charts:**
- **Heatmap (matrix):** `Cohort retention`
  - Rows: Cohort month (signup cohort)
  - Columns: Months since signup (0, 1, 2, 3, …)
  - Values: Retention rate.
- **Line chart:** `DAU, WAU, MAU trends`
  - Axis: Date (daily or weekly)
  - Values: Distinct active users in each window.
- **Boxplot or column chart:** `Sessions_last_30d by churn status`
  - Categories: `is_active` vs churned.
  - Values: Sessions in last 30 days.

**Business narrative:**
- Shows if users are sticking around and where engagement drops before churn.

---

### 8. Customer Segments page

**KPIs:**
- MRR by segment
- Churn rate by segment

**Charts:**
- **Bar chart:** `MRR by segment`
  - Axis: `segment`
  - Values: Sum `amount_usd` (successful).
- **Bar chart:** `Churn rate by segment`
  - Axis: `segment`
  - Values: churned customers / total customers in segment.
- **Stacked bar chart:** `Plan mix by segment`
  - Axis: `segment`
  - Legend: `plan_name`
  - Values: Count of active subscriptions.

**Filters:**
- Date range
- Country
- Device type

**Business narrative:**
- Identifies which segments are high-value and where churn is concentrated so product/CS can prioritize.

---

### 9. Global filters and drill-downs

**Global filters (slicers on all pages):**
- Date range (months/years)
- Country
- Segment
- Device type
- Plan (Basic, Pro, Team, Free)

**Drill-down examples:**
- Click on a country in `MRR by country` to drill into:
  - Channel mix and CAC for that country.
  - Churn and LTV for that country.
- Click on a channel in `CAC by channel` to see:
  - Retention curves for cohorts acquired by that channel.
  - Revenue and payback by months since signup.

---

### 10. Implementation notes

- Build views or materialized tables in your warehouse from the SQL scripts in `/sql` for:
  - `monthly_revenue`
  - `ltv_per_customer`
  - `cohort_retention`
  - `cac_by_channel`
  - `revenue_leakage`
- Connect Power BI / Tableau directly to those views for fast refresh and simple visuals.

