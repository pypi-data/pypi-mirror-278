# Дан список А3, состоящий из четного количества элементов.
# Используя функцию(функции) высшего порядка разбейте его на списки В, С так,
# чтобы в одном были положительные элементы, а в другом отрицательные

def split_list_by_sign(numbers):
    positive_numbers = list(filter(lambda x: x > 0, numbers))
    negative_numbers = list(filter(lambda x: x < 0, numbers))

    return positive_numbers, negative_numbers


A3 = [3, -1, 2, -4, 5, -6, 8, -9]
B, C = split_list_by_sign(A3)

print("Положительные числа (B):", B)
print("Отрицательные числа (C):", C)
