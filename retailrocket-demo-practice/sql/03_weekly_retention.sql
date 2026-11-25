-- Недельное удержание: пользователь активен, если у него есть хотя бы одно событие в неделе.
WITH user_weeks AS (
    SELECT DISTINCT
        visitor_id,
        DATE_TRUNC('week', TO_TIMESTAMP(timestamp_ms / 1000.0))::date AS activity_week
    FROM raw_events
),
cohorts AS (
    SELECT visitor_id, MIN(activity_week) AS cohort_week
    FROM user_weeks
    GROUP BY visitor_id
),
cohort_activity AS (
    SELECT
        c.cohort_week,
        ((u.activity_week - c.cohort_week) / 7)::int AS week_number,
        COUNT(DISTINCT u.visitor_id) AS active_users
    FROM cohorts c
    JOIN user_weeks u USING (visitor_id)
    GROUP BY 1, 2
),
cohort_size AS (
    SELECT cohort_week, COUNT(*) AS cohort_users
    FROM cohorts
    GROUP BY cohort_week
)
SELECT
    a.cohort_week,
    a.week_number,
    s.cohort_users,
    a.active_users,
    ROUND(100.0 * a.active_users / NULLIF(s.cohort_users, 0), 2) AS weekly_retention_pct
FROM cohort_activity a
JOIN cohort_size s USING (cohort_week)
ORDER BY a.cohort_week, a.week_number;
