-- Сравнение конверсии по устройствам.
SELECT
    device,
    COUNT(DISTINCT CASE WHEN event_name = 'visit' THEN session_id END) AS visits,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN session_id END) AS purchases,
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN session_id END)
        / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'visit' THEN session_id END), 0),
        2
    ) AS conversion_pct
FROM events
GROUP BY device
ORDER BY conversion_pct DESC;
