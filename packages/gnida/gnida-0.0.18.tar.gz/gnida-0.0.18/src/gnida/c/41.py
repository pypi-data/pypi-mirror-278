# Дан одномерный массив целых чисел размерности n, заданных случайным
# образом из интервала от -20 до 20. Если в массиве есть отрицательные
# элементы, то отсортировать массив по возрастанию, иначе - по убыванию.
# Реализовать сортировку алгоритмом сортировки вставками

import random


def insertion_sort(arr, ascending=True):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((key < arr[j] and ascending) or (key > arr[j] and not ascending)):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

n = 10
array = [random.randint(-20, 20) for _ in range(n)]

print("Исходный массив:", array)

has_negative = any(x < 0 for x in array)

if has_negative:
    print("Массив содержит отрицательные элементы. Сортируем по возрастанию.")
    insertion_sort(array, ascending=True)
else:
    print("Массив не содержит отрицательных элементов. Сортируем по убыванию.")
    insertion_sort(array, ascending=False)

print("Отсортированный массив:", array)
