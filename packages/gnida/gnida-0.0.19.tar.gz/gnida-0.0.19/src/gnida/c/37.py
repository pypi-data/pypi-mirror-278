# 37. Расположить по алфавиту имена владельцев и, соответственно, вывести
# информацию об их машинах. Использовать алгоритм сортировки выбором.

owners_and_cars = [
    {"Владелец": "Мария", "Машина": "BMW M5 F90"},
    {"Владелец": "Вадим", "Машина": "Honda"},
    {"Владелец": "Юля", "Машина": "Audi Q8"},
    {"Владелец": "Рома", "Машина": "Lada"},
]


def selection_sort(data):
    n = len(data)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if data[j]["Владелец"] < data[min_index]["Владелец"]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]


selection_sort(owners_and_cars)

for entry in owners_and_cars:
    print(entry)
