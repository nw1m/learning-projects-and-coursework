-- Общая воронка по всем сессиям.
SELECT
    COUNT(DISTINCT CASE WHEN event_name = 'visit' THEN session_id END) AS visits,
    COUNT(DISTINCT CASE WHEN event_name = 'view_product' THEN session_id END) AS product_views,
    COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN session_id END) AS add_to_cart,
    COUNT(DISTINCT CASE WHEN event_name = 'checkout' THEN session_id END) AS checkouts,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN session_id END) AS purchases,
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN session_id END)
        / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'visit' THEN session_id END), 0),
        2
    ) AS visit_to_purchase_conversion_pct
FROM events;
