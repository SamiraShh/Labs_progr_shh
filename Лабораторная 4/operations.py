"""Расчеты: момент сопротивления, напряжения и класс прочности."""
from typing import Annotated
from connstans import PI

def calculate_1(
    menu: Annotated[int, "Тип сечения: 1 - прямоугольное, 2 - круглое, 3 - двутавр"],
    size1: Annotated[float, "Первый размер(ширина/диаметр/высота), мм"],
    size2: Annotated[float | None, "Второй размер (высота для прямоугольника), мм"] = None
) -> float:
    """
    Рассчитать момент сопротивления W в зависимости от выбранного сечения.
    Args:
        menu: тип сечения (1, 2 или 3).
        size1: размер сечения (b, d или h).
        size2: второй размер (h для прямоугольника).
    Returns:
        Момент сопротивления W, мм^3.
    """
    if menu == 1:
        # Прямоугольное: W = b * h^2 / 6
        return (size1 * (size2 ** 2)) / 6
    elif menu == 2:
        # Круглое: W = pi * d^3 / 32
        return (PI * (size1 ** 3)) / 32
    elif menu == 3:
        # Двутавр: W = h^3 / 12
        return (size1 ** 3) / 12
    return 0.0

def calculate_2(
    m: Annotated[float, "Изгибающий момент, кН·м"],
    w: Annotated[float, "Момент сопротивления, мм^3"]
) -> float:
    """
    Рассчитать фактическое напряжение sigma = M * 10^6 / W, МПа.
    Args:
        m: изгибающий момент, кН·м.
        w: момент сопротивления, мм^3.
    Returns:
        Фактическое напряжение, МПа.
    """
    return (m * 1000000.0) / w

def stress_coefficient(
    sigma_fact: Annotated[float, "Фактическое напряжение, МПа"],
    sigma_dop: Annotated[float, "Допускаемое напряжение, МПа"]
) -> float:
    """
    Рассчитать коэффициент использования k = sigma_fact / sigma_dop.
    Args:
        sigma_fact: фактическое напряжение, МПа.
        sigma_dop: допускаемое напряжение, МПа.
    Returns:
        Коэффициент использования k.
    """
    return sigma_fact / sigma_dop

def strength_class(
    k: Annotated[float, "Коэффициент использования"]
) -> str:
    """
    Классифицировать запас прочности через if-elif-else.
    k < 0.5 — большой запас;
    0.5 <= k <= 1.0 — допустимо;
    k > 1.0 — перегрузка.
    Args:
        k: коэффициент использования.
    Returns:
        Строка с названием класса прочности.
    """
    if k < 0.5:
        return "большой запас"
    elif 0.5 <= k <= 1.0:
        return "допустимо"
    else:
        return "перегрузка"
