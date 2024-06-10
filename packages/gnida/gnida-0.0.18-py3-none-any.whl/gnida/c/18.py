#  Написать программу с интерактивным консольным меню (т.е. вывод
# списка действий по цифрам) по вычислению площади прямоугольника
# (родительский класс), и периметра прямоугольника (дочерний класс) по
# задаваемой с клавиатуры длине сторон прямоугольника.
# Содержание меню: 1. Вычислить площадь прямоугольника. 2. Вычислить периметр
# прямоугольника

class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


def main():
    while True:
        print("1. Вычислить площадь прямоугольника")
        print("2. Вычислить периметр прямоугольника")
        choice = int(input("Выберите действие: "))

        if choice == 1:
            length = float(input("Введите длину прямоугольника: "))
            width = float(input("Введите ширину прямоугольника: "))
            rect = Rectangle(length, width)
            print(f"Площадь прямоугольника: {rect.area()}")
        elif choice == 2:
            length = float(input("Введите длину прямоугольника: "))
            width = float(input("Введите ширину прямоугольника: "))
            rect = Rectangle(length, width)
            print(f"Периметр прямоугольника: {rect.perimeter()}")
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
