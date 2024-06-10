# Дан однонаправленный связный список. Удалить каждый второй элемент списка

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def delete_every_second(self):
        current = self.head
        index = 1
        while current and current.next:
            temp = current.next
            current.next = temp.next
            temp.next = None
            current = current.next
            index += 2

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("NULL")


ll = LinkedList()
ll.append(12)
ll.append(2)
ll.append(3)
ll.append(10)
ll.append(5)
ll.append(6)

print("Оригинальный список:")
ll.print_list()

ll.delete_every_second()

print("Список после удаления каждого второго элемента:")
ll.print_list()
