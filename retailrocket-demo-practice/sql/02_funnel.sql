-- Упрощённая пользовательская воронка.
-- События должны идти последовательно по времени: view -> addtocart -> transaction.
-- Это не session funnel и не проверка одного и того же товара.
WITH first_view AS (
    SELECT visitor_id, MIN(timestamp_ms) AS first_view_ms
    FROM raw_events
    WHERE event_type = 'view'
    GROUP BY visitor_id
),
first_cart_after_view AS (
    SELECT v.visitor_id, MIN(e.timestamp_ms) AS first_cart_ms
    FROM first_view v
    JOIN raw_events e
      ON e.visitor_id = v.visitor_id
     AND e.event_type = 'addtocart'
     AND e.timestamp_ms >= v.first_view_ms
    GROUP BY v.visitor_id
),
first_purchase_after_cart AS (
    SELECT c.visitor_id, MIN(e.timestamp_ms) AS first_purchase_ms
    FROM first_cart_after_view c
    JOIN raw_events e
      ON e.visitor_id = c.visitor_id
     AND e.event_type = 'transaction'
     AND e.timestamp_ms >= c.first_cart_ms
    GROUP BY c.visitor_id
),
steps AS (
    SELECT
        v.visitor_id,
        (c.visitor_id IS NOT NULL) AS reached_cart,
        (p.visitor_id IS NOT NULL) AS reached_purchase
    FROM first_view v
    LEFT JOIN first_cart_after_view c USING (visitor_id)
    LEFT JOIN first_purchase_after_cart p USING (visitor_id)
)
SELECT
    COUNT(*) AS viewed_users,
    COUNT(*) FILTER (WHERE reached_cart) AS cart_users,
    COUNT(*) FILTER (WHERE reached_purchase) AS purchased_users,
    ROUND(100.0 * COUNT(*) FILTER (WHERE reached_cart) / NULLIF(COUNT(*), 0), 2) AS view_to_cart_pct,
    ROUND(100.0 * COUNT(*) FILTER (WHERE reached_purchase) / NULLIF(COUNT(*) FILTER (WHERE reached_cart), 0), 2) AS cart_to_purchase_pct,
    ROUND(100.0 * COUNT(*) FILTER (WHERE reached_purchase) / NULLIF(COUNT(*), 0), 2) AS view_to_purchase_pct
FROM steps;
