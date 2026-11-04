print("Лабораторная работа 3, Задание 1.1, Вариант 8\n")

# Ввод N элементов с валидацией
ok_n = False
n = 0
while not ok_n:
    try:
        n = int(input("Введите количество чисел (n > 0): "))
        if n > 0:
            ok_n = True
        else:
            print("Ошибка: количество чисел должно быть > 0")
    except ValueError:
        print("Ошибка: введите целое число, а не текст")

# Ввод самой последовательности из n чисел (тоже с валидацией)
numbers = []
print("Введите элементы последовательности: ")
for i in range(n):
    ok_num = False
    x = 0.0
    while not ok_num:
        try:
            x = float(input(f"Элемент {i + 1}: "))
            # Условие для самого первого числа
            if i == 0:
                if x.is_integer() and int(x) % 2 != 0:
                    ok_num = True
                else:
                    print("Ошибка: первое число должно быть нечетным целым. Повторите ввод")
            else:
                # Остальные - просто вещественные 
                ok_num = True
        except ValueError:
            print("Ошибка: введите вещественное число, а не текст")
    numbers.append(x)

# Поиск суммы идущих подряд в начале нечетных чисел
sum_odd = 0.0
active = 1

for j in range(n):
    x = numbers[j]
    # Является ли число целым и нечетным
    is_odd = int(x.is_integer() and int(x) % 2 != 0)
    active *= is_odd
    sum_odd += x * active

print(f"\nСумма всех идущих подряд в начале последовательности нечетных чисел: {sum_odd}")