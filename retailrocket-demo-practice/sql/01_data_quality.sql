-- 1. Объём данных и диапазон дат
SELECT
    COUNT(*) AS event_rows,
    COUNT(DISTINCT visitor_id) AS unique_visitors,
    COUNT(DISTINCT item_id) AS unique_items,
    MIN(to_timestamp(timestamp_ms / 1000.0)) AS first_event_at,
    MAX(to_timestamp(timestamp_ms / 1000.0)) AS last_event_at
FROM raw_events;

-- 2. Типы событий
SELECT event_type, COUNT(*) AS events
FROM raw_events
GROUP BY event_type
ORDER BY events DESC;

-- 3. Проверка неизвестных типов и NULL
SELECT
    COUNT(*) FILTER (WHERE event_type NOT IN ('view', 'addtocart', 'transaction')) AS unknown_event_types,
    COUNT(*) FILTER (WHERE visitor_id IS NULL) AS null_visitors,
    COUNT(*) FILTER (WHERE item_id IS NULL) AS null_items,
    COUNT(*) FILTER (WHERE event_type = 'transaction' AND transaction_id IS NULL) AS transactions_without_id
FROM raw_events;

-- 4. Полные дубли строк
SELECT timestamp_ms, visitor_id, event_type, item_id, transaction_id, COUNT(*) AS copies
FROM raw_events
GROUP BY 1,2,3,4,5
HAVING COUNT(*) > 1
ORDER BY copies DESC
LIMIT 20;
