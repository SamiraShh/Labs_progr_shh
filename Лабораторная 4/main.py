"""
Главный сценарий.
Связывает модули, реализует главный цикл программы (Вариант 8).
"""
from __future__ import annotations
from menu import select_mode, mode_name
from validation import input_size, input_moment, input_sigma
from operations import calculate_1, calculate_2, stress_coefficient, strength_class
def main() -> None:
    """Главный сценарий."""
    print("=== Расчёт прочности балки на изгиб (Вариант 8) ===")
    while True:
        menu = select_mode()
        if menu is None:
            print("Работа завершена.")
            break
        # Запрос размеров в зависимости от выбранного сечения (1 - прямоугольное, 2 - круглое, 3 - двутавр)
        if menu == 1:
            b = input_size()  # ширина
            h = input_size()  # высота
            W = calculate_1(menu, b, h)
        elif menu == 2:
            d = input_size()  # диаметр
            W = calculate_1(menu, d)
        else:
            h = input_size()  # высота двутавра
            W = calculate_1(menu, h)
        # Запрос нагрузок и характеристик материала
        M = input_moment()
        sigma_dop = input_sigma()
        # Расчёты
        sigma_fact = calculate_2(M, W)
        k = stress_coefficient(sigma_fact, sigma_dop)
        cls = strength_class(k)
        proverka = sigma_fact <= sigma_dop
        # Вывод результатов
        print("\n Результаты ")
        print(f"Сечение: {mode_name(menu)}")
        print(f"Момент сопротивления W: {W:.2f} мм^3")
        print(f"Фактическое напряжение σ: {sigma_fact:.2f} МПа")
        print(f"Допускаемое напряжение [σ]: {sigma_dop:.2f} МПа")
        print(f"Коэффициент использования k: {k:.2f}")
        print(f"Проверка прочности (σ <= [σ]): {'Выполнена' if proverka else 'Не выполнена'}")
        print(f"Класс прочности: {cls}")
        print("\n")
if __name__ == "__main__":
    main()