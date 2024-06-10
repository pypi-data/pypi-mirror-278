# Написать программу с интерактивным консольным меню (т.е. вывод списка действий по цифрам) по вычислению площади
# круга (родительский класс), длины окружности (подкласс) и объема шара (подкласс) по задаваемому с клавиатуры
# радиусу. Содержание меню: 1. Вычислить площадь круга. 2. Вычислить длину окружности. 3. Вычислить объем шара.

import math


def calculate_area(radius):
    return math.pi * radius ** 2


def calculate_circumference(radius):
    return 2 * math.pi * radius


def calculate_volume(radius):
    return 4 / 3 * math.pi * radius ** 3


def main():
    while True:
        print("Меню:")
        print("1. Вычислить площадь круга")
        print("2. Вычислить длину окружности")
        print("3. Вычислить объем шара")
        print("4. Выйти")

        choice = input("Выберите действие (1-4): ")

        if choice == '4':
            print("Выход из программы.")
            break

        if choice != '4':
            radius = float(input("Введите радиус: "))

            if choice == '1':
                print(f"Площадь круга: {calculate_area(radius)}")
            elif choice == '2':
                print(f"Длина окружности: {calculate_circumference(radius)}")
            elif choice == '3':
                print(f"Объем шара: {calculate_volume(radius)}")
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
