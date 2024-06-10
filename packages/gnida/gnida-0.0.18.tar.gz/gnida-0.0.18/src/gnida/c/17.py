# Задано положительное и отрицательное число в двоичной системе.
# Составить программу вычисления суммы этих чисел, используя функцию
# сложения чисел в двоичной системе счисления. Использовать рекурсию.

from datetime import datetime


class Automobile:
    def __init__(self, brand, power, seats):
        self.brand = brand
        self.power = power
        self.seats = seats

    def qualities(self):
        return 0.1 * self.power * self.seats

    def display_info(self):
        print(f"Марка: {self.brand}")
        print(f"Мощность двигателя (кВт): {self.power}")
        print(f"Число мест: {self.seats}")
        print(f"Качество (Q): {self.qualities()}")


class Car(Automobile):
    def __init__(self, brand, power, seats, year_of_production):
        super().__init__(brand, power, seats)
        self.year_of_production = year_of_production

    def quality(self):
        T = datetime.now().year
        R = self.year_of_production
        return super().qualities() - 1.5 * (T - R)

    def display_info(self):
        super().display_info()
        print(f"Год выпуска: {self.year_of_production}")
        print(f"Качество (Qp): {self.quality()}")



brand = input("Введите марку автомобиля: ")
power = float(input("Введите мощность двигателя (кВт): "))
seats = int(input("Введите число мест: "))
year_of_production = int(input("Введите год выпуска: "))

car = Car(brand, power, seats, year_of_production)

print("Информация об автомобиле:")
car.display_info()
