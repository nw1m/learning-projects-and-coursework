"""Построение простого графика DAU."""

from pathlib import Path
import matplotlib.pyplot as plt


def save_dau_chart(metrics: dict, output_path: str) -> None:
    dates = list(metrics["dau"].keys())
    values = list(metrics["dau"].values())

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(9, 4.5))
    plt.plot(dates, values, marker="o")
    plt.title("DAU — активные пользователи по дням")
    plt.xlabel("Дата")
    plt.ylabel("Уникальные пользователи")
    plt.xticks(rotation=35, ha="right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()
