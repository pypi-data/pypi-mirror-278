# 40. Создать декоратор dec(a, b) с параметрами a и b. Декоратор увеличивает
# результат декорируемой функции, которая вычисляет сумму произвольного
# количества чисел, на «a» элементов при условии положительного значения суммы.
# Если исходная функция возвращает отрицательное значение суммы, то декоратор
# уменьшает результат декорируемой функции на значение «b».

a = 0
b = 0


def dec(a, b):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result > 0:
                return result + a
            else:
                return result - b

        return wrapper

    return decorator


a = int(input('Введите значение a: '))
b = int(input('Введите значение b: '))


@dec(a, b)
def sum_numbers(numbers):
    return sum(numbers)


sum_list = list(map(int, input("Введите числа через пробел: ").split()))

print(sum_numbers(sum_list))
