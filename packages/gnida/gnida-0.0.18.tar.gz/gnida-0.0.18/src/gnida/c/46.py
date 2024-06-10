# 46. Дан список целых чисел. При помощи механизма map/filter/reduce
# рассчитать остаток от деления на 17 для каждого из чисел списка и получить
# произведение тех остатков, величина которых меньше 7.


from functools import reduce

numbers = [23, 45, 67, 91, 123, 145, 172, 189, 206, 220]

remainders = list(map(lambda x: x % 17, numbers))

filtered_remainders = list(filter(lambda x: x < 7, remainders))

product_of_remainders = reduce(lambda x, y: x * y, filtered_remainders, 1)

print(f"Остатки от деления на 17: {remainders}")
print(f"Остатки, меньше 7: {filtered_remainders}")
print(f"Произведение остатков, меньше 7: {product_of_remainders}")