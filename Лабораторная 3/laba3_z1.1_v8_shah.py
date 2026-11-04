print("Лабораторная работа 3, Задание 1.1, Вариант 8\n")

n = int(input("Введите количество чисел: "))

numbers = list(map(float, input("Введите последовательность через пробел: ").split()))

sum_odd = 0
active = 1

for i in range(n):
    x = numbers[i]
    is_odd = int(x.is_integer() and int(x) % 2 != 0)
    active *= is_odd
    sum_odd += x * active

print(f"Сумма всех идущих подряд в начале последовательности нечетных чисел: {sum_odd}")