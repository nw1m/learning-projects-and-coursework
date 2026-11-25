-- Таблица событий. Одна строка = одно событие пользователя.
CREATE TABLE IF NOT EXISTS events (
    event_id BIGINT PRIMARY KEY,
    session_id VARCHAR(20) NOT NULL,
    user_id VARCHAR(20) NOT NULL,
    event_name VARCHAR(30) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    device VARCHAR(20) NOT NULL,
    source VARCHAR(30) NOT NULL,
    CONSTRAINT chk_event_name CHECK (
        event_name IN ('visit', 'view_product', 'add_to_cart', 'checkout', 'purchase')
    )
);
