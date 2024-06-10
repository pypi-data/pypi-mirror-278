# Создайте класс Speed (Скорость), имеющий атрибуты: value (значение), unit (единица измерения).
# При изменении единицы измерения значение должно соответственно меняться.
# Например, при переходе от км/ч к м/с и наоборот.
# Например, 20 км/ч = 5.56 м/с. Допустимые значения свойства unit: ‘м/с’, ‘км/ч’.
# Организуйте эту проверку. Продемонстрируйте работу с классом.
class Speed:
    def __init__(self, value, unit):
        self._unit = None
        self._value = None
        self.unit = unit
        self.value = value

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, new_unit):
        if new_unit not in ['м/с', 'км/ч']:
            raise ValueError("Единица измерения должна быть 'м/с' или 'км/ч'")

        if self._unit is not None and self._unit != new_unit:
            if new_unit == 'км/ч':
                self._value = self._value * 3.6
            elif new_unit == 'м/с':
                self._value = self._value / 3.6

        self._unit = new_unit

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def convert(self):
        if self.unit == 'км/ч':
            converted_value = self.value / 3.6
            converted_unit = 'м/с'
        else:
            converted_value = self.value * 3.6
            converted_unit = 'км/ч'
        return f"{self.value:.2f} {self.unit} = {converted_value:.2f} {converted_unit}"

    def __str__(self):
        return self.convert()



speed = Speed(20, 'км/ч')
print(speed)

speed.unit = 'м/с'
print(speed)

speed.value = 10
print(speed)

speed.unit = 'км/ч'
print(speed)

try:
    speed.unit = 'миль/ч'
except ValueError as e:
    print(e)
