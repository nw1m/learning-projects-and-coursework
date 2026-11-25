"""Загрузка и простая очистка событий."""

import pandas as pd

REQUIRED_COLUMNS = {
    "event_id", "user_id", "event_type", "event_time", "product_id"
}

ALLOWED_EVENTS = ["app_open", "product_view", "add_to_cart", "purchase"]


def load_events(path: str) -> pd.DataFrame:
    """Загружает CSV и проверяет наличие обязательных столбцов."""
    df = pd.read_csv(path)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"В CSV не хватает обязательных столбцов: {missing}")

    return df


def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Удаляет дубли, пустые значения, неизвестные события
    и строки с некорректной датой.
    """
    clean = df.copy()

    clean = clean.dropna(subset=["event_id", "user_id", "event_type", "event_time"])
    clean["event_id"] = clean["event_id"].astype(str).str.strip()
    clean["user_id"] = clean["user_id"].astype(str).str.strip()
    clean["event_type"] = clean["event_type"].astype(str).str.strip()

    clean = clean[
        (clean["event_id"] != "") &
        (clean["user_id"] != "") &
        (clean["event_type"].isin(ALLOWED_EVENTS))
    ]

    clean["event_time"] = pd.to_datetime(clean["event_time"], errors="coerce")
    clean = clean.dropna(subset=["event_time"])

    # Один event_id должен соответствовать одному событию.
    clean = clean.drop_duplicates(subset=["event_id"], keep="first")

    clean["event_date"] = clean["event_time"].dt.strftime("%Y-%m-%d")
    return clean.reset_index(drop=True)
