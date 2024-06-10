# Создать иерархию классов для фруктов, продающихся в магазине.
# Иерархия должна содержать не менее 3 классов. Объекты должны содержать не
# менее 3-х атрибутов. Часть атрибутов должна быть защищена от изменения.
# Необходимо заполнить список представителями всех классов (всего 5 объектов) и
# продемонстрировать созданную защиту.

class Fruit:
    def __init__(self, name, price_per_kg):
        self.__name = name
        self.price_per_kg = price_per_kg

    def get_name(self):
        return self.__name

class Apple(Fruit):
    def __init__(self, name, price_per_kg, variety):
        super().__init__(name, price_per_kg)
        self._variety = variety

class Banana(Fruit):
    def __init__(self, name, price_per_kg, origin):
        super().__init__(name, price_per_kg)
        self._origin = origin

class Orange(Fruit):
    def __init__(self, name, price_per_kg, color):
        super().__init__(name, price_per_kg)
        self.color = color


apple = Apple("Apple", 3.5, "Granny Smith")
banana = Banana("Banana", 2.0, "Ecuador")
orange = Orange("Orange", 4.0, "Orange")


apple.__name = "Pear"
print(apple.get_name())

banana.price_per_kg = 2.5
print(banana.price_per_kg)

orange.color = "Green"
print(orange.color)