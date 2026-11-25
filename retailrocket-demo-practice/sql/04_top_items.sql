SELECT
    item_id,
    COUNT(*) FILTER (WHERE event_type = 'view') AS views,
    COUNT(*) FILTER (WHERE event_type = 'addtocart') AS cart_adds,
    COUNT(*) FILTER (WHERE event_type = 'transaction') AS purchase_events,
    COUNT(DISTINCT visitor_id) FILTER (WHERE event_type = 'transaction') AS buyers
FROM raw_events
GROUP BY item_id
ORDER BY purchase_events DESC, views DESC
LIMIT 20;
