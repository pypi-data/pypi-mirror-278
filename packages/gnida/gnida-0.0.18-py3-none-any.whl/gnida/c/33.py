# Вывести по убыванию количество всех предыдущих ремонтов машин
# "Жигули". Реализовать с помощью алгоритма сортировки слиянием
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] > right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1


cars = [
    {"Производитель": "Жигули", "Ремонты": 5},
    {"Производитель": "Жигули", "Ремонты": 2},
    {"Производитель": "Жигули", "Ремонты": 9},
    {"Производитель": "Жигули", "Ремонты": 4},
    {"Производитель": "Жигули", "Ремонты": 6},
    {"Производитель": "Жигули", "Ремонты": 3},
    {"Производитель": "Жигули", "Ремонты": 8},
    {"Производитель": "Жигули", "Ремонты": 1},
    {"Производитель": "Жигули", "Ремонты": 7},
    {"Производитель": "Жигули", "Ремонты": 10},
    {"Производитель": "Lada", "Ремонты": 7},
    {"Производитель": "Lada", "Ремонты": 5},
    {"Производитель": "Toyota", "Ремонты": 3}
]

zhiguli_repairs = [car["Ремонты"] for car in cars if car["Производитель"] == "Жигули"]

merge_sort(zhiguli_repairs)

print("Количество всех предыдущих ремонтов машин 'Жигули' по убыванию:")
for repairs in zhiguli_repairs:
    print(repairs)
