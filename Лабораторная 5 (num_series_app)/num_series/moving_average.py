"""Модуль вычисления скользящих средних (SMA, CMA, EMA) и медианного сглаживания (скользящая медиана окна k)."""

from __future__ import annotations
import time
from collections import deque
from typing import Sequence, List


def check_window(window: int, n: int) -> None:
    """Проверка корректности размера окна."""
    if isinstance(window, bool) or not isinstance(window, int):
        raise ValueError(f"window должно быть целым числом (получено: {window!r})")
    if window < 1:
        raise ValueError(f"window должно быть >= 1 (получено: {window})")
    if n <= 0:
        raise ValueError("Ряд пуст: вычисление скользящего окна невозможно")
    if window > n:
        raise ValueError(f"window ({window}) не может превышать длину ряда ({n})")


def _check_alpha(alpha: float) -> None:
    """Проверка коэффициента сглаживания alpha для EMA."""
    if isinstance(alpha, bool) or not (0.0 < alpha <= 1.0):
        raise ValueError(f"alpha должен быть в (0, 1], получено: {alpha}")


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Простая скользящая средняя (SMA) через эффективную бегущую сумму O(n)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт SMA невозможен")
    check_window(window, len(data))

    running = sum(data[:window])
    result = [running / window]

    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


def simple_moving_average_deque(data: Sequence[float], window: int) -> List[float]:
    """SMA с использованием deque (двусторонней очереди)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт SMA невозможен")
    check_window(window, len(data))

    result: List[float] = []
    d: deque[float] = deque()
    running_sum = 0.0
    for x in data:
        d.append(x)
        running_sum += x
        if len(d) > window:
            running_sum -= d.popleft()
        if len(d) == window:
            result.append(running_sum / window)
    return result


def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированная скользящая средняя (требует нечетное окно)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт центрированного MA невозможен")
    check_window(window, len(data))
    if window % 2 == 0:
        raise ValueError("Для центрированного МА размер окна должен быть нечетным")

    running = sum(data[:window])
    result: List[float] = [running / window]
    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """Экспоненциальная скользящая средняя (EMA)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт EMA невозможен")
    _check_alpha(alpha)

    ema = [float(data[0])]
    for i in range(1, len(data)):
        val = alpha * data[i] + (1 - alpha) * ema[-1]
        ema.append(val)
    return ema


# Вариант 8
def median_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Скользящая медиана по окну размера window (работает при чётном и нечётном window)."""
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей медианы невозможен")
    check_window(window, len(data))

    result: List[float] = []
    half = window // 2
    for i in range(len(data) - window + 1):
        s = sorted(data[i : i + window])
        if window % 2 == 1:
            result.append(float(s[half]))
        else:
            result.append((float(s[half - 1]) + float(s[half])) / 2.0)
    return result


def benchmark_moving_average(
    data: Sequence[float], window: int, repeats: int = 1000
) -> dict[str, float]:
    """Замеряет среднее время выполнения SMA для list и deque в секундах."""
    if not data: 
        raise ValueError("Ряд пуст: бенчмарк невозможен")
    check_window(window, len(data))
    if repeats < 1:
        raise ValueError(f"repeats должно быть >= 1 (получено: {repeats})")

    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average(data, window)
    t_list = (time.perf_counter() - t0) / repeats

    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average_deque(data, window)
    t_deque = (time.perf_counter() - t0) / repeats

    return {"list": t_list, "deque": t_deque}