"""Первая, более простая версия расчёта метрик — проход по строкам."""

from collections import defaultdict
from .data_loader import ALLOWED_EVENTS


def calculate_metrics_slow(df):
    """
    Рассчитывает метрики, проходя по каждой строке Python-циклом.
    Эта версия нужна как baseline для сравнения.
    """
    all_users = set()
    users_by_event = {event: set() for event in ALLOWED_EVENTS}
    users_by_date = defaultdict(set)

    for row in df.itertuples(index=False):
        all_users.add(row.user_id)
        users_by_event[row.event_type].add(row.user_id)
        users_by_date[row.event_date].add(row.user_id)

    return {
        "total_events": int(len(df)),
        "unique_users": int(len(all_users)),
        "dau": {
            date: int(len(users))
            for date, users in sorted(users_by_date.items())
        },
        "users_by_event": {
            event: int(len(users_by_event[event]))
            for event in ALLOWED_EVENTS
        },
    }
