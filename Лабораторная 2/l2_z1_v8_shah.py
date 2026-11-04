import math

print("Лабораторная работа 2 (Вариант  8)\n")

# Функция ввода чисел с проверкой ошибок
def vvod_chis(mes, min_znach, max_znach):
    ok = True
    result = 0
    while ok:
        try:
            result = float(input(mes))
            if min_znach <= result <= max_znach:
                ok = False
            else:
                print(f"Ошибка: введите число от {min_znach} до {max_znach}")
        except ValueError:
            print("Ошибка: введите число, а не текст")
    return result

# Меню выбора
f_menu = True
menu = 0
while f_menu:
    try:
        menu = int(input("Выберите тип сечения (1 - прямоугольное, 2 - круглое, 3 - двутавр): "))
        if menu in (1, 2, 3):
            f_menu = False
        else:
            print("Ошибка: введите цифру от 1 до 3")
    except ValueError:
        print("Ошибка: введите число, а не текст")

# Запрос размеров
if menu == 1:
    b = vvod_chis("Введите ширину сечения от 10 до 1000(мм): ", 10, 1000)
    h = vvod_chis("Введите высоту сечения от 10 до 1000(мм): ", 10, 1000)
elif menu == 2:
    d = vvod_chis("Введите диаметр сечения от 10 до 1000(мм): ", 10, 1000)
else:
    h = vvod_chis("Введите высоту двутавра от 10 до 1000(мм): ", 10, 1000)

M = vvod_chis("Введите изгибающий момент от 0.1 до 500(кНм): ", 0.1, 500)
sigma_dop = vvod_chis("Введите допускаемое напряжение от 50 до 400(МПа): ", 50, 400)

# Расчет момента сопротивления
match menu:
    case 1:
        W = (b * h ** 2)/6
        name = "Прямоугольное"
    case 2:
        W = (math.pi * d ** 3)/32
        name = "Круглое"
    case 3:
        W = (h ** 3)/12
        name = "Двутавр" 

sigma_fact = (M * 1000000)/W
k = sigma_fact/sigma_dop

# Проверка прочности и границ
proverka = sigma_fact <= sigma_dop

if k < 0.5:
    class_name = "Большой запас"
elif 0.5 <= k <= 1.0:
    class_name = "Допустимо"
else:
    class_name = "Перегрузка"

# Вывод результатов
print("\nРезультаты расчета\n")
print(f"Тип сечения: {name}")
print(f"Момент сопротивления: {W:.2f} мм^3")
print(f"Фактическое напряжение: {sigma_fact:.2f} МПа")
print(f"Допускаемое напряжение: {sigma_dop:.2f} МПа")
print(f"Коэффициент использования: {k:.2f}")
print(f"Проверка прочности: {"Выполнена" if proverka else "Не выполнена"}")
print(f"Класс прочности: {class_name}")
