# 64. Даны 2 списка с фамилиями студентов 2-х групп. Перевести n студентов
# из 1-й группы во 2-ю. Число пересчета - k.

class CircularList:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        if not self.items:
            raise IndexError("CircularList is empty")
        return self.items[index % len(self.items)]

    def __str__(self):
        return str(self.items)

    def get_kth_elements(self, k, count):
        result = []
        index = k
        for _ in range(count):
            result.append(self.items.pop(index % len(self.items)))
            if len(self.items) == 0:
                break
            index += k - 1
        return result


def transfer_students(group1, group2, n, k):
    group1_list = CircularList()
    group2_list = CircularList()

    for student in group1:
        group1_list.add(student)

    for student in group2:
        group2_list.add(student)

    students_to_transfer = group1_list.get_kth_elements(k, n)

    for student in students_to_transfer:
        group2_list.add(student)

    new_group1 = list(group1_list.items)
    new_group2 = list(group2_list.items)

    return new_group1, new_group2


group1 = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов"]
group2 = ["Алексеев", "Борисов", "Васильев"]
n = 3
k = 2

new_group1, new_group2 = transfer_students(group1, group2, n, k)

print('Группы до перевода: ')
print("Первая группа:", group1)
print("Вторая группа:", group2)

print()

print('Группы после перевода: ')
print("Первая группа:", new_group1)
print("Вторая группа:", new_group2)
