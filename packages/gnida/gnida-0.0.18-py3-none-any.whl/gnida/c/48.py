# Дан список целых чисел. При помощи механизма map/filter/reduce
# рассчитать разность со значением 10 для каждого из чисел списка и получить
# сумму тех значений, величина которых меньше 0.

from functools import reduce

numbers = [118, 48, 7, 3, 21]

remainders = list(map(lambda x: x - 10, numbers))

filtered_remainders = list(filter(lambda x: x < 0, remainders))

result = reduce(lambda x, y: x + y, filtered_remainders)

print(f"Результаты разности: {remainders}")
print(f"Результаты, меньше нуля: {filtered_remainders}")
print(f"Сумма остатков: {result}")