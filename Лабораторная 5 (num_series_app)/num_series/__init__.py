"""Пакет алгоритмической обработки числовых рядов."""

from __future__ import annotations
from .generator import random_series, sine_series, trend_series
from .stats import mean, median, spread, summarize
from .moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
    benchmark_moving_average,
)
from .io_json import save_series_json, load_series_json
from .io_file import load_series_txt, load_series_csv, load_series_auto


__all__ = [
    "random_series", "sine_series", "trend_series",          # Генерация
    "mean", "median", "spread", "summarize",                 # Статистика
    "simple_moving_average",                                 # Скользящие средние
    "centered_moving_average",
    "exponential_moving_average",
    "save_series_json", "load_series_json",                  # Ввод-вывод
    "load_series_txt", "load_series_csv", "load_series_auto"
    "simple_moving_average",                                 # Из deque
    "simple_moving_average_deque",
    "centered_moving_average",
    "exponential_moving_average",
    "benchmark_moving_average"
]


__version__ = "1.1.0"