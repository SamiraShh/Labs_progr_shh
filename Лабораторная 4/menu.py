from __future__ import annotations

def show_menu() -> None:
    """Вывести пункты меню сечений."""
    print("\nМеню: 1- прямоугольное, 2 - круглое, 3 - двутавр, 0 - выход")

def select_mode() -> int | None:
    """Циклически запрашивать выбор сечения через match-case."""
    while True:
        show_menu()
        choice = input("Введите номер меню (от 1 до 3): ").strip()
        match choice:
            case "1" | "2" | "3":
                return int(choice)
            case "0":
                return None
            case _:
                print("Ошибка: неверный пункт меню. Повторите ввод.")

def mode_name(menu: int) -> str:
    """Получить название сечения через math-case."""
    match menu:
        case 1:
            return "Прямоугольное"
        case 2:
            return "Круглое"
        case 3:
            return "Двутавр"
        case _:
            return "Неизвестно"