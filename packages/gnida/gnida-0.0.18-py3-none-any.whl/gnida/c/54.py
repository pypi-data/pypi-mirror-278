# В одномерном массиве (array) целых чисел найти количество пар, модуль
# разности элементов которых больше 10. (пара — это два рядом стоящих элемента)

def count_pairs(array):
    count = 0
    for i in range(len(array) - 1):
        if abs(array[i] - array[i + 1]) > 10:
            count += 1
    return count


array = [1, 2, 3, 25, 5, 6, 7, 8, 9, 10, 11, 12]

print(count_pairs(array))
