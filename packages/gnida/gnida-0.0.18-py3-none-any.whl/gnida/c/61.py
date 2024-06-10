# 61. Даны 2 кольцевых списка: фамилии участников розыгрыша и названия
# призов. Выиграет n человек (каждый k-й). Число для пересчета призов - t.

class CircularList:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index % len(self.items)]

    def __str__(self):
        return str(self.items)

    def get_kth_elements(self, k, count):
        result = []
        index = 0
        for _ in range(count):
            result.append(self[index])
            index += k
        return result

    def get_kth(self, k, count):
        result = []
        index = k
        for _ in range(count):
            result.append(self[index])
            index += k
        return result


def distribute_prizes(surnames, prizes, n, k, t):
    surname_list = CircularList()
    prize_list = CircularList()

    for surname in surnames:
        surname_list.add(surname)

    for prize in prizes:
        prize_list.add(prize)

    winners = surname_list.get_kth(k, n)

    prizes_for_winners = prize_list.get_kth_elements(t, n)

    result = list(zip(winners, prizes_for_winners))

    return result


surnames = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов"]
prizes = ["100 рублей", "10 рублей", "50 рублей", "500 рублей", "5 рублей"]

n = 3
k = 2
t = 4

winners_with_prizes = distribute_prizes(surnames, prizes, n, k, t)
for winner, prize in winners_with_prizes:
    print(f"Победитель - {winner}, приз - {prize}")
