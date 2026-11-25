"""Проверка совпадения результатов и сравнение времени работы."""

from statistics import median
from time import perf_counter

from .metrics_slow import calculate_metrics_slow
from .metrics_fast import calculate_metrics_fast


def benchmark_metrics(df, repeats: int = 5) -> dict:
    """
    Сначала проверяет идентичность результатов, затем замеряет время.
    В отчёт попадает медиана нескольких запусков.
    """
    slow_result = calculate_metrics_slow(df)
    fast_result = calculate_metrics_fast(df)

    if slow_result != fast_result:
        raise AssertionError("Результаты двух версий не совпадают!")

    slow_times = []
    fast_times = []

    # Первый запуск — прогрев; в итоговые замеры он не включается.
    calculate_metrics_slow(df)
    calculate_metrics_fast(df)

    for _ in range(repeats):
        start = perf_counter()
        calculate_metrics_slow(df)
        slow_times.append(perf_counter() - start)

        start = perf_counter()
        calculate_metrics_fast(df)
        fast_times.append(perf_counter() - start)

    slow_median = median(slow_times)
    fast_median = median(fast_times)

    return {
        "slow_seconds": slow_median,
        "fast_seconds": fast_median,
        "speedup": slow_median / fast_median if fast_median > 0 else None,
        "results_match": True,
        "repeats": repeats,
        "rows": int(len(df)),
    }
