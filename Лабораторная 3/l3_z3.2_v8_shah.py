print("Лабораторная работа 3, Задание 3.2, Вариант 8\n")

# Ввод количества элементов N
ok_n = False
n = 0
while not ok_n:
    try:
        n = int(input("Введите количество элементов массива N > 0: "))
        if n > 0:
            ok_n = True
        else:
            print("Ошибка: количество элементов должно быть > 0. Повторите ввод")
    except ValueError:
        print("Ошибка: введите целое число, а не текст. Повторите ввод")

# Ввод элементов массива
arr = []
print("Введите элементы массива: ")
i = 0
while i < n:
    ok_elem = False
    val = 0.0
    while not ok_elem:
        try:
            val = float(input(f"Элемент {i + 1}: "))
            ok_elem = True
        except ValueError:
            print("Ошибка: введите число, а не текст. Повторите ввод")
    arr.append(val)
    i += 1

# Вычисление суммы и среднего арифметического
sum_elements = 0.0
for x in arr:
    sum_elements += x

arithmetic_mean = sum_elements / n if n > 0 else 0.0

# Замена всех нулевых элементов на среднее арифметическое
modified_arr = []
for x in arr:
    if x == 0:
        modified_arr.append(arithmetic_mean)
    else:
        modified_arr.append(x)

print("\nРезультаты расчетов:")
print(f"Исходный массив: {arr}")
print(f"Среднее арифметическое: {arithmetic_mean:.2f}")
print(f"Массив после замены нулей: {modified_arr}")