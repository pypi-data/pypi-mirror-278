# Дан список целых чисел. При помощи механизма map/filter/reduce
# рассчитать остаток от деления на 7 для каждого из чисел списка и получить
# произведение тех остатков, величина которых больше 4
from functools import reduce

numbers = [118, 48, 7, 3, 21]

remainders = list(map(lambda x: x % 7, numbers))

filtered_remainders = list(filter(lambda x: x > 4, remainders))

result = reduce(lambda x, y: x * y, filtered_remainders)

print(f"Остатки от деления на 7: {remainders}")
print(f"Остатки, больше 4: {filtered_remainders}")
print(f"Произведение остатков: {result}")
