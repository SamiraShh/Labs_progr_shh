"""Модуль вычисления скользящих средних (SMA, CMA, EMA)."""

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
        raise ValueError(
            f"window ({window}) не может превышать длину ряда ({n})"
        )


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Простая скользящая средняя (SMA) через эффективную бегущую сумму O(n)."""
    if not data:
        return []
    check_window(window, len(data))

    running = sum(data[:window])
    result = [running / window]

    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)

    return result


def simple_moving_average_deque(data: Sequence[float], window: int) -> List[float]:
    """SMA с использованием deque (двусторонней очереди)."""
    check_window(window, len(data))
    result = []
    d = deque()
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


def benchmark_moving_average(
    data: Sequence[float], window: int, repeats: int = 1000
) -> dict[str, float]:
    """Замеряет среднее время выполнения SMA для list и deque в секундах."""
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