-- Таблица для исходного events.csv. Значения времени храним в миллисекундах UTC.
CREATE TABLE IF NOT EXISTS raw_events (
    timestamp_ms BIGINT NOT NULL,
    visitor_id BIGINT NOT NULL,
    event_type TEXT NOT NULL,
    item_id BIGINT NOT NULL,
    transaction_id BIGINT
);
