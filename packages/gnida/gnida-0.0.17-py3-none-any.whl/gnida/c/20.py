# С помощью функции reduce() вычислить двойной факториал заданного натурального числа n (для четного или нечетного n)

from functools import reduce


def double_factorial(n):
    if n % 2 == 0:
        sequence = range(n, 0, -2)
    else:
        sequence = range(n, 0, -2)
    return reduce(lambda x, y: x * y, sequence)


n = int(input('Введите число для расчета двойного факториала: '))
print(f"Двойной факториал числа {n} это {double_factorial(n)}")
