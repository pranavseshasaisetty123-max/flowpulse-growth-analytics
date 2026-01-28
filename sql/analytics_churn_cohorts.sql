-- Cohort retention analysis: signup cohorts vs months since signup.

WITH customer_cohorts AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', signup_date)::date AS cohort_month,
        signup_date,
        churned_date
    FROM customers
),

activity_months AS (
    SELECT
        c.customer_id,
        c.cohort_month,
        DATE_TRUNC('month', e.event_timestamp)::date AS activity_month
    FROM customer_cohorts c
    LEFT JOIN user_events e
        ON c.customer_id = e.customer_id
    WHERE e.event_timestamp IS NOT NULL
    GROUP BY c.customer_id, c.cohort_month, DATE_TRUNC('month', e.event_timestamp)::date
),

cohort_spine AS (
    SELECT DISTINCT
        cohort_month,
        activity_month,
        DATE_PART('month', AGE(activity_month, cohort_month))::int AS month_number
    FROM activity_months
    WHERE activity_month IS NOT NULL
),

retention AS (
    SELECT
        s.cohort_month,
        s.month_number,
        COUNT(DISTINCT a.customer_id) AS active_customers
    FROM cohort_spine s
    JOIN activity_months a
        ON s.cohort_month = a.cohort_month
       AND s.activity_month = a.activity_month
    GROUP BY s.cohort_month, s.month_number
),

cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(*) AS cohort_size
    FROM customer_cohorts
    GROUP BY cohort_month
)

SELECT
    r.cohort_month,
    r.month_number,
    r.active_customers,
    c.cohort_size,
    r.active_customers::numeric / c.cohort_size AS retention_rate
FROM retention r
JOIN cohort_sizes c
    ON r.cohort_month = c.cohort_month
ORDER BY r.cohort_month, r.month_number;

