# Реализовать декоратор с именем not_sum, который генерирует исключительную
# ситуацию, если декорируемая функция вернула отрицательное значение суммы трех чисел

def not_sum(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, (tuple, list)) and len(result) == 3:
            sum_value = sum(result)
            if sum_value < 0:
                raise NegativeSumError(sum_value)
        return f'Все замечательно! Сумма: {sum_value}'

    return wrapper


class NegativeSumError(Exception):
    def __init__(self, sum_value):
        self.sum_value = sum_value
        self.message = f"Ошибка. Сумма не должна быть отрицательной. Сумма: {sum_value}"
        super().__init__(self.message)


@not_sum
def test_function(a, b, c):
    return a, b, c


a = int(input('Введите первое число: '))
b = int(input('Введите второе число: '))
c = int(input('Введите третье число: '))
try:
    print(test_function(a, b, c))
except NegativeSumError as e:
    print(e)
