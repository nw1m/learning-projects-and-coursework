"""Запуск учебного проекта Product Analytics Performance Lab."""

from pathlib import Path
import pandas as pd

from src.data_loader import load_events, clean_events
from src.data_generator import generate_events
from src.metrics_slow import calculate_metrics_slow
from src.metrics_fast import calculate_metrics_fast
from src.benchmark import benchmark_metrics
from src.visualization import save_dau_chart


BASE_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = BASE_DIR / "data" / "sample_events.csv"
RESULTS_DIR = BASE_DIR / "results"


def print_metrics(metrics: dict) -> None:
    print("\nОСНОВНЫЕ МЕТРИКИ")
    print(f"Количество событий: {metrics['total_events']}")
    print(f"Уникальных пользователей: {metrics['unique_users']}")

    print("\nПОЛЬЗОВАТЕЛИ ПО СОБЫТИЯМ")
    for event, count in metrics["users_by_event"].items():
        print(f"{event:15} {count}")

    print("\nDAU ПО ДНЯМ")
    for date, count in metrics["dau"].items():
        print(f"{date}: {count}")


def main():
    print("=" * 58)
    print("PRODUCT ANALYTICS PERFORMANCE LAB")
    print("=" * 58)

    # 1. Загружаем и очищаем небольшой пример.
    raw_df = load_events(str(SAMPLE_PATH))
    clean_df = clean_events(raw_df)

    print(f"\nСтрок до очистки:    {len(raw_df)}")
    print(f"Строк после очистки: {len(clean_df)}")
    print(f"Удалено строк:       {len(raw_df) - len(clean_df)}")

    # 2. Рассчитываем метрики двумя способами.
    metrics = calculate_metrics_fast(clean_df)
    print_metrics(metrics)

    # 3. Сохраняем график DAU.
    RESULTS_DIR.mkdir(exist_ok=True)
    chart_path = RESULTS_DIR / "dau_chart.png"
    save_dau_chart(metrics, str(chart_path))
    print(f"\nГрафик сохранён: {chart_path.relative_to(BASE_DIR)}")

    # 4. Создаём более крупный датасет только для честного замера скорости.
    print("\nСРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    benchmark_raw = generate_events(
        n_users=3500,
        days=14,
        seed=2026,
        activity_probability=0.25,
        duplicate_rate=0.01,
        invalid_rows=10,
    )
    benchmark_df = clean_events(benchmark_raw)
    result = benchmark_metrics(benchmark_df, repeats=5)

    print(f"Строк в тестовом датасете: {result['rows']}")
    print(f"Версия с циклом:           {result['slow_seconds']:.5f} сек.")
    print(f"Версия с pandas groupby:   {result['fast_seconds']:.5f} сек.")
    print(f"Результаты совпадают:      {result['results_match']}")

    if result["speedup"] is not None:
        print(f"Ускорение примерно в:      {result['speedup']:.2f} раза")

    benchmark_table = pd.DataFrame([
        {"version": "python_loop", "time_seconds": result["slow_seconds"]},
        {"version": "pandas_groupby", "time_seconds": result["fast_seconds"]},
    ])
    benchmark_table.to_csv(RESULTS_DIR / "benchmark_results.csv", index=False)

    print("\nЗамеры сохранены: results/benchmark_results.csv")
    print("\nГотово. Проект выполнен успешно.")


if __name__ == "__main__":
    main()
