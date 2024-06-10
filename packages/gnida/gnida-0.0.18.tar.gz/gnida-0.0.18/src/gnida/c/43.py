# 43. Дан одномерный массив целых чисел размерности n, заданных
# случайным образом из интервала от 0 до 100. Если количество четных элементов,
# стоящих на нечетных местах, превышает количество нечетных элементов, стоящих
# на четных местах, то отсортировать массив по возрастанию, иначе по убыванию.
# Реализовать алгоритм сортировки слиянием.


import random


def merge_sort(arr, reverse=False):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L, reverse)
        merge_sort(R, reverse)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if (L[i] < R[j] and not reverse) or (L[i] > R[j] and reverse):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


n = int(input('Введите число элементов в массиве: '))
array = [random.randint(0, 100) for _ in range(n)]
print('Массив до сортировки: ', array)

even_on_odd_indices = sum(1 for i in range(1, n, 2) if array[i] % 2 == 0)
print(even_on_odd_indices)
odd_on_even_indices = sum(1 for i in range(0, n, 2) if array[i] % 2 != 0)
print(odd_on_even_indices)

if even_on_odd_indices > odd_on_even_indices:
    merge_sort(array)
else:
    merge_sort(array, reverse=True)

print("Отсортированный массив: ", array)
