-- Revenue leakage from failed/refunded payments and monthly churn counts.

WITH payments_labeled AS (
    SELECT
        p.payment_date,
        DATE_TRUNC('month', p.payment_date)::date AS month,
        p.amount_usd,
        p.payment_status
    FROM payments p
),

monthly_leakage AS (
    SELECT
        month,
        SUM(CASE WHEN payment_status = 'success'  THEN amount_usd ELSE 0 END) AS successful_revenue,
        SUM(CASE WHEN payment_status = 'failed'   THEN amount_usd ELSE 0 END) AS failed_amount,
        SUM(CASE WHEN payment_status = 'refunded' THEN amount_usd ELSE 0 END) AS refunded_amount
    FROM payments_labeled
    GROUP BY month
),

churned_customers AS (
    SELECT
        DATE_TRUNC('month', churned_date)::date AS churn_month,
        COUNT(*) AS churned_customers
    FROM customers
    WHERE churned_date IS NOT NULL
    GROUP BY DATE_TRUNC('month', churned_date)::date
)

SELECT
    m.month,
    m.successful_revenue,
    m.failed_amount,
    m.refunded_amount,
    (m.failed_amount + m.refunded_amount) AS revenue_leakage_usd,
    c.churned_customers
FROM monthly_leakage m
LEFT JOIN churned_customers c
    ON m.month = c.churn_month
ORDER BY m.month;

