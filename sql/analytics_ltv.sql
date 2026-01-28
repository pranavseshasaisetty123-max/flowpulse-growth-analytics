-- Customer lifetime value (LTV) at the customer level.

WITH pay AS (
    SELECT
        p.payment_id,
        s.customer_id,
        p.amount_usd,
        p.payment_status
    FROM payments p
    JOIN subscriptions s
        ON p.subscription_id = s.subscription_id
    WHERE p.payment_status = 'success'
),

ltv_per_customer AS (
    SELECT
        customer_id,
        SUM(amount_usd) AS ltv_usd,
        COUNT(DISTINCT payment_id) AS successful_payments
    FROM pay
    GROUP BY customer_id
)

SELECT
    c.customer_id,
    c.segment,
    c.country,
    c.signup_date,
    l.ltv_usd,
    l.successful_payments
FROM ltv_per_customer l
JOIN customers c
    ON l.customer_id = c.customer_id
ORDER BY l.ltv_usd DESC;

