# Даны 2 кольцевых списка с фамилиями шахматистов 2-х команд.
# Произвести жеребьевку. В первой команде выбирается каждый n-й игрок, а во
# второй - каждый k-й

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def display(self):
        elems = []
        if self.head:
            current = self.head
            while True:
                elems.append(current.data)
                current = current.next
                if current == self.head:
                    break
        return elems

    def get_nth_player(self, n):
        players = []
        current = self.head
        count = 1
        if self.head:
            while True:
                if count % n == 0:
                    players.append(current.data)
                current = current.next
                count += 1
                if current == self.head:
                    break
        return players


def perform_draw(team1, team2, n, k):
    selected_team1 = team1.get_nth_player(n)
    selected_team2 = team2.get_nth_player(k)
    return selected_team1, selected_team2


team1 = CircularLinkedList()
team1.append("Иванов")
team1.append("Петров")
team1.append("Сидоров")
team1.append("Кузнецов")
team1.append("Смирнов")

team2 = CircularLinkedList()
team2.append("Ковалев")
team2.append("Попов")
team2.append("Лебедев")
team2.append("Соколов")
team2.append("Васильев")

n = 2
k = 3

selected_team1, selected_team2 = perform_draw(team1, team2, n, k)

print("Выбранные игроки из первой команды:", selected_team1)
print("Выбранные игроки из второй команды:", selected_team2)
