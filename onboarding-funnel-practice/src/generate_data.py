from pathlib import Path
import numpy as np
import pandas as pd

# Учебная симуляция событий приложения, не реальные пользовательские данные.
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "events_demo.csv"
OUT.parent.mkdir(exist_ok=True)
rng = np.random.default_rng(20261122)
n_users = 2500
users = [f"U{i:05d}" for i in range(1, n_users + 1)]
devices = rng.choice(["Android", "iOS", "Web"], size=n_users, p=[.48, .37, .15])
sources = rng.choice(["Поиск", "Реклама", "Соцсети", "Прямой переход"], size=n_users, p=[.35, .28, .22, .15])
dates = pd.to_datetime(rng.choice(pd.date_range("2025-09-01", "2025-09-30"), size=n_users))
rows = []
for i, user in enumerate(users):
    t0 = dates[i] + pd.Timedelta(minutes=int(rng.integers(0, 24*60)))
    device, source = devices[i], sources[i]
    rows.append([user, "visit_landing", t0, device, source])
    if rng.random() < .46:
        t1 = t0 + pd.Timedelta(minutes=int(rng.integers(1, 80)))
        rows.append([user, "sign_up", t1, device, source])
        if rng.random() < .72:
            t2 = t1 + pd.Timedelta(minutes=int(rng.integers(2, 180)))
            rows.append([user, "complete_profile", t2, device, source])
            if rng.random() < .63:
                t3 = t2 + pd.Timedelta(minutes=int(rng.integers(1, 240)))
                rows.append([user, "first_key_action", t3, device, source])
df = pd.DataFrame(rows, columns=["user_id", "event_name", "event_time", "device", "source"])
df["event_time"] = pd.to_datetime(df["event_time"]).dt.strftime("%Y-%m-%d %H:%M:%S")
df.to_csv(OUT, index=False, encoding="utf-8-sig")
print(f"Saved {len(df)} events to {OUT}")
