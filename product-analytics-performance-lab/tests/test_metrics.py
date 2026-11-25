"""Тесты для проверки корректности расчёта метрик."""

from src.data_generator import generate_events
from src.data_loader import clean_events
from src.metrics_slow import calculate_metrics_slow
from src.metrics_fast import calculate_metrics_fast


def test_slow_and_fast_results_are_equal():
    raw = generate_events(
        n_users=80,
        days=5,
        seed=7,
        activity_probability=0.4,
        duplicate_rate=0.05,
        invalid_rows=4,
    )
    clean = clean_events(raw)

    assert calculate_metrics_slow(clean) == calculate_metrics_fast(clean)


def test_cleaning_removes_duplicate_event_ids():
    raw = generate_events(
        n_users=30,
        days=4,
        seed=10,
        activity_probability=0.6,
        duplicate_rate=0.2,
        invalid_rows=0,
    )
    clean = clean_events(raw)

    assert clean["event_id"].is_unique


def test_dau_is_not_greater_than_unique_users():
    raw = generate_events(
        n_users=50,
        days=4,
        seed=11,
        activity_probability=0.5,
        invalid_rows=0,
    )
    clean = clean_events(raw)
    metrics = calculate_metrics_fast(clean)

    assert all(value <= metrics["unique_users"] for value in metrics["dau"].values())
