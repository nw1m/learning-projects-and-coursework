from pathlib import Path
import subprocess
import shutil

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

if (RAW / "events.csv").exists():
    print("events.csv уже найден:", RAW / "events.csv")
    raise SystemExit(0)

kaggle_cli = shutil.which("kaggle")
if kaggle_cli is None:
    print("Команда kaggle не найдена. Установите пакет kaggle и настройте API-токен.")
    raise SystemExit(1)

try:
    subprocess.run(
        [kaggle_cli, "datasets", "download", "-d", "retailrocket/ecommerce-dataset", "-p", str(RAW), "--unzip"],
        check=True,
    )
except subprocess.CalledProcessError:
    print("Скачивание не удалось. Проверьте Kaggle API token и доступ к датасету.")
    print("Альтернатива: скачайте архив вручную со страницы https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset")
    raise SystemExit(1)

if not (RAW / "events.csv").exists():
    print("Архив распакован, но events.csv не найден. Проверьте содержимое:", RAW)
    raise SystemExit(1)

print("Готово:", RAW / "events.csv")
