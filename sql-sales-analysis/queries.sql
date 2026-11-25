-- ============================================================
--  Анализ продаж онлайн-магазина (SQLite)
--  Запуск:  sqlite3 shop.db < queries.sql
--  Таблицы: customers, products, orders, order_items
-- ============================================================


-- 1. Общие показатели магазина: сколько заказов и клиентов в базе
SELECT
    COUNT(DISTINCT order_id)    AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers
FROM orders;


-- 2. Общая выручка по выполненным заказам
--    (считаем только status = 'completed', отменённые и возвраты не берём)
SELECT
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'completed';


-- 3. Средний чек (средняя сумма одного выполненного заказа)
SELECT
    ROUND(AVG(order_sum), 0) AS avg_order_value
FROM (
    SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS order_sum
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY o.order_id
);


-- 4. Топ-5 клиентов по сумме покупок
SELECT
    c.customer_id,
    c.name,
    c.city,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name, c.city
ORDER BY revenue DESC
LIMIT 5;


-- 5. Выручка по категориям товаров
SELECT
    p.category,
    SUM(oi.quantity * oi.unit_price) AS revenue,
    SUM(oi.quantity)                 AS units_sold
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o       ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;


-- 6. Топ-5 товаров по количеству проданных штук
SELECT
    p.name,
    p.category,
    SUM(oi.quantity) AS units_sold
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o       ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.name, p.category
ORDER BY units_sold DESC
LIMIT 5;


-- 7. Помесячная динамика выручки
SELECT
    strftime('%Y-%m', o.order_date)  AS month,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month
ORDER BY month;


-- 8. Заказы по статусам и их доля
SELECT
    status,
    COUNT(*)                                   AS orders_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 1) AS share_pct
FROM orders
GROUP BY status
ORDER BY orders_count DESC;


-- 9. Выручка по сегментам клиентов
SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id)    AS customers,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY c.segment
ORDER BY revenue DESC;


-- 10. Количество клиентов по городам
SELECT
    city,
    COUNT(*) AS customers
FROM customers
GROUP BY city
ORDER BY customers DESC;


-- 11. Среднее количество позиций в одном заказе
SELECT
    ROUND(AVG(items_in_order), 2) AS avg_items_per_order
FROM (
    SELECT order_id, COUNT(*) AS items_in_order
    FROM order_items
    GROUP BY order_id
);


-- 12. Повторные клиенты: у кого больше одного выполненного заказа
--     (используем HAVING для фильтрации по агрегату)
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 1
ORDER BY orders_count DESC
LIMIT 10;


-- 13. Дорогие заказы: выполненные заказы на сумму свыше 100 000 руб.
SELECT
    o.order_id,
    o.order_date,
    c.name,
    SUM(oi.quantity * oi.unit_price) AS order_sum
FROM orders o
JOIN customers c    ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY o.order_id, o.order_date, c.name
HAVING SUM(oi.quantity * oi.unit_price) > 100000
ORDER BY order_sum DESC;


-- 14. Сколько новых клиентов регистрировалось по месяцам
SELECT
    strftime('%Y-%m', signup_date) AS month,
    COUNT(*)                       AS new_customers
FROM customers
GROUP BY month
ORDER BY month;


-- 15. Доля отмен и возвратов в общем числе заказов (в процентах)
SELECT
    ROUND(
        SUM(CASE WHEN status IN ('cancelled', 'returned') THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 1
    ) AS cancel_return_rate_pct
FROM orders;
