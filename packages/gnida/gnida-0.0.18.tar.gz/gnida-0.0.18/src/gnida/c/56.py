# Дан двунаправленный связный список.
# Вставить элемент после n-го элемента списка


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last

    def insert_after_nth(self, data, n):
        if n < 0:
            raise ValueError("n должно быть неотрицательным целым числом")
        new_node = Node(data)
        current = self.head
        count = 1

        while current is not None and count < n:
            current = current.next
            count += 1

        if current is None:
            raise IndexError("Список содержит менее n элементов")

        new_node.next = current.next
        new_node.prev = current

        if current.next is not None:
            current.next.prev = new_node
        current.next = new_node

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()


dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
dll.append(3)
dll.append(4)

print("Список до вставки:")
dll.print_list()

n = 2
m = 5 # элемент, который вставляем
dll.insert_after_nth(m, n)

print("Список после вставки:")
dll.print_list()
