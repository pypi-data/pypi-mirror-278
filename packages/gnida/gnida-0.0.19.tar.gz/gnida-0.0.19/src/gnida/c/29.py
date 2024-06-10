# Дан однонаправленный связный список.
# Вставить элемент после n-го элемента списка

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

    def insert_after_n(self, data, n):
        new_node = Node(data)
        current = self.head
        count = 1
        while current and count < n:
            current = current.next
            count += 1
        if current:
            new_node.next = current.next
            current.next = new_node
        else:
            print(f"Невозможно вставить после {n}-го элемента, так как список короче {n}.")

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("NULL")


ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.append(4)

print("Оригинальный список:")
ll.print_list()

n = 3
m = 8
ll.insert_after_n(m, n)

print(f"Список после вставки {m} после {n}-го элемента:")
ll.print_list()
