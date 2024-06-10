# 22. Создать класс Деньги для работы с денежными суммами. Число должно
# быть представлено списком, состоящим из рублей и копеек. Реализовать сложение,
# вычитание, деление сумм, деление денежных сумм.

class Money:
    def __init__(self, rubles, kopek):
        self.rubles = rubles
        self.kopek = kopek
        self._normalize()

    def _normalize(self):
        total_kopek = self.rubles * 100 + self.kopek
        self.rubles = total_kopek // 100
        self.kopek = total_kopek % 100

    def __add__(self, other):
        total_kopek = (self.rubles * 100 + self.kopek) + (other.rubles * 100 + other.kopek)
        return Money(total_kopek // 100, total_kopek % 100)

    def __sub__(self, other):
        total_kopek = (self.rubles * 100 + self.kopek) - (other.rubles * 100 + other.kopek)
        return Money(total_kopek // 100, total_kopek % 100)

    def __truediv__(self, other):
        if isinstance(other, Money):
            total_kopek = (self.rubles * 100 + self.kopek) / (other.rubles * 100 + other.kopek) * 100
            if (other.rubles * 100 + other.kopek) == 0:
                raise ZeroDivisionError("Деление на ноль")
            return Money(int(total_kopek // 100), int(total_kopek % 100))
        elif isinstance(other, (int, float)):
            total_kopek = (self.rubles * 100 + self.kopek) / other
            return Money(int(total_kopek // 100), int(total_kopek % 100))
        raise TypeError("Деление возможно только на числовое значение")

    def __str__(self):
        return f"{self.rubles} руб. {self.kopek:02d} коп."


# Примеры использования
a = Money(5, 100)
b = Money(3, 0)

print(f"Сложение: {a + b}")
print(f"Вычитание: {a - b}")
print(f"Деление сумм: {(a + b) / 2}")
print(f"Деление денежных сумм: {a / b}")
