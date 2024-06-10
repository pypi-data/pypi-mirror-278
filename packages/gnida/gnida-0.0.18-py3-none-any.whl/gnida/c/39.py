# Дан одномерный массив целых чисел размерности n, заданных
# случайным образом из интервала от -20 до 20. Если сумма отрицательных
# элементов по модулю превышает сумму положительных, то отсортировать массив
# по возрастанию, иначе – по убыванию. Реализовать сортировку алгоритмом
# сортировки выбором.

import random


def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def check_sum(arr):
    negative_sum = 0
    positive_sum = 0
    for num in arr:
        if num < 0:
            negative_sum += num
        else:
            positive_sum += num
    if abs(negative_sum) > positive_sum:
        return True
    else:
        return False


def main():
    n = int(input("Введите размер массива: "))
    arr = [random.randint(-20, 20) for _ in range(n)]
    print("Исходный массив:", arr)
    if check_sum(arr):
        arr = selection_sort(arr)
        print("Отсортированный массив по возрастанию:", arr)
    else:
        arr = selection_sort(arr)[::-1]
        print("Отсортированный массив по убыванию:", arr)


if __name__ == '__main__':
    main()
