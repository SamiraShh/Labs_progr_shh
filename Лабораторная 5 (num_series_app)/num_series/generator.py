"""Модуль генерации числовых рядов (случайные, синусоида, тренд)."""

from __future__ import annotations
import math
import random
from typing import List, Optional


def _validate_n(n: int) -> None:
    """Проверка, что n — положительное целое число."""
    try:
        is_positive_int = (n > 0) and (int(n) == n)
    except (TypeError, ValueError) as err:
        raise ValueError(
            f"n должно быть положительным целым числом "
            f"(получено: {n!r}; причина: {err.args[0]})"
        ) from err

    if not is_positive_int:
        raise ValueError(f"n должно быть положительным целым числом (получено: {n!r})")


def random_series(
    n: int,
    low: float = -100.0,
    high: float = 100.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Ряд из n равномерно распределённых случайных чисел на [low, high]."""
    _validate_n(n)
    if low >= high:
        raise ValueError(f"low должно быть меньше high (получено: {low} >= {high})")
    rng = random.Random(seed)
    return [rng.uniform(low, high) for _ in range(n)]


def sine_series(
    n: int,
    amplitude: float = 1.0,
    frequency: float = 1.0,
    noise: float = 0.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Синусоидальный ряд с аддитивным шумом."""
    _validate_n(n)
    rng = random.Random(seed)
    return [
        amplitude * math.sin(2 * math.pi * frequency * i / n)
        + (rng.uniform(-noise, noise) if noise else 0.0)
        for i in range(n)
    ] 


def trend_series(
    n: int,
    start: float = 0.0,
    step: float = 1.0,
    noise: float = 0.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Линейный тренд с добавлением шума."""
    _validate_n(n)
    rng = random.Random(seed)
    return [
        start + step * i + (rng.uniform(-noise, noise) if noise else 0.0)
        for i in range(n)
    ]


# Вариант 8
def variant8_series(
    n: int = 1500,
    noise_scale: float = 1.0,
    outlier_factor: float = 10.0,
    seed: Optional[int] = None,
) -> List[float]:
    """Вариант 8: ряд из n (по умолчанию 1500) чисел — шум + два выброса
    (значения примерно в 10 раз больше типичных)."""
    _validate_n(n)
    if noise_scale <= 0:
        raise ValueError(f"noise_scale должно быть > 0 (получено: {noise_scale})")
    if outlier_factor <= 1.0:
        raise ValueError(f"outlier_factor должно быть > 1.0 (получено: {outlier_factor})")

    rng = random.Random(seed)
    series = [float(rng.gauss(0.0, noise_scale)) for _ in range(n)]

    # Типичное значение ряда (среднее абсолютное отклонение от 0 / масштаб шума)
    typical = sum(abs(x) for x in series) / len(series)
    if typical == 0.0:
        typical = float(noise_scale)

    # Добавляем два выброса в 10 раз больше типичных значений
    idx1 = n // 4
    idx2 = (3 * n) // 4
    if idx2 == idx1 and n >= 2:
        idx2 = min(n - 1, idx1 + 1)

    series[idx1] = float(outlier_factor * typical)
    if n >= 2:
        series[idx2] = float(-outlier_factor * typical)

    return series