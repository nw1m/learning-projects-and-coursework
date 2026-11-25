-- Перед запуском импортируйте data/sales_demo.csv в таблицу sales через DBeaver.
-- Структура ожидаемых полей: order_id, order_date, customer_id, region, category, product, quantity, unit_price, discount, sales, profit.

-- 1. Выручка и прибыль по категориям
SELECT
    category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM sales
GROUP BY category
ORDER BY total_sales DESC;

-- 2. Выручка по регионам
SELECT
    region,
    SUM(sales) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- 3. Количество заказов и средний чек
SELECT
    COUNT(*) AS orders_count,
    AVG(order_total) AS average_order_value
FROM (
    SELECT order_id, SUM(sales) AS order_total
    FROM sales
    GROUP BY order_id
) AS orders;

-- 4. Товары с самой низкой суммарной прибылью
SELECT
    product,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM sales
GROUP BY product
ORDER BY total_profit ASC
LIMIT 5;

-- 5. Динамика выручки по месяцам (PostgreSQL)
SELECT
    DATE_TRUNC('month', order_date::date) AS month,
    SUM(sales) AS total_sales
FROM sales
GROUP BY 1
ORDER BY 1;
