"""Оптимизированная версия расчёта метрик через pandas groupby."""

from .data_loader import ALLOWED_EVENTS


def calculate_metrics_fast(df):
    """
    Рассчитывает те же метрики с помощью groupby/nunique.
    Группировка выполняется оптимизированными операциями pandas.
    """
    dau = (
        df.groupby("event_date")["user_id"]
        .nunique()
        .sort_index()
    )

    users_by_event = (
        df.groupby("event_type")["user_id"]
        .nunique()
        .reindex(ALLOWED_EVENTS, fill_value=0)
    )

    return {
        "total_events": int(len(df)),
        "unique_users": int(df["user_id"].nunique()),
        "dau": {date: int(value) for date, value in dau.items()},
        "users_by_event": {
            event: int(users_by_event[event])
            for event in ALLOWED_EVENTS
        },
    }
