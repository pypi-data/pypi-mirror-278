# Задание: построить базовый класс с указанными в таблице полями и
# методами:
# - конструктор; - функция, которая определяет «качество» объекта – Q по
# заданной формуле; - метод вывода информации об объекте.
# Построить дочерний класс (класс-потомок), который содержит:
# - дополнительное поле P;
# - функция, которая определяет «качество» объекта дочернего класса – Qp и
# перегружает функцию качества родительского класса (Q), выполняя вычисление по
# новой формуле.
# Создать проект для демонстрации работы: ввод и вывод информации об
# объектах классов
class Computer:
    def __init__(self, processor_name, processor_speed, memory):
        self.processor_name = processor_name
        self.processor_speed = processor_speed
        self.memory = memory

    def calculate_qualities(self):
        return (0.1 * self.processor_speed) + self.memory

    def display_info(self):
        print("Процессор:", self.processor_name)
        print("Частота процессора (MHz):", self.processor_speed)
        print("Память (MB):", self.memory)
        print("Q:", self.calculate_qualities())


class UpgradedComputer(Computer):
    def __init__(self, processor_name, processor_speed, memory, ssd_capacity):
        super().__init__(processor_name, processor_speed, memory)
        self.ssd_capacity = ssd_capacity

    def calculate_quality(self):
        base_quality = super().calculate_qualities()
        return base_quality + 0.5 * self.ssd_capacity

    def display_info(self):
        super().display_info()
        print("SSD (GB):", self.ssd_capacity)
        print("Q (Upgraded):", self.calculate_quality())


base_computer = Computer("Intel i5", 2500, 8192)
print("Base Computer Info:")
base_computer.display_info()

upgraded_computer = UpgradedComputer("Intel i7", 3500, 16384, 512)
print("\nUpgraded Computer Info:")
upgraded_computer.display_info()
