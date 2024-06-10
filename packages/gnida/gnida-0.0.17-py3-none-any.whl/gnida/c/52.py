# 52. Создать иерархию классов для фруктов, продающихся в магазине.
# Иерархия должна содержать не менее 3 классов. Объекты должны содержать не
# менее 2-х атрибутов и 2-х методов. Реализовать механизм автоматического
# подсчета количества всех созданных фруктов и автоматического присвоения
# каждому фрукту уникального идентификатора. Необходимо заполнить список
# представителями всех классов (всего не менее 5 объектов) и продемонстрировать
# работу созданного механизма.


class Fruit:
    _count = 0
    _id_counter = 1

    def __init__(self, color, weight):
        self.color = color
        self.weight = weight
        self.id = Fruit._id_counter
        Fruit._id_counter += 1
        Fruit._count += 1

    def display(self):
        return f"ID: {self.id}, Цвет: {self.color}, Вес: {self.weight}g"

    @classmethod
    def get_total_fruits(cls):
        return cls._count


class Apple(Fruit):
    def __init__(self, color, weight, variety):
        super().__init__(color, weight)
        self.variety = variety

    def display(self):
        return f"Яблоко - ID: {self.id}, Сорт: {self.variety}, Цвет: {self.color}, Вес: {self.weight}g"


class Banana(Fruit):
    def __init__(self, country, weight):
        super().__init__(country, weight)
        self.country = country

    def display(self):
        return f"Банан - ID: {self.id}, Страна поставки: {self.country}, Вес: {self.weight}g"


class Orange(Fruit):
    def __init__(self, color, weight, pack):
        super().__init__(color, weight)
        self.pack = pack

    def display(self):
        return f"Апельсин - ID: {self.id}, Упаковка: {self.pack}, Цвет: {self.color}, Вес: {self.weight}g"


apple = Apple("Красный", 150, "Гала")
apple2 = Apple("Зеленый", 130, "Смит")
banana = Banana("Эквадор", 120)
orange = Orange("Красный", 180, 'Сетка')
orange2 = Orange("Оранжевый", 200, 'Сетка')

fruits = [apple, apple2, banana, orange, orange2]

for fruit in fruits:
    print(fruit.display())

print("Всего фруктов:", Fruit.get_total_fruits())
