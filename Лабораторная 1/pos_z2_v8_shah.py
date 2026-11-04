import math

print("Лабораторная работа 1, Задание 2 (Вариант 8)\n")

# Ввод величин
d = float(input("Введите диаметр окружности: "))
alpha_rad = float(input("Введите радианную меру угла: "))

# Проверка существования окружности и угла
if d <= 0 or alpha_rad <= 0 or alpha_rad > 2 * math.pi:
    print("Ошибка!")
else:
    r = d/2
    l = r * alpha_rad
    s_seg = (0.5 * r ** 2) * (alpha_rad - math.sin(alpha_rad)) 

print(f"\nДлина дуги: {l:.2f}")
print(f"Площадь кругового сегмента: {s_seg:.2f}")
