# Создать базовый класс по следующей предметной области.
# Известны оклад (зарплата) и ставка процента подоходного налога.
# Определить размер подоходного налога и сумму, получаемую на руки.
# Исходными данными являются величина оклада (переменная oklad, выражаемая числом)
# и ставка подоходного налога (переменная procent, выражаемая числом).
# Размер налога (переменная nalog) определяется как oklad∗procent/100,
# а сумма, получаемая на руки (переменная summa) — как oklad-nalog.

class Salary:
    def __init__(self, oklad, procent):
        self.oklad = oklad
        self.procent = procent
        self.nalog = self.calculate_nalog()
        self.summa = self.calculate_summa()

    def calculate_nalog(self):
        return self.oklad * self.procent / 100

    def calculate_summa(self):
        return self.oklad - self.nalog

    def display_info(self):
        print(f"Оклад: {self.oklad}")
        print(f"Ставка налога: {self.procent}%")
        print(f"Размер налога: {self.nalog}")
        print(f"Сумма на руки: {self.summa}")


salary = Salary(50000, 13)
salary.display_info()
