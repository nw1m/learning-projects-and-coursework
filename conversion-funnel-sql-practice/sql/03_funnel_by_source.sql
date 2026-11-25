-- Сравнение воронки по источникам трафика.
WITH funnel AS (
    SELECT
        source,
        COUNT(DISTINCT CASE WHEN event_name = 'visit' THEN session_id END) AS visits,
        COUNT(DISTINCT CASE WHEN event_name = 'view_product' THEN session_id END) AS product_views,
        COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN session_id END) AS carts,
        COUNT(DISTINCT CASE WHEN event_name = 'checkout' THEN session_id END) AS checkouts,
        COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN session_id END) AS purchases
    FROM events
    GROUP BY source
)
SELECT
    source,
    visits,
    product_views,
    carts,
    checkouts,
    purchases,
    ROUND(100.0 * purchases / NULLIF(visits, 0), 2) AS conversion_pct
FROM funnel
ORDER BY conversion_pct DESC;
