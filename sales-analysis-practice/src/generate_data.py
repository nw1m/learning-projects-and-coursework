from pathlib import Path
import numpy as np
import pandas as pd

# Учебные синтетические данные. Не реальные заказы компании.
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sales_demo.csv"
OUT.parent.mkdir(exist_ok=True)
rng = np.random.default_rng(20261121)
n_orders = 1250
order_ids = [f"ORD-{i:05d}" for i in range(1, n_orders + 1)]
order_dates = pd.to_datetime(rng.choice(pd.date_range("2025-01-01", "2025-12-31"), size=n_orders))
customer_ids = [f"CUST-{x:04d}" for x in rng.integers(1, 520, size=n_orders)]
regions = ["Северо-Запад", "Центр", "Юг", "Урал", "Сибирь"]
catalog = {
    "Электроника": [("Наушники", 2200, 1250), ("Мышь", 900, 430), ("Клавиатура", 2800, 1650), ("Колонка", 3900, 2450)],
    "Дом": [("Лампа", 1400, 650), ("Органайзер", 750, 320), ("Плед", 2100, 1020), ("Посуда", 1600, 760)],
    "Канцелярия": [("Тетрадь", 180, 75), ("Ручка", 90, 28), ("Папка", 250, 100), ("Блокнот", 330, 130)],
}
rows = []
for i, order_id in enumerate(order_ids):
    region = str(rng.choice(regions, p=[.26, .28, .18, .14, .14]))
    n_items = int(rng.choice([1, 2, 3, 4], p=[.48, .32, .15, .05]))
    for _ in range(n_items):
        category = str(rng.choice(list(catalog), p=[.38, .34, .28]))
        product, price, cost = catalog[category][int(rng.integers(0, len(catalog[category])))]
        quantity = int(rng.choice([1, 2, 3, 4], p=[.62, .25, .10, .03]))
        discount = float(rng.choice([0, .05, .10, .15, .20], p=[.40, .20, .22, .13, .05]))
        sales = round(quantity * price * (1 - discount), 2)
        profit = round(sales - quantity * cost, 2)
        rows.append([order_id, order_dates[i].strftime("%Y-%m-%d"), customer_ids[i], region, category, product, quantity, price, discount, sales, profit])
columns = ["order_id", "order_date", "customer_id", "region", "category", "product", "quantity", "unit_price", "discount", "sales", "profit"]
pd.DataFrame(rows, columns=columns).to_csv(OUT, index=False, encoding="utf-8-sig")
print(f"Saved {len(rows)} rows to {OUT}")
