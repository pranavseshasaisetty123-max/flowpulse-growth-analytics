-- Monthly recurring revenue (MRR) and month-over-month growth.

WITH payments_clean AS (
    SELECT
        payment_id,
        subscription_id,
        payment_date,
        DATE_TRUNC('month', payment_date)::date AS month,
        amount_usd,
        payment_status
    FROM payments
    WHERE payment_status = 'success'
),

monthly_revenue AS (
    SELECT
        month,
        SUM(amount_usd) AS mrr_usd
    FROM payments_clean
    GROUP BY month
),

monthly_revenue_with_growth AS (
    SELECT
        month,
        mrr_usd,
        LAG(mrr_usd) OVER (ORDER BY month) AS prev_mrr_usd,
        CASE
            WHEN LAG(mrr_usd) OVER (ORDER BY month) IS NULL THEN NULL
            WHEN LAG(mrr_usd) OVER (ORDER BY month) = 0 THEN NULL
            ELSE (mrr_usd - LAG(mrr_usd) OVER (ORDER BY month))
                 / LAG(mrr_usd) OVER (ORDER BY month)::numeric
        END AS mrr_growth_rate
    FROM monthly_revenue
)
SELECT *
FROM monthly_revenue_with_growth
ORDER BY month;

