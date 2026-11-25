-- Перед запуском импортируйте data/events_demo.csv в таблицу events через DBeaver.
-- Поля: user_id, event_name, event_time, device, source.

-- 1. Количество уникальных пользователей на каждом шаге
SELECT
    event_name,
    COUNT(DISTINCT user_id) AS users_count
FROM events
GROUP BY event_name
ORDER BY users_count DESC;

-- 2. Пользователи по устройствам
SELECT
    device,
    COUNT(DISTINCT user_id) AS users_count
FROM events
GROUP BY device
ORDER BY users_count DESC;

-- 3. Количество пользователей по источникам трафика
SELECT
    source,
    COUNT(DISTINCT user_id) AS users_count
FROM events
WHERE event_name = 'visit_landing'
GROUP BY source
ORDER BY users_count DESC;

-- 4. Число пользователей, совершивших первое целевое действие
SELECT COUNT(DISTINCT user_id) AS users_with_first_action
FROM events
WHERE event_name = 'first_key_action';
