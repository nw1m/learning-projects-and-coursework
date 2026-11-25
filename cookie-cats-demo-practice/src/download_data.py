from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "raw" / "cookie_cats.csv"
TARGET.parent.mkdir(parents=True, exist_ok=True)

URLS = [
    "https://raw.githubusercontent.com/nsy0079/cookie-cats-ab-test/main/data/cookie_cats.csv",
    "https://raw.githubusercontent.com/ryanschaub/Mobile-Games-A-B-Testing-with-Cookie-Cats/master/cookie_cats.csv",
]

if TARGET.exists():
    print("Файл уже существует:", TARGET)
    raise SystemExit(0)

for url in URLS:
    try:
        print("Пробую скачать:", url)
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        if not response.text.lower().startswith("userid,"):
            raise ValueError("Ответ не похож на CSV Cookie Cats")
        TARGET.write_bytes(response.content)
        print("Готово:", TARGET, "Размер:", len(response.content), "байт")
        break
    except Exception as exc:
        print("Не получилось:", exc)
else:
    print("Автоматическое скачивание не удалось.")
    print("Скачайте CSV вручную со страницы Kaggle:")
    print("https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats")
    print("Сохраните файл под именем:", TARGET)
    raise SystemExit(1)
