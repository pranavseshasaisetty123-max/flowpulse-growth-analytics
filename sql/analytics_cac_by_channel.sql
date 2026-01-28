-- Customer acquisition cost (CAC) and estimated spend by marketing channel.

WITH acquisitions AS (
    SELECT
        mc.channel_name,
        mc.channel_id,
        COUNT(DISTINCT c.customer_id) AS acquired_customers,
        AVG(mc.cac_usd) AS avg_cac_usd
    FROM customers c
    JOIN marketing_channels mc
        ON c.acquisition_channel_id = mc.channel_id
    GROUP BY mc.channel_name, mc.channel_id
)

SELECT
    channel_name,
    acquired_customers,
    avg_cac_usd,
    acquired_customers * avg_cac_usd AS est_marketing_spend_usd
FROM acquisitions
ORDER BY est_marketing_spend_usd DESC;

