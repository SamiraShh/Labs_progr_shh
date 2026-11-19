"""Модуль расчёта базовых статистических показателей."""

from __future__ import annotations
from typing import Dict, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    """Проверка, что числовой ряд не пуст (принцип fail fast)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")


def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)


def median(data: Sequence[float]) -> float:
    """Медиана (устойчива к выбросам)."""
    _ensure_not_empty(data)
    s = sorted(data)
    k = len(s) // 2
    if len(s) % 2:
        return float(s[k])
    return (s[k - 1] + s[k]) / 2.0


def spread(data: Sequence[float]) -> float:
    """Размах ряда: max - min."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))

# Вариант 8
def trimmed_mean(data: Sequence[float], proportion: float = 0.1) -> float:
    """Устойчивая статистика: усечённое среднее (по умолчанию 10% с каждого конца)."""
    _ensure_not_empty(data)
    if not (0.0 <= proportion < 0.5):
        raise ValueError(
            f"proportion должно быть в диапазоне [0.0, 0.5) (получено: {proportion})"
        )
    s = sorted(data)
    k = int(len(s) * proportion)
    if k == 0:
        return mean(data)
    trimmed = s[k : len(s) - k]
    if not trimmed:
        return mean(data)
    return sum(trimmed) / len(trimmed)


def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Сводный отчёт: count, mean, median, spread, min, max, trimmed_mean_10."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
        "trimmed_mean_10": trimmed_mean(data, proportion=0.1),
    }