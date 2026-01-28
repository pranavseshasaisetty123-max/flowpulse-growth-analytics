-- Identify the top 20% of customers by LTV and their revenue share.

WITH pay AS (
    SELECT
        p.payment_id,
        s.customer_id,
        p.amount_usd
    FROM payments p
    JOIN subscriptions s
        ON p.subscription_id = s.subscription_id
    WHERE p.payment_status = 'success'
),

ltv AS (
    SELECT
        customer_id,
        SUM(amount_usd) AS ltv_usd
    FROM pay
    GROUP BY customer_id
),

ltv_ranked AS (
    SELECT
        customer_id,
        ltv_usd,
        NTILE(5) OVER (ORDER BY ltv_usd DESC) AS quintile,
        SUM(ltv_usd) OVER () AS total_revenue
    FROM ltv
)

SELECT
    CASE WHEN quintile = 1 THEN 'Top 20%' ELSE 'Others' END AS customer_bucket,
    COUNT(*) AS num_customers,
    SUM(ltv_usd) AS bucket_revenue,
    MAX(total_revenue) AS total_revenue,
    SUM(ltv_usd) / MAX(total_revenue) AS revenue_share
FROM ltv_ranked
GROUP BY CASE WHEN quintile = 1 THEN 'Top 20%' ELSE 'Others' END
ORDER BY revenue_share DESC;

