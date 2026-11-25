"""
Генерация датасета онлайн-магазина и сборка базы данных SQLite.
Запуск: python build_database.py
Результат: shop.db + csv-файлы в папке data/
"""
import sqlite3
import csv
import os
import random
from datetime import date, timedelta

random.seed(42)  # фиксируем seed, чтобы данные были одинаковыми при каждом запуске

os.makedirs("data", exist_ok=True)

# ---------- Справочники ----------
CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург",
          "Казань", "Нижний Новгород", "Самара", "Краснодар"]
SEGMENTS = ["Розница", "Опт", "Корпоративный"]

CATEGORIES = {
    "Электроника": [("Смартфон", 45000), ("Ноутбук", 78000), ("Наушники", 6500),
                    ("Планшет", 32000), ("Умные часы", 18000)],
    "Бытовая техника": [("Чайник", 3500), ("Микроволновка", 12000),
                        ("Пылесос", 21000), ("Кофемашина", 38000)],
    "Аксессуары": [("Чехол", 1200), ("Зарядное устройство", 1800),
                   ("Powerbank", 4200), ("Кабель USB", 600)],
    "Канцелярия": [("Ежедневник", 900), ("Набор ручек", 450), ("Папка", 300)],
}

STATUSES = ["completed", "completed", "completed", "completed",
            "cancelled", "returned"]  # большинство выполнено

# ---------- 1. Клиенты ----------
male = ["Иван", "Алексей", "Дмитрий", "Сергей", "Павел", "Андрей"]
female = ["Мария", "Ольга", "Анна", "Елена", "Наталья", "Татьяна"]
surnames = ["Иванов", "Петров", "Смирнов", "Кузнецов", "Соколов", "Попов",
            "Лебедев", "Козлов", "Новиков", "Морозов", "Волков", "Зайцев"]

customers = []
start = date(2023, 1, 1)
for cid in range(1, 81):  # 80 клиентов
    if random.random() < 0.5:
        fname = random.choice(male)
        sname = random.choice(surnames)          # мужская фамилия
    else:
        fname = random.choice(female)
        sname = random.choice(surnames) + "а"     # женская фамилия (Иванова и т.п.)
    name = f"{fname} {sname}"
    city = random.choice(CITIES)
    seg = random.choices(SEGMENTS, weights=[6, 2, 2])[0]
    signup = start + timedelta(days=random.randint(0, 540))
    customers.append((cid, name, city, seg, signup.isoformat()))

# ---------- 2. Товары ----------
products = []
pid = 1
for cat, items in CATEGORIES.items():
    for pname, price in items:
        products.append((pid, pname, cat, price))
        pid += 1

# ---------- 3. Заказы и позиции заказов ----------
orders = []
order_items = []
oid = 1
item_id = 1
for _ in range(600):  # 600 заказов
    cust = random.choice(customers)
    cid = cust[0]
    # заказ не раньше регистрации клиента
    signup_date = date.fromisoformat(cust[4])
    max_days = (date(2024, 12, 31) - signup_date).days
    if max_days < 1:
        continue
    odate = signup_date + timedelta(days=random.randint(1, max_days))
    status = random.choice(STATUSES)
    orders.append((oid, cid, odate.isoformat(), status))

    # 1-4 позиции в заказе
    for _ in range(random.randint(1, 4)):
        prod = random.choice(products)
        qty = random.randint(1, 3)
        # цена в заказе чуть отличается от прайса (скидки/акции)
        unit_price = round(prod[3] * random.uniform(0.9, 1.0))
        order_items.append((item_id, oid, prod[0], qty, unit_price))
        item_id += 1
    oid += 1

# ---------- Запись CSV (для просмотра на GitHub) ----------
def dump_csv(name, header, rows):
    with open(f"data/{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

dump_csv("customers", ["customer_id", "name", "city", "segment", "signup_date"], customers)
dump_csv("products", ["product_id", "name", "category", "price"], products)
dump_csv("orders", ["order_id", "customer_id", "order_date", "status"], orders)
dump_csv("order_items", ["order_item_id", "order_id", "product_id", "quantity", "unit_price"], order_items)

# ---------- Сборка SQLite ----------
if os.path.exists("shop.db"):
    os.remove("shop.db")
conn = sqlite3.connect("shop.db")
cur = conn.cursor()

cur.executescript("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    city        TEXT,
    segment     TEXT,
    signup_date TEXT
);
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT,
    price      INTEGER
);
CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date  TEXT,
    status      TEXT
);
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER REFERENCES orders(order_id),
    product_id    INTEGER REFERENCES products(product_id),
    quantity      INTEGER,
    unit_price    INTEGER
);
""")

cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)
cur.executemany("INSERT INTO products VALUES (?,?,?,?)", products)
cur.executemany("INSERT INTO orders VALUES (?,?,?,?)", orders)
cur.executemany("INSERT INTO order_items VALUES (?,?,?,?,?)", order_items)
conn.commit()

print("Готово.")
print("Клиентов:", len(customers))
print("Товаров:", len(products))
print("Заказов:", len(orders))
print("Позиций в заказах:", len(order_items))
conn.close()
