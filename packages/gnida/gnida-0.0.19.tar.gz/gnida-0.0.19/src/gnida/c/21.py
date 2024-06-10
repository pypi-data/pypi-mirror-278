#  Создайте класс Заказ(Order), у которого есть свойства код_товара(code),
# цена(price), количество(count) и методы __init__ и __str__. Создайте 2 классапотомка: Опт(Opt) и
# Розница(Retail). В этих классах создайте методы __init__,
# __str__ и сумма_заказа (summa), позволяющий узнать стоимость заказа. Для опта
# стоимость единицы товара составляет 95% от цены, а при покупке более 500 штук
# – 90% цены. В розницу стоимость единицы товара составляет 100% цены.
# Стоимость заказа равна произведению цены на количество. Создайте список,
# содержащий по 2 объекта каждого класса (Order, Opt, Retail). Для этого списка:
# • выведите информацию о каждом объекте с помощью метода __str__;
# • найдите общую стоимость заказов для объектов Opt и Retail.
class Order:
    def __init__(self, code, price, count):
        self.code = code
        self.price = price
        self.count = count

    def __str__(self):
        return f"Код товара: {self.code}, Цена: {self.price}, Количество: {self.count}"

class Opt(Order):
    def __init__(self, code, type, price, count):
        super().__init__(code, price, count)
        self.type = type

    def __str__(self):
        return f"Код товара: {self.code}, Тип: {self.type}, Цена: {self.price}, Количество: {self.count}"

    def summa(self):
        if self.count > 500:
            return 0.9 * self.price * self.count
        else:
            return 0.95 * self.price * self.count


class Retail(Order):
    def __init__(self, code, type, price, count):
        super().__init__(code, price, count)
        self.type = type

    def summa(self):
        return self.price * self.count

    def __str__(self):
        return f"Код товара: {self.code}, Тип: {self.type}, Цена: {self.price}, Количество: {self.count}"


orders = [
    Order("001", 100, 200),
    Order("002", 50, 600),
    Opt("003", 'Opt', 80, 300),
    Opt("004", 'Opt',120, 700),
    Retail("005", 'Retail',70, 400),
    Retail("006", 'Retail',90, 800)
]

total_opt_cost = sum(order.summa() for order in orders if isinstance(order, Opt))
total_retail_cost = sum(order.summa() for order in orders if isinstance(order, Retail))

for order in orders:
    print(order)

print(f"Общая стоимость заказов для объектов Opt: {total_opt_cost}")
print(f"Общая стоимость заказов для объектов Retail: {total_retail_cost}")


