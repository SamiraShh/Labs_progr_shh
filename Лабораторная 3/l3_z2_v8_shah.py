print("Лабораторная работа 3, Задание 2, Вариант 8\n")

# Ввод строки
ok_str = False
s = ""
while not ok_str:
    s = input("Введите строку, заканчивающуюся точкой: ").strip()
    if len(s) == 0:
        print("Ошибка: строка не может быть пустой. Повторите ввод")
    elif not s.endswith('.'):
        print("Ошибка: строка должна заканчиваться точкой (.). Повторите ввод")
    else:
        ok_str = True

# Убираем точку в конце для подсчета слов
s_without_dot = s[:-1].strip()

# Подсчет количества слов
word_count = 0
if len(s_without_dot) > 0:
    words = s_without_dot.split()
    word_count = len(words)

print("\nРезультаты расчета:")
print(f"Исходная строка: {s}")
print(f"Количество слов в строке: {word_count}")