print("Лабораторная работа 3, Задание 3.1, Вариант 8\n")

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

# Нахождение суммы и произведения элементов списка
sum_elements = 0.0
prod_elements = 1.0

for x in arr:
    sum_elements += x
    prod_elements *= x

print("\nРезультаты расчетов:")
print(f"Массив: {arr}")
print(f"Сумма элементов списка: {sum_elements}")
print(f"Произведение элементов списка: {prod_elements}")