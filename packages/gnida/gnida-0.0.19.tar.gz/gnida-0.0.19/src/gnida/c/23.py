# Дан кольцевой список из 20 фамилий студентов.
# Разбить студентов на 2 группы по 10 человек.
# Во вторую группу попадает каждый 11-й человек.
class CircularList:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if not self.items:
            raise StopIteration
        item = self.items[self.index % len(self.items)]
        self.index += 1
        return item

    def to_list(self, count):
        return [self.items[i % len(self.items)] for i in range(count)]


def split_students(circular_list):
    group2 = []
    iterator = iter(circular_list)
    count = 1
    while len(group2) < 10:
        student = next(iterator)
        if count % 11 == 0:
            group2.append(student)
        count += 1

    return group2


students = [
    "Студент1", "Студент2", "Студент3", "Студент4", "Студент5",
    "Студент6", "Студент7", "Студент8", "Студент9", "Студент10",
    "Студент11", "Студент12", "Студент13", "Студент14", "Студент15",
    "Студент16", "Студент17", "Студент18", "Студент19", "Студент20"
]

circular_list = CircularList(students)
group2 = split_students(circular_list)
group1 = [student for student in students if student not in group2]

print("Группа 1:")
print(group1)
print("Группа 2:")
print(group2)
