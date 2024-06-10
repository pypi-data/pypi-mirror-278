# В одномерном массиве целых чисел найти количество пар
# элементов разного знака. (пара — это два рядом стоящих элемента)


def count_opposite_sign_pairs(arr):
    count = 0
    for i in range(len(arr) - 1):
        if (arr[i] >= 0 and arr[i+1] < 0) or (arr[i] < 0 and arr[i+1] >= 0):
            count += 1
    return count


arr = [1, 2, 3, -4, 5, -6]
print(count_opposite_sign_pairs(arr))
