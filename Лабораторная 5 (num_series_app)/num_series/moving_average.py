"""Модуль вычисления скользящих средних (SMA, CMA, EMA)."""

from __future__ import annotations
from typing import Sequence, List


def _check_window(window: int, n: int) -> None:
    """Проверка корректности размера окна."""
    if window < 1:
        raise ValueError(f"Размер окна должен быть >= 1 (получено: {window})")
    if window > n:
        raise ValueError(f"Размер окна ({window}) больше длины ряда ({n})")


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Простая скользящая средняя (SMA) через эффективную бегущую сумму O(n)."""
    if not data:
        return []
    _check_window(window, len(data))

    running = sum(data[:window])
    result = [running / window]

    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)

    return result


def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированная скользящая средняя (требует нечетное окно)."""
    if window % 2 == 0:
        raise ValueError("Для центрированного МА размер окна должен быть нечетным")
  
    sma = simple_moving_average(data, window)
    k = window // 2
    # Сглаживаем SMA попарно для выравнивания по центру
    return [(sma[i] + sma[i + 1]) / 2.0 for i in range(len(sma) - 1)]


def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """Экспоненциальная скользящая средняя (EMA)."""
    if not data:
        return []
    if not (0.0 < alpha <= 1.0):
        raise ValueError(f"alpha должна быть в диапазоне (0, 1] (получено: {alpha})")

    ema = [data[0]]
    for i in range(1, len(data)):
        val = alpha * data[i] + (1 - alpha) * ema[-1]
        ema.append(val)
    return ema