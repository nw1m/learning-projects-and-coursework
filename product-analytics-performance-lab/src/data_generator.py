"""Создание учебного набора событий приложения."""

from datetime import datetime, timedelta
import random
import pandas as pd


def generate_events(
    n_users: int = 3500,
    days: int = 14,
    seed: int = 42,
    activity_probability: float = 0.25,
    duplicate_rate: float = 0.01,
    invalid_rows: int = 5,
) -> pd.DataFrame:
    """
    Генерирует искусственные события приложения.

    Для активного пользователя в конкретный день создаётся app_open.
    Дальнейшие события образуют простую воронку:
    app_open -> product_view -> add_to_cart -> purchase.
    """
    rng = random.Random(seed)
    start_date = datetime(2026, 1, 1)
    rows = []
    event_number = 1

    def add_event(user_id, event_type, event_time, product_id=""):
        nonlocal event_number
        rows.append({
            "event_id": f"event_{event_number:07d}",
            "user_id": user_id,
            "event_type": event_type,
            "event_time": event_time.isoformat(sep=" "),
            "product_id": product_id,
        })
        event_number += 1

    for user_number in range(1, n_users + 1):
        user_id = f"user_{user_number:05d}"

        for day_number in range(days):
            if rng.random() > activity_probability:
                continue

            day_start = start_date + timedelta(days=day_number)
            event_time = day_start + timedelta(
                hours=rng.randint(8, 22),
                minutes=rng.randint(0, 59),
                seconds=rng.randint(0, 59),
            )
            add_event(user_id, "app_open", event_time)

            # Следующие события происходят с заданной вероятностью.
            if rng.random() < 0.75:
                event_time += timedelta(minutes=rng.randint(1, 8))
                product_id = f"product_{rng.randint(1, 80):03d}"
                add_event(user_id, "product_view", event_time, product_id)

                if rng.random() < 0.35:
                    event_time += timedelta(minutes=rng.randint(1, 5))
                    add_event(user_id, "add_to_cart", event_time, product_id)

                    if rng.random() < 0.50:
                        event_time += timedelta(minutes=rng.randint(1, 10))
                        add_event(user_id, "purchase", event_time, product_id)

    # Добавляем небольшое количество дублей с тем же event_id.
    if rows and duplicate_rate > 0:
        duplicate_count = max(1, int(len(rows) * duplicate_rate))
        for _ in range(duplicate_count):
            rows.append(dict(rng.choice(rows)))

    # Добавляем намеренно некорректные строки, чтобы показать очистку данных.
    for i in range(invalid_rows):
        rows.append({
            "event_id": f"invalid_{i:03d}",
            "user_id": "" if i % 2 == 0 else f"user_bad_{i}",
            "event_type": "unknown_event" if i % 2 == 1 else "app_open",
            "event_time": "not-a-date" if i == 0 else "2026-01-01 12:00:00",
            "product_id": "",
        })

    return pd.DataFrame(rows)


def save_sample_dataset(path: str, **kwargs) -> None:
    """Создаёт CSV с учебными данными."""
    df = generate_events(**kwargs)
    df.to_csv(path, index=False)
