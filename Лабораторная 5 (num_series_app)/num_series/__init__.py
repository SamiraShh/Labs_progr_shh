"""Пакет алгоритмической обработки числовых рядов."""

from __future__ import annotations
from .generator import random_series, sine_series, trend_series
from .stats import mean, median, spread, summarize
from .moving_average import (
    simple_moving_average,
    centered_moving_average,
    exponential_moving_average,
)


__all__ = [
    "random_series", "sine_series", "trend_series",          # Генерация
    "mean", "median", "spread", "summarize",                 # Статистика
    "simple_moving_average",                                 # Скользящие средние
    "centered_moving_average",
    "exponential_moving_average",
]


__version__ = "1.0.0"